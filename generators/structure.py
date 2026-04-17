import os
from core.utils import print_color, Colors

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
        _create_clean_architecture_structure(arch_path, app_path)
    
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
        'services',
        'widgets',
    ])

def _create_mvvm_structure(arch_path: str):
    """Create MVVM architecture structure."""
    _create_directories(arch_path, [
        'models',
        'views',
        'viewmodels',
        'services',
        'widgets',
    ])

def _create_clean_architecture_structure(arch_path: str, lib_path: str):
    """Create Clean Architecture structure."""
    # Core is always global
    _create_directories(lib_path, [
        'core',
        'core/error',
        'core/network',
        'core/usecases',
        'core/util',
    ])
    # Features go to arch_path
    _create_directories(arch_path, [
        'data',
        'data/datasources',
        'data/models',
        'data/repositories',
        'domain',
        'domain/entities',
        'domain/repositories',
        'domain/usecases',
        'presentation',
        'presentation/bloc',
        'presentation/pages',
        'presentation/widgets',
    ])


