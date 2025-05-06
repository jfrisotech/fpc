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
