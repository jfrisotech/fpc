import os
import json
from typing import Optional, Dict, Any
from .core.utils import print_color, Colors

class ConfigManager:
    """Manages .fpc.json configuration files."""
    
    CONFIG_NAME = '.fpc.json'

    @staticmethod
    def find_project_root(start_dir: str = None) -> Optional[str]:
        """Find the root directory of the project (containing pubspec.yaml)."""
        d = os.path.abspath(start_dir or os.getcwd())
        while True:
            if os.path.exists(os.path.join(d, 'pubspec.yaml')):
                return d
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
        return None

    @classmethod
    def get_config(cls, current_dir: str = None) -> Dict[str, Any]:
        """Finds .fpc.json traversing up from current_dir."""
        d = os.path.abspath(current_dir or os.getcwd())
        while True:
            p = os.path.join(d, cls.CONFIG_NAME)
            if os.path.exists(p):
                try:
                    with open(p, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    print_color(f"Error reading {cls.CONFIG_NAME}: {e}", Colors.RED)
                    pass
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
        return {}

    @classmethod
    def save_config(cls, project_path: str, preferences: Dict[str, Any]):
        """Saves preferences to .fpc.json in project_path."""
        config_path = os.path.join(project_path, cls.CONFIG_NAME)
        try:
            with open(config_path, 'w') as f:
                json.dump(preferences, f, indent=2)
            return True
        except Exception as e:
            print_color(f"Failed to save {cls.CONFIG_NAME}: {e}", Colors.YELLOW)
            return False

    @classmethod
    def is_fpc_initialized(cls, project_path: str) -> bool:
        """Checks if FPC is initialized in the project path."""
        return os.path.exists(os.path.join(project_path, cls.CONFIG_NAME))
