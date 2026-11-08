import os
from fpc.core.utils import print_color, Colors

def generate_project_structure(project_path: str, preferences: dict):
    """Generate project directory structure based on preferences."""
    print_color("Generating project structure...", Colors.BLUE)
    
    lib_path = os.path.join(project_path, 'lib')
    
    # Create assets in the project root
    assets_path = os.path.join(project_path, 'assets')
    images_path = os.path.join(assets_path, 'images')
    icons_path = os.path.join(assets_path, 'icons')
    os.makedirs(images_path, exist_ok=True)
    os.makedirs(icons_path, exist_ok=True)
    with open(os.path.join(images_path, '.gitkeep'), 'w') as f:
        pass
    with open(os.path.join(icons_path, '.gitkeep'), 'w') as f:
        pass
    
    app_path = os.path.join(lib_path, 'app')
    os.makedirs(app_path, exist_ok=True)
    
    # Create common directories inside app_path
    common_dirs = [
        'config',
        'shared',
        'shared/theme',
        'shared/utils',
        'shared/assets',
        'shared/storage',
    ]
    _create_directories(app_path, common_dirs)
    
    folder_structure = preferences.get('folder_structure', 'Standard (Layer First)')
    if folder_structure == 'Modular (Feature First)':
        arch_path = os.path.join(app_path, 'modules', 'auth')
    else:
        arch_path = app_path
    os.makedirs(arch_path, exist_ok=True)
    
    # Create architecture-specific directories
    architecture = preferences.get('architecture', '')
    state_management = preferences.get('state_management', 'None')
    if architecture == 'MVC (Model-View-Controller)':
        _create_mvc_structure(arch_path, state_management)
    elif architecture == 'MVVM (Model-View-ViewModel)':
        _create_mvvm_structure(arch_path, state_management)
    elif architecture == 'Clean Architecture':
        _create_clean_architecture_structure(arch_path, app_path, preferences)
    
    print_color("Project structure generated successfully!", Colors.GREEN)

def _create_directories(base_path: str, directories: list):
    """Create directories within the base path."""
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)

def _create_mvc_structure(arch_path: str, state_management: str = 'None'):
    """Create MVC architecture structure."""
    dirs = [
        'models',
        'views',
        'controllers',
        'services',
    ]
    if 'getx' in state_management.lower():
        dirs.append('bindings')
    _create_directories(arch_path, dirs)

def _create_mvvm_structure(arch_path: str, state_management: str = 'None'):
    """Create MVVM architecture structure."""
    dirs = [
        'models',
        'views',
        'viewmodels',
        'services',
    ]
    if 'getx' in state_management.lower():
        dirs.append('bindings')
    _create_directories(arch_path, dirs)

def _create_clean_architecture_structure(arch_path: str, lib_path: str, preferences: dict):
    """Create Clean Architecture structure."""
    # Core is always global
    _create_directories(lib_path, [
        'core',
        'core/error',
        'core/network',
        'core/usecases',
    ])
    
    state_management = preferences.get('state_management', 'None')
    database = preferences.get('database', 'None')

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
    elif 'cubit' in sm_lower:
        state_folder = 'cubit'
    elif 'none' in sm_lower:
        state_folder = None

    # Features go to arch_path
    presentation_dirs = [
        'presentation',
        'presentation/pages',
    ]
    if state_folder:
        presentation_dirs.append(f'presentation/{state_folder}')
    if 'getx' in sm_lower:
        presentation_dirs.append('presentation/bindings')

    datasources_dirs = [
        'data',
        'data/datasources',
        'data/datasources/remote',
    ]
    if database and database.lower() != 'none':
        datasources_dirs.append('data/datasources/local')

    _create_directories(arch_path, datasources_dirs + [
        'data/models',
        'data/repositories',
        'domain',
        'domain/entities',
        'domain/repositories',
        'domain/usecases',
    ] + presentation_dirs)


