import os
import subprocess
from fpc.core.utils import print_color, Colors
from rich.console import Console

def update_pubspec(project_path: str, preferences: dict):
    """Update pubspec.yaml with dependencies based on preferences using flutter pub add."""
    
    deps_to_fetch = set()
    dev_deps_to_fetch = set()
    
    # Architecture
    architecture = preferences.get('architecture')
    if architecture == 'Clean Architecture':
        deps_to_fetch.add('dartz')
        
    # State management
    state_management = preferences.get('state_management')
    if state_management == 'Provider':
        deps_to_fetch.add('provider')
    elif state_management == 'BLoC':
        deps_to_fetch.add('flutter_bloc')
        deps_to_fetch.add('equatable')
    elif state_management == 'GetX':
        deps_to_fetch.add('get')
    elif state_management == 'Riverpod':
        deps_to_fetch.add('flutter_riverpod')
    elif state_management == 'MobX':
        deps_to_fetch.add('mobx')
        deps_to_fetch.add('flutter_mobx')
        dev_deps_to_fetch.add('mobx_codegen')
    
    # HTTP client
    http_client = preferences.get('http_client')
    if http_client == 'Dio':
        deps_to_fetch.add('dio')
    elif http_client == 'http':
        deps_to_fetch.add('http')
    
    # Database
    database = preferences.get('database')
    if database == 'SQLite (sqflite)':
        deps_to_fetch.add('sqflite')
        deps_to_fetch.add('path_provider')
    elif database == 'Hive':
        deps_to_fetch.add('hive')
        deps_to_fetch.add('hive_flutter')
        dev_deps_to_fetch.add('hive_generator')
    elif database == 'Isar':
        deps_to_fetch.add('isar')
        deps_to_fetch.add('isar_flutter_libs')
        deps_to_fetch.add('path_provider')
        dev_deps_to_fetch.add('isar_generator')
    elif database == 'ObjectBox':
        deps_to_fetch.add('objectbox')
        deps_to_fetch.add('objectbox_flutter_libs')
        deps_to_fetch.add('path_provider')
        dev_deps_to_fetch.add('objectbox_generator')
    
    # BaaS
    baas = preferences.get('baas')
    if baas == 'Firebase':
        deps_to_fetch.add('firebase_core')
        deps_to_fetch.add('firebase_auth')
        deps_to_fetch.add('cloud_firestore')
    elif baas == 'Supabase':
        deps_to_fetch.add('supabase_flutter')
    elif baas == 'Appwrite':
        deps_to_fetch.add('appwrite')
    
    # Common utility dependencies
    if architecture == 'Clean Architecture' or state_management in ['BLoC', 'MobX', 'None']:
        deps_to_fetch.add('get_it')
        
    deps_to_fetch.add('path')
    deps_to_fetch.add('shared_preferences')
    deps_to_fetch.add('intl')
    dev_deps_to_fetch.add('logger')

    # Dev dependencies for build_runner
    if state_management == 'MobX' or database in ['Hive', 'Isar', 'ObjectBox']:
        dev_deps_to_fetch.add('build_runner')
        
    console = Console()
    with console.status("[bold blue]Resolving and injecting compatible packages via flutter pub add...[/bold blue]", spinner="dots"):
        all_deps = list(deps_to_fetch) + [f"dev:{pkg}" for pkg in dev_deps_to_fetch]
        
        if all_deps:
            try:
                subprocess.run(
                    ['flutter', 'pub', 'add'] + all_deps,
                    cwd=project_path,
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                print_color(f"Error resolving dependencies: {e.stderr}", Colors.RED)
                
    print_color("pubspec.yaml updated with compatible versions successfully!", Colors.GREEN)
