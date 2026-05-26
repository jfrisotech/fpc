import os
from fpc.core.utils import print_color, Colors
from fpc.templates.common.main_template import get_main_file_content
from fpc.templates.common.app_routes_template import get_app_routes_content
from fpc.templates.common.app_theme_template import get_app_theme_content
from fpc.templates.common.app_config_template import get_app_config_content
from fpc.templates.common.gitignore_template import get_gitignore_content
from fpc.templates.mvc.mvc_templates import create_mvc_templates
from fpc.templates.mvvm.mvvm_templates import create_mvvm_templates
from fpc.templates.clean_arch.clean_architecture_data import create_clean_architecture_data
from fpc.templates.clean_arch.clean_architecture_domain import create_clean_architecture_domain
from fpc.templates.clean_arch.clean_architecture_presentation import create_clean_architecture_presentation
from fpc.templates.common.initial_test_templates import (
    get_mvc_controller_test,
    get_mvvm_viewmodel_test,
    get_clean_usecase_test,
    get_clean_repository_impl_test,
)

def create_template_files(project_path: str, preferences: dict):
    """Create template files based on project preferences."""
    print_color("Creating template files...", Colors.BLUE)
    
    lib_path = os.path.join(project_path, 'lib')
    app_path = os.path.join(lib_path, 'app')
    os.makedirs(app_path, exist_ok=True)
    
    # Create main.dart and app_widget.dart
    _create_main_files(lib_path, app_path, preferences)
    
    # Create app configuration files
    _create_app_config_files(app_path, preferences)
    
    # Create design system files
    _create_design_system_files(app_path)
    
    # Create/Overwrite .gitignore
    with open(os.path.join(project_path, '.gitignore'), 'w') as file:
        file.write(get_gitignore_content())
    
    folder_structure = preferences.get('folder_structure', 'Standard (Layer First)')
    if folder_structure == 'Modular (Feature First)':
        auth_path = os.path.join(app_path, 'modules', 'auth')
        home_path = os.path.join(app_path, 'modules', 'home')
    else:
        auth_path = app_path
        home_path = app_path
        
    # Create architecture-specific files
    architecture = preferences.get('architecture', '')
    if architecture == 'MVC (Model-View-Controller)':
        _create_mvc_template_files(auth_path, home_path, preferences)
    elif architecture == 'MVVM (Model-View-ViewModel)':
        _create_mvvm_template_files(auth_path, home_path, preferences)
    elif architecture == 'Clean Architecture':
        _create_clean_architecture_template_files(auth_path, home_path, app_path, preferences)
    
    # Overwrite default flutter test file
    test_path = os.path.join(project_path, 'test')
    os.makedirs(test_path, exist_ok=True)
    project_name = os.path.basename(os.path.normpath(project_path))
    
    with open(os.path.join(test_path, 'widget_test.dart'), 'w') as file:
        file.write(f'''import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:{project_name}/app/app_widget.dart';

void main() {{
  testWidgets('AppWidget loading test', (WidgetTester tester) async {{
    // Build our app and trigger a frame.
    await tester.pumpWidget(const AppWidget());
    expect(find.byType(MaterialApp), findsOneWidget);
  }});
}}
''')

    # Create initial unit tests per architecture (Bug #9 fix)
    _create_initial_unit_tests(project_path, architecture, folder_structure)

    print_color("Template files created successfully!", Colors.GREEN)

def _create_main_files(lib_path: str, app_path: str, preferences: dict):
    """Create main.dart and app_widget.dart files."""
    # Generate content
    main_content, app_widget_content = get_main_file_content(preferences)
    
    with open(os.path.join(lib_path, 'main.dart'), 'w') as file:
        file.write(main_content)
        
    with open(os.path.join(app_path, 'app_widget.dart'), 'w') as file:
        file.write(app_widget_content)

