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
        dependencies.append('  provider: ^6.1.1')
    elif state_management == 'BLoC':
        dependencies.append('  flutter_bloc: ^8.1.3')
        dependencies.append('  equatable: ^2.0.5')
    elif state_management == 'GetX':
        dependencies.append('  get: ^4.6.6')
    elif state_management == 'Riverpod':
        dependencies.append('  flutter_riverpod: ^2.4.9')
    elif state_management == 'MobX':
        dependencies.append('  mobx: ^2.2.3')
        dependencies.append('  flutter_mobx: ^2.2.0')
        dev_dependencies.append('  mobx_codegen: ^2.4.0')
    
    # Add dependencies based on HTTP client choice
    http_client = preferences['http_client']
    if http_client == 'Dio':
        dependencies.append('  dio: ^5.4.0')
    elif http_client == 'http':
        dependencies.append('  http: ^1.1.2')
    elif http_client == 'Retrofit':
        dependencies.append('  retrofit: ^4.0.3')
        dependencies.append('  dio: ^5.4.0')
        dev_dependencies.append('  retrofit_generator: ^8.0.6')
        dev_dependencies.append('  json_serializable: ^6.7.1')
    
    # Add dependencies based on local database choice
    database = preferences['database']
    if database == 'SQLite (sqflite)':
        dependencies.append('  sqflite: ^2.3.0')
        dependencies.append('  path_provider: ^2.1.1')
    elif database == 'Hive':
        dependencies.append('  hive: ^2.2.3')
        dependencies.append('  hive_flutter: ^1.1.0')
        dev_dependencies.append('  hive_generator: ^2.0.1')
    elif database == 'Isar':
        dependencies.append('  isar: ^3.1.0+1')
        dependencies.append('  isar_flutter_libs: ^3.1.0+1')
        dependencies.append('  path_provider: ^2.1.1')
        dev_dependencies.append('  isar_generator: ^3.1.0+1')
    elif database == 'ObjectBox':
        dependencies.append('  objectbox: ^2.3.1')
        dependencies.append('  objectbox_flutter_libs: ^2.3.1')
        dependencies.append('  path_provider: ^2.1.1')
        dev_dependencies.append('  objectbox_generator: ^2.3.1')
    
    # Add dependencies based on BaaS choice
    baas = preferences['baas']
    if baas == 'Firebase':
        dependencies.append('  firebase_core: ^2.24.2')
        dependencies.append('  firebase_auth: ^4.15.3')
        dependencies.append('  cloud_firestore: ^4.13.6')
    elif baas == 'Supabase':
        dependencies.append('  supabase_flutter: ^1.10.24')
    elif baas == 'Appwrite':
        dependencies.append('  appwrite: ^11.0.1')
    
    # Common utility dependencies
    dependencies.append('  path: ^1.8.3')
    dependencies.append('  shared_preferences: ^2.2.2')
    dependencies.append('  intl: ^0.18.1')
    dev_dependencies.append('  logger: ^2.0.2+1')

    # Dev dependencies
    if state_management == 'MobX' or http_client == 'Retrofit' or database == 'Hive' or  database == 'Isar' or database == 'ObjectBox':
        dev_dependencies.append('  build_runner: ^2.4.7')
    
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
