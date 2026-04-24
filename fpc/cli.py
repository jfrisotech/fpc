#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from rich.console import Console
from rich.table import Table

# Add the current directory to sys.path so we can find the fpc package
# This is mainly for development. In production, fpc should be installed.
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from fpc.generators.generator import FlutterGenerator
from fpc.config_manager import ConfigManager
from fpc.core.utils import print_color, Colors

def main():
    console = Console()
    parser = argparse.ArgumentParser(description="FPC CLI - Flutter Project Companion")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # create command
    create_parser = subparsers.add_parser('create', help='Create a new Flutter project')
    create_parser.add_argument('-n', '--name', required=True, help='Project name')
    create_parser.add_argument('-p', '--path', default=os.getcwd(), help='Output directory path')
    create_parser.add_argument('--arch', choices=['mvc', 'mvvm', 'clean'], help='Architecture pattern')
    create_parser.add_argument('--state', choices=['provider', 'bloc', 'getx', 'riverpod', 'mobx', 'none'], help='State management')
    create_parser.add_argument('--http', choices=['dio', 'http', 'none'], help='HTTP Client')
    create_parser.add_argument('--db', choices=['sqlite', 'hive', 'isar', 'objectbox', 'none'], help='Local database')
    create_parser.add_argument('--baas', choices=['firebase', 'supabase', 'appwrite', 'none'], help='Backend as a Service')
    create_parser.add_argument('--structure', choices=['standard', 'modular'], help='Folder structure pattern')

    # init command
    init_parser = subparsers.add_parser('init', help='Initialize FPC in an existing project')

    # config command
    config_parser = subparsers.add_parser('config', help='Show or modify project configuration')
    config_parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'), help='Set a configuration value')

    # add command (legacy/simple)
    add_parser = subparsers.add_parser('add', help='Add files to an existing project')
    add_parser.add_argument('-t', '--type', required=True, choices=['controller', 'view', 'service', 'model'], help='Type of file to add')
    add_parser.add_argument('-d', '--directory', required=True, help='Target directory path')
    add_parser.add_argument('-n', '--name', required=True, help='Name of the file to add')

    # gen command
    gen_parser = subparsers.add_parser('gen', help='Generate a file with specific state management')
    gen_parser.add_argument('type', choices=['controller', 'ctrl', 'view', 'model', 'service', 'interface', 'intf', 'feature'], help='Type of file to generate')
    gen_parser.add_argument('path', help='Path to the file (including name)')
    gen_parser.add_argument('-s', '--state', help='State management solution (overrides project default)')
    
    # aliases for flutter commands
    subparsers.add_parser('get', help='Alias for flutter pub get')
    subparsers.add_parser('build', help='Alias for build_runner build')
    subparsers.add_parser('watch', help='Alias for build_runner watch')
    subparsers.add_parser('clean', help='Alias for flutter clean')
    subparsers.add_parser('upgrade', help='Alias for flutter pub upgrade')
    
    # run command
    run_parser = subparsers.add_parser('run', help='Run a script from pubspec.yaml')
    run_parser.add_argument('script', help='Script name to run')

    # doctor command
    subparsers.add_parser('doctor', help='Check the health of your development environment')

    args = parser.parse_args()
    generator = FlutterGenerator()

    if args.command == 'create':
        output_path = os.path.abspath(args.path)
        project_path = os.path.join(output_path, args.name)
        headless_args = {
            'arch': args.arch,
            'state': args.state,
            'http': args.http,
            'db': args.db,
            'baas': args.baas,
            'structure': args.structure
        }
        generator.run_with_name_interactive(args.name, project_path, headless_args)

    elif args.command == 'init':
        project_root = ConfigManager.find_project_root()
        if not project_root:
            console.print("[red]Error: Could not find project root (no pubspec.yaml found).[/red]")
            return
        
        if ConfigManager.is_fpc_initialized(project_root):
            console.print("[yellow]FPC is already initialized in this project.[/yellow]")
            return
            
        console.print(f"[bold blue]Initializing FPC in {project_root}...[/bold blue]")
        preferences = generator.get_project_preferences()
        ConfigManager.save_config(project_root, preferences)
        console.print("[green]FPC initialized successfully![/green]")

    elif args.command == 'config':
        project_root = ConfigManager.find_project_root()
        if not project_root:
            console.print("[red]Error: Project root not found.[/red]")
            return
            
        config = ConfigManager.get_config(project_root)
        
        if args.set:
            key, value = args.set
            config[key] = value
            ConfigManager.save_config(project_root, config)
            console.print(f"[green]Config updated: {key} = {value}[/green]")
        else:
            if not config:
                console.print("[yellow]No FPC configuration found. Run 'fpc init' first.[/yellow]")
                return
            
            table = Table(title=f"FPC Configuration ({project_root})")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="magenta")
            for k, v in config.items():
                table.add_row(k, str(v))
            console.print(table)

    elif args.command == 'add':
        generator.add_file(args.type, args.directory, args.name)

    elif args.command == 'gen':
        full_path = args.path
        directory = os.path.dirname(full_path) or os.getcwd()
        name = os.path.basename(full_path)
        generator.generate_file(args.type, directory, name, state_management=args.state)

    elif args.command == 'get':
        project_root = ConfigManager.find_project_root()
        if project_root:
            generator.project_manager.run_flutter_command(project_root, ['pub', 'get'], "Fetching dependencies...")
        else:
            console.print("[red]Error: Project root not found.[/red]")

    elif args.command == 'build':
        project_root = ConfigManager.find_project_root()
        if project_root:
            generator.project_manager.run_build_runner(project_root)
        else:
            console.print("[red]Error: Project root not found.[/red]")

    elif args.command == 'watch':
        project_root = ConfigManager.find_project_root()
        if project_root:
            generator.project_manager.run_flutter_command(project_root, ['pub', 'run', 'build_runner', 'watch', '--delete-conflicting-outputs'], "Watching for changes...")
        else:
            console.print("[red]Error: Project root not found.[/red]")

    elif args.command == 'clean':
        project_root = ConfigManager.find_project_root()
        if project_root:
            generator.project_manager.run_flutter_command(project_root, ['clean'], "Cleaning project...")
        else:
            console.print("[red]Error: Project root not found.[/red]")

    elif args.command == 'upgrade':
        project_root = ConfigManager.find_project_root()
        if project_root:
            generator.project_manager.run_flutter_command(project_root, ['pub', 'upgrade'], "Upgrading dependencies...")
        else:
            console.print("[red]Error: Project root not found.[/red]")

    elif args.command == 'run':
        generator.run_pubspec_script(args.script, os.getcwd())

    elif args.command == 'doctor':
        from fpc.doctor import Doctor
        Doctor().run()

    elif args.command is None:
        parser.print_help()

if __name__ == "__main__":
    main()
