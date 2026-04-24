import os
import sys
import json
from typing import Dict, Any, Optional
from rich.console import Console
from rich.prompt import IntPrompt

from fpc.core.utils import print_color, Colors, to_snake_case, to_pascal_case
from fpc.generators.structure import generate_project_structure
from fpc.templates.templates import create_template_files
from fpc.generators.pubspec import update_pubspec
from fpc.config_manager import ConfigManager
from fpc.project_manager import ProjectManager
from fpc.template_manager import TemplateManager

class FlutterGenerator:
    """Class to generate Flutter project with custom structure."""

    def __init__(self):
        self.console = Console()
        self.project_manager = ProjectManager()
        self.config_manager = ConfigManager()
        self.template_manager = TemplateManager()
        
        self.architecture_options = [
            'MVC (Model-View-Controller)',
            'MVVM (Model-View-ViewModel)',
            'Clean Architecture',
        ]
        
        self.state_management_options = [
            'Provider',
            'BLoC',
            'GetX',
            'Riverpod',
            'MobX',
            'None',
        ]
        
        self.http_client_options = [
            'Dio',
            'http',
            'None',
        ]
        
        self.database_options = [
            'SQLite (sqflite)',
            'Hive',
            'Isar',
            'ObjectBox',
            'None',
        ]
        
        self.baas_options = [
            'Firebase',
            'Supabase',
            'Appwrite',
            'None',
        ]

    def get_user_choice(self, options, message) -> str:
        """Get user choice from a list of options."""
        self.console.print(f"\n[magenta bold]{message}[/magenta bold]")
        for i, option in enumerate(options, 1):
            self.console.print(f"  [cyan]{i}.[/cyan] {option}")
            
        while True:
            choice = IntPrompt.ask("[yellow]Select an option[/yellow]")
            if 1 <= choice <= len(options):
                return options[choice - 1]
            self.console.print(f"[red]Please enter a number between 1 and {len(options)}[/red]")

    def get_project_preferences(self, headless_args=None) -> Dict[str, str]:
        """Get user preferences for project structure, respecting headless args."""
        
        def map_choice(short_choice, full_options):
            if not short_choice:
                return None
            short_choice = short_choice.lower()
            for opt in full_options:
                if opt.lower().startswith(short_choice) or short_choice in opt.lower():
                    return opt
            return None

        architecture = None
        state_management = None
        http_client = None
        database = None
        baas = None
        folder_structure = None
        
        folder_structure_options = [
            'Standard (Layer First)',
            'Modular (Feature First)'
        ]
        
        if headless_args:
            architecture = map_choice(headless_args.get('arch'), self.architecture_options)
            state_management = map_choice(headless_args.get('state'), self.state_management_options)
            http_client = map_choice(headless_args.get('http'), self.http_client_options)
            database = map_choice(headless_args.get('db'), self.database_options)
            baas = map_choice(headless_args.get('baas'), self.baas_options)
            folder_structure = map_choice(headless_args.get('structure'), folder_structure_options)

        if not architecture:
            architecture = self.get_user_choice(self.architecture_options, "Select architecture pattern:")
        if not folder_structure:
            folder_structure = self.get_user_choice(folder_structure_options, "Select folder structure:")
        if not state_management:
            state_management = self.get_user_choice(self.state_management_options, "Select state management solution:")
        if not http_client:
            http_client = self.get_user_choice(self.http_client_options, "Select HTTP client:")
        if not database:
            database = self.get_user_choice(self.database_options, "Select local database:")
        if not baas:
            baas = self.get_user_choice(self.baas_options, "Select Backend-as-a-Service:")
        
        return {
            'architecture': architecture,
            'folder_structure': folder_structure,
            'state_management': state_management,
            'http_client': http_client,
            'database': database,
            'baas': baas,
        }

    def run_with_name_interactive(self, project_name: str, project_path: str, headless_args=None):
        """Run project creation with given project name and interactive/headless preferences."""
        print_color("Flutter Project CLI Generator", Colors.BOLD)
        
        preferences = self.get_project_preferences(headless_args)
        output_dir = os.path.dirname(project_path)
        
        created_project_path = self.project_manager.create_project(project_name, output_dir)
        if not created_project_path:
            return

        self.config_manager.save_config(created_project_path, preferences)
        generate_project_structure(created_project_path, preferences)
        create_template_files(created_project_path, preferences)
        update_pubspec(created_project_path, preferences)
        
        # Check if build_runner is needed
        state_management = preferences.get('state_management', '')
        database = preferences.get('database', '')
        
        if 'MobX' in state_management or any(db in database for db in ['Hive', 'Isar', 'ObjectBox']):
            self.project_manager.run_build_runner(created_project_path)
        
        print_color(f"Flutter project '{project_name}' created successfully!", Colors.GREEN)

    def generate_file(self, file_type: str, directory: str, name: str, state_management: Optional[str] = None):
        """Generate a file with specific state management and smart path detection."""
        
        # Suffix mapping
        type_mapping = {
            'ctrl': 'controller',
            'intf': 'interface',
            'repo': 'repository',
            'entity': 'entity',
            'controller': 'controller',
            'viewmodel': 'viewmodel',
            'vm': 'viewmodel',
            'view': 'view',
            'service': 'service',
            'model': 'model',
            'interface': 'interface',
            'repository': 'repository',
            'repository_impl': 'repository_impl'
        }
        
        if file_type == 'feature':
            self._generate_feature(directory, name, state_management)
            return

        actual_type = type_mapping.get(file_type.lower())
        if not actual_type:
            self.console.print(f"[red]Error: Invalid file type '{file_type}'.[/red]")
            return

        preferences = self.config_manager.get_config(directory)
        if not state_management:
            state_management = preferences.get('state_management', 'none')

        # Normalize name and handle suffix
        snake_name = to_snake_case(name)
        suffix = f"_{actual_type}"
        base_name = snake_name[:-len(suffix)] if snake_name.endswith(suffix) else snake_name
        
        final_file_name = f"{base_name}_{actual_type}.dart"
        file_path = os.path.join(directory, final_file_name)

        if os.path.exists(file_path):
            self.console.print(f"[yellow]Warning: File '{file_path}' already exists. Skipping.[/yellow]")
            return

        os.makedirs(directory, exist_ok=True)
        
        content = self.template_manager.get_template_content(actual_type, base_name, state_management)
        
        with open(file_path, 'w') as f:
            f.write(content)

        self.console.print(f"[green]Created {actual_type}:[/green] [cyan]{file_path}[/cyan]")
        
        # Automatically generate test file
        self._generate_test_file(directory, actual_type, base_name)

    def _generate_test_file(self, directory: str, file_type: str, base_name: str):
        """Generate a corresponding test file in the test/ directory mirroring the lib/ structure."""
        project_root = self.config_manager.find_project_root(directory)
        if not project_root:
            return

        # Find relative path from lib
        try:
            lib_pos = directory.find('/lib/')
            if lib_pos == -1:
                return # Not inside lib, skip test generation
                
            rel_path = directory[lib_pos + len('/lib/'):]
            test_dir = os.path.join(project_root, 'test', rel_path)
            os.makedirs(test_dir, exist_ok=True)
            
            test_file_name = f"{base_name}_{file_type}_test.dart"
            test_file_path = os.path.join(test_dir, test_file_name)
            
            if os.path.exists(test_file_path):
                return
                
            from fpc.templates.common.test_templates import get_unit_test_template, get_widget_test_template
            
            class_name = to_pascal_case(base_name) + to_pascal_case(file_type)
            # Find relative import path for the tested file
            # In Flutter tests, we usually use package: imports, but for now we'll just leave a placeholder or comment
            
            if file_type == 'view':
                content = get_widget_test_template(class_name, f"package:your_project/{rel_path}/{base_name}_{file_type}.dart")
            else:
                content = get_unit_test_template(class_name, f"package:your_project/{rel_path}/{base_name}_{file_type}.dart")
                
            with open(test_file_path, 'w') as f:
                f.write(content)
                
            self.console.print(f"[dim]Generated test:[/dim] [cyan]{test_file_path}[/cyan]")
        except Exception:
            # Silent fail for tests to not break the main flow
            pass

    def _generate_feature(self, directory: str, name: str, state_management: Optional[str]):
        """Generate a complete feature based on the project's architecture."""
        feature_name = to_snake_case(name)
        feature_dir = os.path.join(directory, feature_name)
        
        preferences = self.config_manager.get_config(directory)
        architecture = preferences.get('architecture', '')
        
        os.makedirs(feature_dir, exist_ok=True)
        
        if 'Clean Architecture' in architecture:
            # Clean Architecture subfolders
            data_dir = os.path.join(feature_dir, 'data')
            domain_dir = os.path.join(feature_dir, 'domain')
            presentation_dir = os.path.join(feature_dir, 'presentation')
            
            # Sub-sub folders
            os.makedirs(os.path.join(data_dir, 'datasources', 'local'), exist_ok=True)
            os.makedirs(os.path.join(data_dir, 'datasources', 'remote'), exist_ok=True)
            os.makedirs(os.path.join(data_dir, 'models'), exist_ok=True)
            os.makedirs(os.path.join(data_dir, 'repositories'), exist_ok=True)
            os.makedirs(os.path.join(domain_dir, 'entities'), exist_ok=True)
            os.makedirs(os.path.join(domain_dir, 'repositories'), exist_ok=True)
            os.makedirs(os.path.join(domain_dir, 'usecases'), exist_ok=True)
            
            pages_dir = os.path.join(presentation_dir, 'pages')
            os.makedirs(pages_dir, exist_ok=True)
            os.makedirs(os.path.join(presentation_dir, 'widgets'), exist_ok=True)
            
            # Map state management to folder name
            sm = (state_management or preferences.get('state_management', 'none')).lower()
            state_folder = 'bloc'
            if 'riverpod' in sm: state_folder = 'notifiers'
            elif 'provider' in sm: state_folder = 'providers'
            elif 'getx' in sm: state_folder = 'controllers'
            elif 'mobx' in sm: state_folder = 'store'
            
            os.makedirs(os.path.join(presentation_dir, state_folder), exist_ok=True)
            
            # Generate files in their places
            self.generate_file('controller', os.path.join(presentation_dir, state_folder), feature_name, state_management)
            self.generate_file('view', pages_dir, feature_name, state_management)
            self.generate_file('service', os.path.join(data_dir, 'datasources', 'remote'), feature_name, state_management)
            self.generate_file('model', os.path.join(data_dir, 'models'), feature_name, state_management)
            self.generate_file('repository_impl', os.path.join(data_dir, 'repositories'), feature_name, state_management)
            self.generate_file('interface', os.path.join(domain_dir, 'repositories'), f"{feature_name}_repository", state_management)
            self.generate_file('entity', os.path.join(domain_dir, 'entities'), feature_name, state_management)
            
        else:
            # MVC / MVVM / Generic subfolders
            ctrl_type = 'viewmodel' if 'MVVM' in architecture else 'controller'
            ctrl_dir = os.path.join(feature_dir, f'{ctrl_type}s')
            view_dir = os.path.join(feature_dir, 'views')
            repo_dir = os.path.join(feature_dir, 'repositories')
            service_dir = os.path.join(feature_dir, 'services')
            model_dir = os.path.join(feature_dir, 'models')
            
            os.makedirs(ctrl_dir, exist_ok=True)
            os.makedirs(view_dir, exist_ok=True)
            os.makedirs(repo_dir, exist_ok=True)
            os.makedirs(service_dir, exist_ok=True)
            os.makedirs(model_dir, exist_ok=True)
            
            self.generate_file(ctrl_type, ctrl_dir, feature_name, state_management)
            self.generate_file('view', view_dir, feature_name, state_management)
            self.generate_file('service', service_dir, feature_name, state_management)
            self.generate_file('model', model_dir, feature_name, state_management)
            self.generate_file('repository', repo_dir, feature_name, state_management)
        
        self.console.print(f"[bold green]Feature '{feature_name}' generated successfully with {architecture} structure.[/bold green]")

    def add_file(self, file_type: str, directory: str, name: str):
        """Legacy support for add_file, redirects to generate_file."""
        self.generate_file(file_type, directory, name)

    def run_pubspec_script(self, script_name: str, current_dir: str):
        """Read pubspec.yaml and run the specified script if it exists."""
        project_root = self.config_manager.find_project_root(current_dir)
        if not project_root:
            print_color("Could not find project root.", Colors.RED)
            return

        pubspec_path = os.path.join(project_root, 'pubspec.yaml')
        
        from ruamel.yaml import YAML
        yaml = YAML()
        try:
            with open(pubspec_path, 'r') as f:
                data = yaml.load(f)
            
            scripts = data.get('scripts', {})
            if scripts and script_name in scripts:
                command = scripts[script_name]
                print_color(f"Running custom script '{script_name}': {command}", Colors.BLUE)
                
                import shlex
                cmd_args = shlex.split(command)
                
                if cmd_args[0] == 'flutter':
                    self.project_manager.run_flutter_command(project_root, cmd_args[1:], f"Executing {script_name}...")
                else:
                    import subprocess
                    subprocess.run(cmd_args, cwd=project_root, check=True)
            else:
                print_color(f"Script '{script_name}' not found. Trying 'flutter pub run {script_name}'...", Colors.YELLOW)
                self.project_manager.run_flutter_command(project_root, ['pub', 'run', script_name], f"Executing {script_name}...")
        except Exception as e:
            print_color(f"Error: {e}", Colors.RED)
