import os
from core.utils import print_color, Colors
from templates.common.main_template import get_main_file_content
from templates.common.app_routes_template import get_app_routes_content
from templates.common.app_theme_template import get_app_theme_content
from templates.common.app_config_template import get_app_config_content
from templates.mvc.mvc_templates import create_mvc_templates
from templates.mvvm.mvvm_templates import create_mvvm_templates
from templates.clean_arch.clean_architecture_data import create_clean_architecture_data
from templates.clean_arch.clean_architecture_domain import create_clean_architecture_domain
from templates.clean_arch.clean_architecture_presentation import create_clean_architecture_presentation

def create_template_files(project_path: str, preferences: dict):
    """Create template files based on project preferences."""
    print_color("Creating template files...", Colors.BLUE)
    
    lib_path = os.path.join(project_path, 'lib')
    
    # Create main.dart
    _create_main_file(lib_path, preferences)
    
    # Create app configuration files
    _create_app_config_files(lib_path, preferences)
    
    # Create design system files
    _create_design_system_files(lib_path)
    
    # Create architecture-specific files
    architecture = preferences['architecture']
    if architecture == 'MVC (Model-View-Controller)':
        _create_mvc_template_files(lib_path, preferences)
    elif architecture == 'MVVM (Model-View-ViewModel)':
        _create_mvvm_template_files(lib_path, preferences)
    elif architecture == 'Clean Architecture':
        _create_clean_architecture_template_files(lib_path, preferences)
    
    print_color("Template files created successfully!", Colors.GREEN)

def _create_main_file(lib_path: str, preferences: dict):
    """Create main.dart file."""
    main_content = get_main_file_content(preferences)
    # Ensure lib_path exists
    os.makedirs(lib_path, exist_ok=True)
    with open(os.path.join(lib_path, 'main.dart'), 'w') as file:
        file.write(main_content)

def _create_app_config_files(lib_path: str, preferences: dict):
    """Create app configuration files."""
    config_path = os.path.join(lib_path, 'config')
    # Separate folder creation
    os.makedirs(config_path, exist_ok=True)
    
    # File creations
    # Create app_routes.dart
    with open(os.path.join(config_path, 'app_routes.dart'), 'w') as file:
        file.write(get_app_routes_content())
    
    # Create app_theme.dart
    with open(os.path.join(config_path, 'app_theme.dart'), 'w') as file:
        file.write(get_app_theme_content())
    
    # Create app_config.dart for BaaS configuration
    baas = preferences['baas']
    if baas != 'None':
        with open(os.path.join(config_path, 'app_config.dart'), 'w') as file:
            file.write(get_app_config_content(preferences))

def _create_mvc_template_files(lib_path: str, preferences: dict):
    """Create template files for MVC architecture."""
    create_mvc_templates(lib_path)

def _create_mvvm_template_files(lib_path: str, preferences: dict):
    """Create template files for MVVM architecture."""
    create_mvvm_templates(lib_path, preferences)

def _create_clean_architecture_template_files(lib_path: str, preferences: dict):
    """Create template files for Clean Architecture."""
    from templates.clean_arch.core.clean_architecture_core import create_clean_architecture_core
    
    create_clean_architecture_core(lib_path)
    create_clean_architecture_data(lib_path)
    create_clean_architecture_domain(lib_path)
    create_clean_architecture_presentation(lib_path)

def _create_design_system_files(lib_path: str):
    """Create design system files in shared/theme folder."""
    from templates.shared.theme.app_colors_template import get_app_colors_content
    from templates.shared.theme.app_typography_template import get_app_typography_content
    from templates.shared.theme.app_spacing_template import get_app_spacing_content
    from templates.shared.theme.app_dimensions_template import get_app_dimensions_content
    
    theme_path = os.path.join(lib_path, 'shared', 'theme')
    os.makedirs(theme_path, exist_ok=True)
    
    # Create app_colors.dart
    with open(os.path.join(theme_path, 'app_colors.dart'), 'w') as file:
        file.write(get_app_colors_content())
    
    # Create app_typography.dart
    with open(os.path.join(theme_path, 'app_typography.dart'), 'w') as file:
        file.write(get_app_typography_content())
    
    # Create app_spacing.dart
    with open(os.path.join(theme_path, 'app_spacing.dart'), 'w') as file:
        file.write(get_app_spacing_content())
    
    # Create app_dimensions.dart
    with open(os.path.join(theme_path, 'app_dimensions.dart'), 'w') as file:
        file.write(get_app_dimensions_content())
