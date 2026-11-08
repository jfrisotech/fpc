#!/usr/bin/env python3
"""
FPC Git Hooks Installer
Configures Git to use versioned hooks located in .githooks/
Usage: python3 scripts/install_git_hooks.py
"""

import os
import subprocess
import sys

def install_hooks():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hooks_dir = os.path.join(repo_root, '.githooks')
    
    if not os.path.isdir(hooks_dir):
        print(f"❌ Error: .githooks directory not found at {hooks_dir}")
        sys.exit(1)

    try:
        # Configure git to point to .githooks directory
        subprocess.run(['git', 'config', 'core.hooksPath', '.githooks'], cwd=repo_root, check=True)
        
        # Ensure executable permissions on unix-like systems
        pre_commit_file = os.path.join(hooks_dir, 'pre-commit')
        if os.path.exists(pre_commit_file) and hasattr(os, 'chmod'):
            os.chmod(pre_commit_file, 0o755)

        print("✅ Git hooks installed successfully! Commits will now automatically validate with pytest.")
    except Exception as e:
        print(f"❌ Failed to configure git hooks: {e}")
        sys.exit(1)

if __name__ == '__main__':
    install_hooks()

