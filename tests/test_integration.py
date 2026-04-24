import os
import pytest
from fpc.generators.generator import FlutterGenerator
from fpc.config_manager import ConfigManager

def test_full_generation_flow(tmp_path):
    """Integration test: init project and generate a feature."""
    # 1. Setup a fake flutter project root
    project_root = tmp_path / "my_app"
    project_root.mkdir()
    (project_root / "pubspec.yaml").write_text("name: my_app")
    
    lib_dir = project_root / "lib"
    lib_dir.mkdir()
    
    # 2. Initialize FPC
    generator = FlutterGenerator()
    preferences = {
        "architecture": "MVC",
        "state_management": "Provider",
        "http_client": "Dio",
        "database": "None",
        "baas": "None",
        "structure": "standard"
    }
    ConfigManager.save_config(str(project_root), preferences)
    
    assert os.path.exists(os.path.join(str(project_root), ".fpc.json"))
    
    # 3. Generate a feature
    # We need to be inside the project or pass the directory
    feature_parent_dir = str(lib_dir)
    generator.generate_file('feature', feature_parent_dir, 'auth')
    
    # 4. Verify physical structure
    auth_dir = lib_dir / "auth"
    assert auth_dir.exists()
    assert (auth_dir / "controllers").exists()
    assert (auth_dir / "views").exists()
    assert (auth_dir / "controllers" / "auth_controller.dart").exists()
    
    # 5. Verify physical tests structure
    test_dir = project_root / "test" / "auth"
    assert test_dir.exists()
    assert (test_dir / "controllers" / "auth_controller_test.dart").exists()
    
    # 6. Verify content of generated test
    test_content = (test_dir / "controllers" / "auth_controller_test.dart").read_text()
    assert "AuthController Unit Tests" in test_content
    assert "void main()" in test_content
