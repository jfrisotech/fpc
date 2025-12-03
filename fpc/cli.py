#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generators.generator import FlutterGenerator

def main():
    parser = argparse.ArgumentParser(
        description="FPC CLI"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # create command
    create_parser = subparsers.add_parser('create', help='Create a new Flutter project')
    create_parser.add_argument('-n', '--name', required=True, help='Project name')
    create_parser.add_argument('-p', '--path', default=os.getcwd(), help='Output directory path')

    # add command
    add_parser = subparsers.add_parser('add', help='Add files to an existing project')
    add_parser.add_argument('-t', '--type', required=True, choices=[
        'controller',
        'view',
        'service',
        'model',
    ], help='Type of file to add')
    add_parser.add_argument('-d', '--directory', required=True, help='Target directory path')
    add_parser.add_argument('-n', '--name', required=True, help='Name of the file to add (without extension)')

    # help command
    help_parser = subparsers.add_parser('help', help='Show help information')

    # gen command
    gen_parser = subparsers.add_parser('gen', help='Generate a file with specific state management')
    gen_parser.add_argument('type', choices=['controller', 'ctrl', 'view', 'model', 'service', 'interface', 'intf'], help='Type of file to generate')
    gen_parser.add_argument('state_management', choices=['mobx', 'provider', 'bloc', 'getx', 'riverpod', 'none'], help='State management solution')
    gen_parser.add_argument('path', help='Path to the file (including name)')

    args = parser.parse_args()

    generator = FlutterGenerator()

    if args.command == 'create':
        output_path = os.path.abspath(args.path)
        project_path = os.path.join(output_path, args.name)
        generator.run_with_name_interactive(args.name, project_path)
    elif args.command == 'add':
        # Call a new method to add files based on type, directory, and name
        generator.add_file(args.type, args.directory, args.name)
    elif args.command == 'gen':
        # Parse path to separate directory and filename
        full_path = args.path
        directory = os.path.dirname(full_path)
        name = os.path.basename(full_path)
        
        # If directory is empty, use current directory
        if not directory:
            directory = os.getcwd()
            
        generator.generate_file(args.type, args.state_management, directory, name)
    elif args.command == 'help' or args.command is None:
        parser.print_help()
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()

if __name__ == "__main__":
    main()
