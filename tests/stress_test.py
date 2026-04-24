import os
import shutil
import unittest
import unittest.mock
import tempfile
from fpc.generators.generator import FlutterGenerator
from fpc.config_manager import ConfigManager

class TestFPCScenarios(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def setup_fake_project(self, name):
        project_path = os.path.join(self.test_dir, name)
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, 'lib'), exist_ok=True)
        with open(os.path.join(project_path, 'pubspec.yaml'), 'w') as f:
            f.write(f"name: {name}\n")
        return project_path

    def assert_class_name(self, file_path, expected_class):
        with open(file_path, 'r') as f:
            content = f.read()
            self.assertIn(f"class {expected_class}", content, f"Class {expected_class} not found in {file_path}")

    def assert_import_consistency(self, file_path, project_name):
        with open(file_path, 'r') as f:
            content = f.read()
            # Check if any package imports match the expected project name
            if "package:" in content:
                self.assertIn(f"package:{project_name}/", content, f"Broken package import in {file_path}")

    def test_scenario_clean_arch_bloc_firebase(self):
        """Scenario 1: Clean Architecture + BLoC + Firebase (Rigid)"""
        project_name = "clean_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()
        
        preferences = {
            "architecture": "Clean Architecture",
            "state_management": "BLoC",
            "baas": "Firebase",
            "http_client": "Dio",
            "database": "None"
        }
        ConfigManager.save_config(project_path, preferences)
        
        # Generate feature
        generator.generate_file('feature', os.path.join(project_path, 'lib'), 'auth')
        
        # Rigid Validations
        repo_impl_path = os.path.join(project_path, 'lib/auth/data/repositories/auth_repository_impl.dart')
        self.assert_class_name(repo_impl_path, "AuthRepositoryImpl")
        self.assertIn("AuthRepository", open(repo_impl_path).read()) # Implements interface
        
        entity_path = os.path.join(project_path, 'lib/auth/domain/entities/auth_entity.dart')
        self.assert_class_name(entity_path, "AuthEntity")

    def test_scenario_mvvm_riverpod_hive(self):
        """Scenario 2: MVVM + Riverpod + Hive (Rigid)"""
        project_name = "mvvm_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()
        
        preferences = {
            "architecture": "MVVM",
            "state_management": "Riverpod",
            "database": "Hive",
            "http_client": "http",
            "baas": "None"
        }
        ConfigManager.save_config(project_path, preferences)
        
        # Generate viewmodel
        vm_dir = os.path.join(project_path, 'lib/viewmodels')
        generator.generate_file('viewmodel', vm_dir, 'user_profile')
        
        # Rigid Validations
        vm_path = os.path.join(vm_dir, 'user_profile_viewmodel.dart')
        self.assert_class_name(vm_path, "UserProfileViewModel")
        
        # Test naming validation
        test_path = os.path.join(project_path, 'test/viewmodels/user_profile_viewmodel_test.dart')
        self.assertTrue(os.path.exists(test_path))

    def test_scenario_mvc_getx_sqlite(self):
        """Scenario 3: MVC + GetX + SQLite (Rigid)"""
        project_name = "mvc_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()
        
        preferences = {
            "architecture": "MVC",
            "state_management": "GetX",
            "database": "SQLite (sqflite)",
            "http_client": "None",
            "baas": "None"
        }
        ConfigManager.save_config(project_path, preferences)
        
        # Generate controller
        ctrl_dir = os.path.join(project_path, 'lib/controllers')
        generator.generate_file('ctrl', ctrl_dir, 'HomeDashboard') # Testing PascalCase input
        
        # Rigid Validations
        # File should be snake_case
        ctrl_path = os.path.join(ctrl_dir, 'home_dashboard_controller.dart')
        self.assertTrue(os.path.exists(ctrl_path))
        self.assert_class_name(ctrl_path, "HomeDashboardController")

    def test_full_project_creation_scaffolding(self):
        """Scenario 4: Full Project Creation (Scaffolding) Logic"""
        project_name = "full_scaffold_app"
        project_path = os.path.join(self.test_dir, project_name)
        generator = FlutterGenerator()
        
        preferences = {
            "project_name": project_name,
            "arch": "Clean",
            "state": "BLoC",
            "http": "Dio",
            "db": "Hive",
            "baas": "Firebase",
            "structure": "Standard"
        }
        
        # We mock the shell command for 'flutter create' and pubspec updates
        with unittest.mock.patch('fpc.generators.generator.ProjectManager.create_project', return_value=project_path), \
             unittest.mock.patch('fpc.generators.generator.update_pubspec'), \
             unittest.mock.patch('fpc.generators.generator.ProjectManager.run_build_runner'):
             
            # Manually create the folder and pubspec that flutter create would make
            os.makedirs(os.path.join(project_path, 'lib'), exist_ok=True)
            with open(os.path.join(project_path, 'pubspec.yaml'), 'w') as f:
                f.write(f"name: {project_name}\n")
            
            # Run FPC internal scaffolding
            generator.run_with_name_interactive(project_name, project_path, headless_args=preferences)
            
            # 1. Verify Folder Skeleton (Inside 'app' folder)
            self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/core/error')))
            self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/config')))
            
            # 2. Verify Config File
            config_path = os.path.join(project_path, '.fpc.json')
            self.assertTrue(os.path.exists(config_path))
            
            # 3. Verify main.dart content
            main_path = os.path.join(project_path, 'lib/main.dart')
            self.assertTrue(os.path.exists(main_path))
            main_content = open(main_path).read()
            self.assertIn("sl.init()", main_content) # Should have DI for Clean Arch
            
            # 4. Verify core templates
            failure_path = os.path.join(project_path, 'lib/app/core/error/failures.dart')
            self.assertTrue(os.path.exists(failure_path))
            self.assertIn("abstract class Failure", open(failure_path).read())


if __name__ == "__main__":
    unittest.main()
