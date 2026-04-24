import os
from fpc.core.utils import print_color, Colors

def generate_project_structure(project_path: str, preferences: dict):
    """Generate project directory structure based on preferences."""
    print_color("Generating project structure...", Colors.BLUE)
    
    lib_path = os.path.join(project_path, 'lib')
    
    # Create assets in the project root
    os.makedirs(os.path.join(project_path, 'assets'), exist_ok=True)
    
    app_path = os.path.join(lib_path, 'app')
    os.makedirs(app_path, exist_ok=True)
    
    # Create common directories inside app_path
    common_dirs = ['config', 'utils', 'shared', 'shared/theme', 'l10n']
    _create_directories(app_path, common_dirs)
    
    folder_structure = preferences.get('folder_structure', 'Standard (Layer First)')
    if folder_structure == 'Modular (Feature First)':
        arch_path = os.path.join(app_path, 'modules', 'auth')
    else:
        arch_path = app_path
    os.makedirs(arch_path, exist_ok=True)
    
    # Create architecture-specific directories
    architecture = preferences.get('architecture', '')
    if architecture == 'MVC (Model-View-Controller)':
        _create_mvc_structure(arch_path)
    elif architecture == 'MVVM (Model-View-ViewModel)':
        _create_mvvm_structure(arch_path)
    elif architecture == 'Clean Architecture':
        state_management = preferences.get('state_management', 'None')
        _create_clean_architecture_structure(arch_path, app_path, state_management)
    
    print_color("Project structure generated successfully!", Colors.GREEN)

def _create_directories(base_path: str, directories: list):
    """Create directories within the base path."""
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)

def _create_mvc_structure(arch_path: str):
    """Create MVC architecture structure."""
    _create_directories(arch_path, [
        'models',
        'views',
        'controllers',
        'repositories',
        'services',
        'widgets',
    ])

def _create_mvvm_structure(arch_path: str):
    """Create MVVM architecture structure."""
    _create_directories(arch_path, [
        'models',
        'views',
        'viewmodels',
        'repositories',
        'services',
        'widgets',
    ])

def _create_clean_architecture_structure(arch_path: str, lib_path: str, state_management: str):
    """Create Clean Architecture structure."""
    # Core is always global
    _create_directories(lib_path, [
        'core',
        'core/error',
        'core/network',
        'core/usecases',
        'core/util',
    ])
    
    # Map state management to folder name
    state_folder = 'bloc'
    sm_lower = state_management.lower()
    if 'riverpod' in sm_lower:
        state_folder = 'notifiers'
    elif 'provider' in sm_lower:
        state_folder = 'providers'
    elif 'getx' in sm_lower:
        state_folder = 'controllers'
    elif 'mobx' in sm_lower:
        state_folder = 'store'
    elif 'none' in sm_lower:
        state_folder = None

    # Features go to arch_path
    presentation_dirs = [
        'presentation',
        'presentation/pages',
        'presentation/widgets',
    ]
    if state_folder:
        presentation_dirs.append(f'presentation/{state_folder}')

    _create_directories(arch_path, [
        'data',
        'data/datasources',
        'data/datasources/local',
        'data/datasources/remote',
        'data/models',
        'data/repositories',
        'domain',
        'domain/entities',
        'domain/repositories',
        'domain/usecases',
    ] + presentation_dirs)


