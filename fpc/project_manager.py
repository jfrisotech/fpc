import subprocess
import sys
import os
from typing import List, Optional
from .core.utils import print_color, Colors
from rich.console import Console

class ProjectManager:
    """Handles Flutter-specific project operations."""
    
    def __init__(self):
        self.console = Console()

    def run_flutter_command(self, project_path: str, command_args: List[str], status_message: str = None) -> bool:
        """Execute a generic Flutter command."""
        if not status_message:
            status_message = f"Running 'flutter {' '.join(command_args)}'..."
            
        try:
            with self.console.status(f"[bold blue]{status_message}[/bold blue]", spinner="dots"):
                result = subprocess.run(
                    ['flutter'] + command_args,
                    cwd=project_path,
                    check=True,
                    capture_output=True,
                    text=True
                )
            return True
        except subprocess.CalledProcessError as e:
            print_color(f"Error running flutter command: {e.stderr}", Colors.RED)
            return False
        except FileNotFoundError:
            print_color("Flutter command not found. Make sure Flutter is installed and in your PATH.", Colors.RED)
            return False

    def create_project(self, project_name: str, output_dir: str) -> Optional[str]:
        """Create a base Flutter project."""
        project_path = os.path.join(output_dir, project_name)
        success = self.run_flutter_command(
            output_dir, 
            ['create', '--project-name', project_name, project_name],
            f"Creating base Flutter project '{project_name}'..."
        )
        return project_path if success else None

    def run_build_runner(self, project_path: str) -> bool:
        """Run build_runner build."""
        print_color("Running build_runner...", Colors.BLUE)
        return self.run_flutter_command(
            project_path, 
            ['pub', 'run', 'build_runner', 'build', '--delete-conflicting-outputs'],
            "Generating files with build_runner..."
        )

    def add_dependencies(self, project_path: str, dependencies: List[str], dev: bool = False) -> bool:
        """Add dependencies using flutter pub add."""
        if not dependencies:
            return True
            
        cmd_args = ['pub', 'add']
        if dev:
            cmd_args.append('--dev')
        cmd_args.extend(dependencies)
        
        return self.run_flutter_command(
            project_path, 
            cmd_args,
            f"Adding {'dev ' if dev else ''}dependencies..."
        )
