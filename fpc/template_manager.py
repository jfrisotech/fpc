import os
from typing import Dict, Any, Optional
from .core.utils import to_snake_case, to_pascal_case

class TemplateManager:
    """Manages template retrieval and generation."""
    
    @staticmethod
    def get_template_content(file_type: str, name: str, state_management: Optional[str] = None) -> str:
        """Fetch template content for a given type, name, and state management."""
        class_name = to_pascal_case(name)
        # Ensure suffix is present in class name (e.g. UserProfile + ViewModel)
        type_suffix = to_pascal_case(file_type)
        if file_type == 'viewmodel':
            type_suffix = 'ViewModel'
            
        if not class_name.endswith(type_suffix):
            # Special case for repository_impl -> RepositoryImpl
            if file_type == 'repository_impl':
                if not class_name.endswith('Repository'):
                    class_name += 'RepositoryImpl'
                else:
                    class_name += 'Impl'
            else:
                class_name += type_suffix
                
        sm = (state_management or 'none').lower()
        
        # Mapping file types to generic templates
        generic_mapping = {
            'controller': 'fpc.templates.generic.controller_template',
            'viewmodel': 'fpc.templates.generic.controller_template',  # Generic fallback
            'view': 'fpc.templates.generic.view_template',
            'service': 'fpc.templates.generic.service_template',
            'model': 'fpc.templates.generic.model_template',
            'interface': 'fpc.templates.generic.interface_template',
            'repository': 'fpc.templates.generic.repository_template',
            'repository_impl': 'fpc.templates.generic.repository_template', # Fallback to generic repo or specific impl
            'entity': 'fpc.templates.generic.entity_template',
        }
        
        # Mapping for SM-specific templates
        sm_mapping = {
            'none': {
                'repository_impl': 'fpc.templates.clean_arch.repository_impl_template'
            },
            'mobx': {
                'controller': 'fpc.templates.mobx.controller_template',
                'viewmodel': 'fpc.templates.mobx.controller_template',
                'view': 'fpc.templates.mobx.view_template'
            },
            'provider': {
                'controller': 'fpc.templates.provider.controller_template',
                'viewmodel': 'fpc.templates.provider.controller_template',
                'view': 'fpc.templates.provider.view_template'
            },
            'bloc': {
                'controller': 'fpc.templates.bloc.controller_template',
                'viewmodel': 'fpc.templates.bloc.controller_template',
                'view': 'fpc.templates.bloc.view_template'
            },
            'getx': {
                'controller': 'fpc.templates.getx.controller_template',
                'viewmodel': 'fpc.templates.getx.controller_template',
                'view': 'fpc.templates.getx.view_template'
            },
            'riverpod': {
                'controller': 'fpc.templates.riverpod.controller_template',
                'viewmodel': 'fpc.templates.riverpod.controller_template',
                'view': 'fpc.templates.riverpod.view_template'
            }
        }
        
        # Try SM-specific template first
        target_sm = sm
        if sm not in sm_mapping or file_type not in sm_mapping[sm]:
            target_sm = 'none'

        if target_sm in sm_mapping and file_type in sm_mapping[target_sm]:
            module_path = sm_mapping[target_sm][file_type]
            try:
                module = __import__(module_path, fromlist=['*'])
                # Use sm if available, else use 'none' for func name
                func_sm = sm if sm in sm_mapping and file_type in sm_mapping[sm] else 'none'
                func_name = f"get_{func_sm}_{file_type}_template"
                
                # Special cases for function names
                if not hasattr(module, func_name):
                    possible_names = [
                        f"get_{file_type}_template",
                        f"get_{sm}_{file_type}_template",
                        "get_controller_template" if file_type == 'viewmodel' else None
                    ]
                    for p_name in possible_names:
                        if p_name and hasattr(module, p_name):
                            func_name = p_name
                            break
                
                try:
                    return getattr(module, func_name)(class_name, name)
                except (TypeError, AttributeError):
                    return getattr(module, func_name)(class_name)
            except (ImportError, AttributeError):
                pass
        
        # Fallback to generic
        if file_type in generic_mapping:
            module_path = generic_mapping[file_type]
            try:
                module = __import__(module_path, fromlist=['*'])
                func_name = f"get_{file_type}_template"
                # Fallback to controller template for viewmodel
                if not hasattr(module, func_name) and file_type == 'viewmodel':
                    func_name = "get_controller_template"
                    
                try:
                    return getattr(module, func_name)(class_name, name)
                except (ImportError, AttributeError, TypeError):
                    return getattr(module, func_name)(class_name)
            except (ImportError, AttributeError):
                pass
                
        return f"// Template for {file_type} {name} (SM: {sm}) not found."
