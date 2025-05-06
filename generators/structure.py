import os
from core.utils import print_color, Colors

def generate_project_structure(project_path: str, preferences: dict):
    """Generate project directory structure based on preferences."""
    print_color("Generating project structure...", Colors.BLUE)
    
    lib_path = os.path.join(project_path, 'lib')
    
    # Create common directories
    common_dirs = ['assets', 'config', 'utils', 'theme', 'l10n']
    _create_directories(lib_path, common_dirs)
    
    # Create architecture-specific directories
    architecture = preferences['architecture']
    if architecture == 'MVC (Model-View-Controller)':
        _create_mvc_structure(lib_path)
    elif architecture == 'MVVM (Model-View-ViewModel)':
        _create_mvvm_structure(lib_path)
    elif architecture == 'Clean Architecture':
        _create_clean_architecture_structure(lib_path)
    
    print_color("Project structure generated successfully!", Colors.GREEN)

def _create_directories(base_path: str, directories: list):
    """Create directories within the base path."""
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)

def _create_mvc_structure(lib_path: str):
    """Create MVC architecture structure."""
    _create_directories(lib_path, [
        'models',
        'views',
        'controllers',
        'services',
        'widgets',
    ])

def _create_mvvm_structure(lib_path: str):
    """Create MVVM architecture structure."""
    _create_directories(lib_path, [
        'models',
        'views',
        'viewmodels',
        'services',
        'widgets',
    ])

def _create_clean_architecture_structure(lib_path: str):
    """Create Clean Architecture structure."""
    _create_directories(lib_path, [
        'core',
        'core/error',
        'core/network',
        'core/usecases',
        'core/util',
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


