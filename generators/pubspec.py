import os
from core.utils import print_color, Colors

def update_pubspec(project_path: str, preferences: dict):
    """Update pubspec.yaml with dependencies based on preferences."""
    print_color("Updating pubspec.yaml...", Colors.BLUE)
    
    pubspec_path = os.path.join(project_path, 'pubspec.yaml')
    
    with open(pubspec_path, 'r') as file:
        content = file.read()
    
    dependencies = []
    dev_dependencies = []
    
    # Add dependencies based on state management choice
    state_management = preferences['state_management']
    if state_management == 'Provider':
        dependencies.append('  provider:')
    elif state_management == 'BLoC':
        dependencies.append('  flutter_bloc:')
        dependencies.append('  equatable:')
    elif state_management == 'GetX':
        dependencies.append('  get:')
    elif state_management == 'Riverpod':
        dependencies.append('  flutter_riverpod:')
    elif state_management == 'MobX':
        dependencies.append('  mobx:')
        dependencies.append('  flutter_mobx:')
        dev_dependencies.append('  mobx_codegen:')
    
    # Add dependencies based on HTTP client choice
    http_client = preferences['http_client']
    if http_client == 'Dio':
        dependencies.append('  dio:')
    elif http_client == 'http':
        dependencies.append('  http:')
    elif http_client == 'Retrofit':
        dependencies.append('  retrofit:')
        dependencies.append('  dio:')
        dev_dependencies.append('  retrofit_generator:')
        dev_dependencies.append('  json_serializable:')
    
    # Add dependencies based on local database choice
    database = preferences['database']
    if database == 'SQLite (sqflite)':
        dependencies.append('  sqflite:')
        dependencies.append('  path_provider:')
    elif database == 'Hive':
        dependencies.append('  hive:')
        dependencies.append('  hive_flutter:')
        dev_dependencies.append('  hive_generator:')
    elif database == 'Isar':
        dependencies.append('  isar:')
        dependencies.append('  isar_flutter_libs:')
        dependencies.append('  path_provider:')
        dev_dependencies.append('  isar_generator:')
    elif database == 'ObjectBox':
        dependencies.append('  objectbox:')
        dependencies.append('  objectbox_flutter_libs:')
        dependencies.append('  path_provider:')
        dev_dependencies.append('  objectbox_generator:')
    
    # Add dependencies based on BaaS choice
    baas = preferences['baas']
    if baas == 'Firebase':
        dependencies.append('  firebase_core:')
        dependencies.append('  firebase_auth:')
        dependencies.append('  cloud_firestore:')
    elif baas == 'Supabase':
        dependencies.append('  supabase_flutter:')
    elif baas == 'Appwrite':
        dependencies.append('  appwrite:')
    
    # Common utility dependencies
    dependencies.append('  path:')
    dependencies.append('  shared_preferences:')
    dependencies.append('  intl:')
    dev_dependencies.append('  logger:')

    # Dev dependencies
    if state_management == 'MobX' or http_client == 'Retrofit' or database == 'Hive' or  database == 'Isar' or database == 'ObjectBox':
        dev_dependencies.append('  build_runner:')
    
    # Insert dependencies into pubspec content
    if dependencies:
        dependency_block = '\n'.join(dependencies)
        updated_content = content.replace(
            'dependencies:\n  flutter:\n    sdk: flutter',
            f'dependencies:\n  flutter:\n    sdk: flutter\n\n{dependency_block}'
        )

        dev_dependency_block = '\n'.join(dev_dependencies)
        updated_content = updated_content.replace(
            'dev_dependencies:\n  flutter_test:\n    sdk: flutter',
            f'dev_dependencies:\n  flutter_test:\n    sdk: flutter\n\n{dev_dependency_block}'
        )
        
        with open(pubspec_path, 'w') as file:
            file.write(updated_content)
        
        print_color("pubspec.yaml updated successfully!", Colors.GREEN)
    else:
        print_color("No dependencies to add to pubspec.yaml", Colors.YELLOW)
