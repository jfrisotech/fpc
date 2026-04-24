import os
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from fpc.config_manager import ConfigManager

class Doctor:
    def __init__(self):
        self.console = Console()

    def run(self):
        self.console.print(Panel("[bold blue]FPC Doctor - Environment Health Check[/bold blue]"))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Details")

        # 1. Check Python
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        table.add_row(
            "Python", 
            "[green]OK[/green]", 
            f"Version {py_version}"
        )

        # 2. Check Flutter
        flutter_status, flutter_detail = self._check_command(['flutter', '--version'])
        table.add_row("Flutter", flutter_status, flutter_detail)

        # 3. Check Git
        git_status, git_detail = self._check_command(['git', '--version'])
        table.add_row("Git", git_status, git_detail)

        # 4. Check FPC Initialization
        project_root = ConfigManager.find_project_root()
        if project_root:
            if ConfigManager.is_fpc_initialized(project_root):
                fpc_status = "[green]Initialized[/green]"
                config = ConfigManager.get_config(project_root)
                fpc_detail = f"Project: {project_root}\nArch: {config.get('architecture')}"
            else:
                fpc_status = "[yellow]Not Initialized[/yellow]"
                fpc_detail = "Run 'fpc init' to enable FPC features"
        else:
            fpc_status = "[red]No Project[/red]"
            fpc_detail = "Not inside a Flutter project"
        
        table.add_row("FPC Project", fpc_status, fpc_detail)

        self.console.print(table)
        
        if "[red]" in str(table) or "[yellow]" in str(table):
            self.console.print("\n[bold yellow]Suggestions:[/bold yellow]")
            if "[red]Missing[/red]" in str(table):
                self.console.print("- Install missing tools and add them to your PATH.")
            if "[yellow]Not Initialized[/yellow]" in str(table):
                self.console.print("- Run [bold cyan]fpc init[/bold cyan] in your project root.")
        else:
            self.console.print("\n[bold green]Everything looks good! Happy coding! 🚀[/bold green]")

    def _check_command(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return "[green]OK[/green]", result.stdout.split('\n')[0]
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "[red]Missing[/red]", "Command not found or failed"
