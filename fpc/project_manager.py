import subprocess
import sys
import os
import shutil
from typing import List, Optional
from .core.utils import print_color, Colors
from rich.console import Console


def _find_flutter() -> str:
    """Resolve the flutter binary, checking common macOS/Linux install locations."""
    # 1. Check PATH via shutil.which (works in most cases)
    found = shutil.which('flutter')
    if found:
        return found
    # 2. Common manual install locations
    candidates = [
        os.path.expanduser('~/development/flutter/bin/flutter'),
        os.path.expanduser('~/flutter/bin/flutter'),
        '/usr/local/bin/flutter',
        '/opt/homebrew/bin/flutter',
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return 'flutter'  # fall back — will raise FileNotFoundError with a clear message


def _flutter_env() -> dict:
    """Return os.environ extended with Flutter and Dart SDK in PATH."""
    flutter_bin = _find_flutter()
    flutter_bin_dir = os.path.dirname(os.path.abspath(flutter_bin))
    # Flutter ships its own Dart SDK at flutter/bin/cache/dart-sdk/bin
    flutter_root = os.path.dirname(flutter_bin_dir)  # parent of bin/
    dart_sdk_bin = os.path.join(flutter_root, 'bin', 'cache', 'dart-sdk', 'bin')

    env = os.environ.copy()
    extra = [flutter_bin_dir]
    if os.path.isdir(dart_sdk_bin):
        extra.append(dart_sdk_bin)
    for p in reversed(extra):
        if p not in env.get('PATH', ''):
            env['PATH'] = p + os.pathsep + env.get('PATH', '')
    return env


class ProjectManager:
    """Handles Flutter-specific project operations."""
    
    def __init__(self):
        self.console = Console()

    def run_flutter_command(self, project_path: str, command_args: List[str], status_message: str = None) -> bool:
        """Execute a generic Flutter command."""
        if not status_message:
            status_message = f"Running 'flutter {' '.join(command_args)}'..."

        flutter_bin = _find_flutter()
        env = _flutter_env()

        try:
            with self.console.status(f"[bold blue]{status_message}[/bold blue]", spinner="dots"):
                subprocess.run(
                    [flutter_bin] + command_args,
                    cwd=project_path,
                    check=True,
                    capture_output=True,
                    text=True,
                    env=env,
                )
            return True
        except subprocess.CalledProcessError as e:
            print_color(f"Error running flutter command: {e.stderr}", Colors.RED)
            return False
        except FileNotFoundError:
            print_color(f"Flutter not found at '{flutter_bin}'. Make sure Flutter is installed and in your PATH.", Colors.RED)
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