def _create_app_config_files(lib_path: str, preferences: dict):
    """Create app configuration files."""
    config_path = os.path.join(lib_path, 'config')
    # Separate folder creation
    os.makedirs(config_path, exist_ok=True)
    
    # File creations
    # Create app_routes.dart
    with open(os.path.join(config_path, 'app_routes.dart'), 'w') as file:
        file.write(get_app_routes_content(preferences))
    
    # Create app_theme.dart
    with open(os.path.join(config_path, 'app_theme.dart'), 'w') as file:
        file.write(get_app_theme_content())

    # Create service_locator.dart conditionally
    architecture = preferences.get('architecture', '')
    state_management = preferences.get('state_management', 'None')
    
    if architecture == 'Clean Architecture' or state_management in ['BLoC', 'MobX', 'None']:
        from fpc.templates.common.service_locator_template import get_service_locator_content
        with open(os.path.join(config_path, 'service_locator.dart'), 'w') as file:
            file.write(get_service_locator_content())
    
    # Create app_config.dart for BaaS configuration
    baas = preferences['baas']
    if baas != 'None':
        with open(os.path.join(config_path, 'app_config.dart'), 'w') as file:
            file.write(get_app_config_content(preferences))

def _create_mvc_template_files(auth_path: str, home_path: str, preferences: dict):
    """Create template files for MVC architecture."""
    create_mvc_templates(auth_path, home_path, preferences)

def _create_mvvm_template_files(auth_path: str, home_path: str, preferences: dict):
    """Create template files for MVVM architecture."""
    create_mvvm_templates(auth_path, home_path, preferences)

def _create_clean_architecture_template_files(auth_path: str, home_path: str, app_path: str, preferences: dict):
    """Create template files for Clean Architecture."""
    from fpc.templates.clean_arch.core.clean_architecture_core import create_clean_architecture_core
    
    # Core is always bound to app_path
    create_clean_architecture_core(app_path)
    # Architecture specifics bound to auth_path (for auth feature)
    create_clean_architecture_data(auth_path, preferences)
    create_clean_architecture_domain(auth_path, preferences)
    create_clean_architecture_presentation(auth_path, preferences)
    
    # Note: For Clean Arch, we could also create a home page in home_path if needed, 
    # but currently it only generates the auth feature.

def _create_design_system_files(lib_path: str):
    """Create design system files in shared/theme folder."""
    from fpc.templates.shared.theme.app_colors_template import get_app_colors_content
    from fpc.templates.shared.theme.app_typography_template import get_app_typography_content
    from fpc.templates.shared.theme.app_spacing_template import get_app_spacing_content
    from fpc.templates.shared.theme.app_dimensions_template import get_app_dimensions_content
    
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


def _create_initial_unit_tests(project_path: str, architecture: str, folder_structure: str):
    """Create initial unit test files per architecture (Bug #9 fix)."""
    project_name = os.path.basename(os.path.normpath(project_path))
    test_path = os.path.join(project_path, 'test')
    is_modular = folder_structure == 'Modular (Feature First)'

    if architecture == 'MVC (Model-View-Controller)':
        if is_modular:
            ctrl_test_dir = os.path.join(test_path, 'app', 'modules', 'auth', 'controllers')
        else:
            ctrl_test_dir = os.path.join(test_path, 'app', 'controllers')
        os.makedirs(ctrl_test_dir, exist_ok=True)
        with open(os.path.join(ctrl_test_dir, 'auth_controller_test.dart'), 'w') as f:
            f.write(get_mvc_controller_test(project_name, is_modular))

    elif architecture == 'MVVM (Model-View-ViewModel)':
        if is_modular:
            vm_test_dir = os.path.join(test_path, 'app', 'modules', 'auth', 'viewmodels')
        else:
            vm_test_dir = os.path.join(test_path, 'app', 'viewmodels')
        os.makedirs(vm_test_dir, exist_ok=True)
        with open(os.path.join(vm_test_dir, 'auth_viewmodel_test.dart'), 'w') as f:
            f.write(get_mvvm_viewmodel_test(project_name, is_modular))

    elif architecture == 'Clean Architecture':
        if is_modular:
            usecase_dir = os.path.join(test_path, 'app', 'modules', 'auth', 'domain', 'usecases')
            repo_dir = os.path.join(test_path, 'app', 'modules', 'auth', 'data', 'repositories')
        else:
            usecase_dir = os.path.join(test_path, 'app', 'domain', 'usecases')
            repo_dir = os.path.join(test_path, 'app', 'data', 'repositories')

        os.makedirs(usecase_dir, exist_ok=True)
        os.makedirs(repo_dir, exist_ok=True)

        with open(os.path.join(usecase_dir, 'login_usecase_test.dart'), 'w') as f:
            f.write(get_clean_usecase_test(project_name, is_modular))

        with open(os.path.join(repo_dir, 'auth_repository_impl_test.dart'), 'w') as f:
            f.write(get_clean_repository_impl_test(project_name, is_modular))

