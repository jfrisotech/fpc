import os
import sys
import subprocess
from typing import Dict
from core.utils import print_color, Colors
from generators.structure import generate_project_structure
from templates.templates import create_template_files
from generators.pubspec import update_pubspec

class FlutterGenerator:
    """Class to generate Flutter project with custom structure."""

    def __init__(self):
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
            'Retrofit',
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
        print_color(message, Colors.HEADER)
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        while True:
            try:
                choice = input(f"{Colors.YELLOW}Select an option (1-{len(options)}): {Colors.ENDC}")
                index = int(choice) - 1
                if 0 <= index < len(options):
                    return options[index]
                else:
                    print_color(f"Please enter a number between 1 and {len(options)}", Colors.RED)
            except ValueError:
                print_color("Please enter a valid number", Colors.RED)

    def get_project_preferences(self) -> Dict[str, str]:
        """Get user preferences for project structure."""
        architecture = self.get_user_choice(
            self.architecture_options,
            "Select architecture pattern:"
        )
        
        state_management = self.get_user_choice(
            self.state_management_options,
            "Select state management solution:"
        )
        
        http_client = self.get_user_choice(
            self.http_client_options,
            "Select HTTP client:"
        )
        
        database = self.get_user_choice(
            self.database_options,
            "Select local database:"
        )
        
        baas = self.get_user_choice(
            self.baas_options,
            "Select Backend-as-a-Service:"
        )
        
        return {
            'architecture': architecture,
            'state_management': state_management,
            'http_client': http_client,
            'database': database,
            'baas': baas,
        }

    def create_flutter_project(self, project_name: str, output_dir: str) -> str:
        """Create a base Flutter project."""
        print_color(f"Creating base Flutter project '{project_name}'...", Colors.BLUE)
        
        project_path = os.path.join(output_dir, project_name)
        
        try:
            subprocess.run(
                ['flutter', 'create', '--project-name', project_name, project_path],
                check=True,
                capture_output=True,
                text=True
            )
            print_color("Base Flutter project created successfully!", Colors.GREEN)
            return project_path
        except subprocess.CalledProcessError as e:
            print_color(f"Error creating Flutter project: {e.stderr}", Colors.RED)
            sys.exit(1)
        except FileNotFoundError:
            print_color("Flutter command not found. Make sure Flutter is installed and in your PATH.", Colors.RED)
            sys.exit(1)

    def run(self):
        print_color("Flutter Project CLI Generator", Colors.BOLD)
        project_name = input("Enter your Flutter project name: ").strip()
        if not project_name:
            print_color("Project name cannot be empty.", Colors.RED)
            return
        
        output_dir = os.getcwd()
        
        preferences = self.get_project_preferences()
        
        project_path = self.create_flutter_project(project_name, output_dir)
        
        generate_project_structure(project_path, preferences)
        
        create_template_files(project_path, preferences)
        
        update_pubspec(project_path, preferences)
        
        print_color(f"Flutter project '{project_name}' created successfully with the selected options.", Colors.GREEN)

    def run_with_name_interactive(self, project_name: str, project_path: str):
        """Run project creation with given project name and interactive preferences."""
        print_color("Flutter Project CLI Generator (Interactive Preferences)", Colors.BOLD)
        
        preferences = self.get_project_preferences()
        
        output_dir = os.path.dirname(project_path)
        
        created_project_path = self.create_flutter_project(project_name, output_dir)
        
        generate_project_structure(created_project_path, preferences)
        
        create_template_files(created_project_path, preferences)
        
        update_pubspec(created_project_path, preferences)
        
        print_color(f"Flutter project '{project_name}' created successfully with the selected options.", Colors.GREEN)

    def add_file(self, file_type: str, directory: str, name: str):
        """Add a file of specified type in the given directory with a template."""
        import os
        from core.utils import to_snake_case, to_pascal_case

        valid_types = ['controller', 'view', 'service', 'model']
        if file_type not in valid_types:
            print(f"Error: Invalid file type '{file_type}'. Valid types are: {', '.join(valid_types)}")
            return

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        # Normalize name to snake_case
        snake_name = to_snake_case(name)
        
        # Strip suffix if present (e.g. auth_controller -> auth)
        suffix = f"_{file_type}"
        base_name = snake_name
        if snake_name.endswith(suffix):
            base_name = snake_name[:-len(suffix)]
        
        # File name should include suffix (e.g. auth_controller.dart)
        # But if the user provided auth_controller, base_name is auth.
        # If user provided auth, base_name is auth.
        # We want the final file to be auth_controller.dart
        
        final_file_name = f"{base_name}{suffix}"
        file_path = os.path.join(directory, f"{final_file_name}.dart")

        if os.path.exists(file_path):
            print(f"Error: File '{file_path}' already exists.")
            return

        # Template content needs the class name.
        # Class name should be PascalCase of base_name (e.g. Auth)
        # The template will append the suffix (e.g. AuthController)
        template_content = self._get_template_content(file_type, base_name)

        with open(file_path, 'w') as f:
            f.write(template_content)

        print(f"Created {file_type} file at: {file_path}")

    def generate_file(self, file_type: str, state_management: str, directory: str, name: str):
        """Generate a file with specific state management."""
        import os
        from core.utils import to_snake_case, to_pascal_case

        # Normalize file type
        if file_type == 'ctrl':
            file_type = 'controller'
        elif file_type == 'intf':
            file_type = 'interface'
        
        valid_types = ['controller', 'view', 'service', 'model', 'interface']
        if file_type not in valid_types:
            print(f"Error: Invalid file type '{file_type}'. Valid types are: {', '.join(valid_types)}")
            return

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        # Normalize name and strip suffix
        snake_name = to_snake_case(name)
        suffix = f"_{file_type}"
        base_name = snake_name
        if snake_name.endswith(suffix):
            base_name = snake_name[:-len(suffix)]
        
        final_file_name = f"{base_name}{suffix}"
        file_path = os.path.join(directory, f"{final_file_name}.dart")

        if os.path.exists(file_path):
            print(f"Error: File '{file_path}' already exists.")
            return

        template_content = self._get_specific_template_content(file_type, state_management, base_name)

        with open(file_path, 'w') as f:
            f.write(template_content)

        print(f"Created {state_management} {file_type} file at: {file_path}")

    def _get_specific_template_content(self, file_type: str, state_management: str, name: str) -> str:
        """Return template content for specific state management."""
        from core.utils import to_pascal_case
        class_name = to_pascal_case(name)

        if file_type == 'controller':
            if state_management == 'mobx':
                from templates.mobx.controller_template import get_mobx_controller_template
                return get_mobx_controller_template(class_name)
            elif state_management == 'provider':
                from templates.provider.controller_template import get_provider_controller_template
                return get_provider_controller_template(class_name)
            elif state_management == 'bloc':
                from templates.bloc.controller_template import get_bloc_controller_template
                return get_bloc_controller_template(class_name)
            elif state_management == 'getx':
                from templates.getx.controller_template import get_getx_controller_template
                return get_getx_controller_template(class_name)
            elif state_management == 'riverpod':
                from templates.riverpod.controller_template import get_riverpod_controller_template
                return get_riverpod_controller_template(class_name)
        elif file_type == 'view':
            if state_management == 'mobx':
                from templates.mobx.view_template import get_mobx_view_template
                return get_mobx_view_template(class_name)
            elif state_management == 'provider':
                from templates.provider.view_template import get_provider_view_template
                return get_provider_view_template(class_name)
            elif state_management == 'bloc':
                from templates.bloc.view_template import get_bloc_view_template
                return get_bloc_view_template(class_name)
            elif state_management == 'getx':
                from templates.getx.view_template import get_getx_view_template
                return get_getx_view_template(class_name)
            elif state_management == 'riverpod':
                from templates.riverpod.view_template import get_riverpod_view_template
                return get_riverpod_view_template(class_name)
        
        # Fallback to generic if no specific template found
        return self._get_template_content(file_type, name)

    def _get_template_content(self, file_type: str, name: str) -> str:
        """Return template content for the given file type and name."""
        from templates.generic.controller_template import get_controller_template
        from templates.generic.view_template import get_view_template
        from templates.generic.service_template import get_service_template
        from templates.generic.model_template import get_model_template
        from templates.generic.interface_template import get_interface_template
        from core.utils import to_pascal_case

        # name here is the base name (e.g. auth)
        class_name = to_pascal_case(name)

        if file_type == 'controller':
            return get_controller_template(class_name)
        elif file_type == 'view':
            return get_view_template(class_name)
        elif file_type == 'service':
            return get_service_template(class_name)
        elif file_type == 'model':
            return get_model_template(class_name)
        elif file_type == 'interface':
            return get_interface_template(class_name)
        else:
            return "// Unknown file type"
