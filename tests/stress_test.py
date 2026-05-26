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

    # ──────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────

    def setup_fake_project(self, name):
        """Create a minimal fake Flutter project directory."""
        project_path = os.path.join(self.test_dir, name)
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, 'lib'), exist_ok=True)
        with open(os.path.join(project_path, 'pubspec.yaml'), 'w') as f:
            f.write(f"name: {name}\n")
        return project_path

    def assert_class_name(self, file_path, expected_class):
        """Assert that a Dart file contains a specific class declaration."""
        self.assertTrue(os.path.exists(file_path), f"File not found: {file_path}")
        with open(file_path, 'r') as f:
            content = f.read()
        self.assertIn(
            f"class {expected_class}", content,
            f"Class '{expected_class}' not found in {file_path}"
        )

    def run_full_scaffold(self, project_name, headless_args):
        """Run full scaffolding with flutter create mocked."""
        project_path = os.path.join(self.test_dir, project_name)
        generator = FlutterGenerator()

        with unittest.mock.patch('fpc.generators.generator.ProjectManager.create_project', return_value=project_path), \
             unittest.mock.patch('fpc.generators.generator.update_pubspec'), \
             unittest.mock.patch('fpc.generators.generator.ProjectManager.run_build_runner'):

            os.makedirs(os.path.join(project_path, 'lib'), exist_ok=True)
            with open(os.path.join(project_path, 'pubspec.yaml'), 'w') as f:
                f.write(f"name: {project_name}\n")

            generator.run_with_name_interactive(project_name, project_path, headless_args=headless_args)

        return project_path

    # ──────────────────────────────────────────────────────────
    # Original 4 scenarios (kept intact)
    # ──────────────────────────────────────────────────────────

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

        generator.generate_file('feature', os.path.join(project_path, 'lib'), 'auth')

        repo_impl_path = os.path.join(project_path, 'lib/auth/data/repositories/auth_repository_impl.dart')
        self.assert_class_name(repo_impl_path, "AuthRepositoryImpl")
        self.assertIn("AuthRepository", open(repo_impl_path).read())

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

        vm_dir = os.path.join(project_path, 'lib/viewmodels')
        generator.generate_file('viewmodel', vm_dir, 'user_profile')

        vm_path = os.path.join(vm_dir, 'user_profile_viewmodel.dart')
        self.assert_class_name(vm_path, "UserProfileViewModel")

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

        ctrl_dir = os.path.join(project_path, 'lib/controllers')
        generator.generate_file('ctrl', ctrl_dir, 'HomeDashboard')  # Testing PascalCase input

        ctrl_path = os.path.join(ctrl_dir, 'home_dashboard_controller.dart')
        self.assertTrue(os.path.exists(ctrl_path))
        self.assert_class_name(ctrl_path, "HomeDashboardController")

    def test_full_project_creation_scaffolding(self):
        """Scenario 4: Full Project Creation (Scaffolding) Logic — Clean + BLoC + Standard"""
        project_path = self.run_full_scaffold("full_scaffold_app", {
            "arch": "Clean", "state": "BLoC", "http": "Dio",
            "db": "Hive", "baas": "Firebase", "structure": "Standard"
        })

        # Folder skeleton
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/core/error')))
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/config')))

        # Config file
        self.assertTrue(os.path.exists(os.path.join(project_path, '.fpc.json')))

        # main.dart has DI init for Clean Arch
        main_content = open(os.path.join(project_path, 'lib/main.dart')).read()
        self.assertIn("sl.init()", main_content)

        # Core template
        failure_path = os.path.join(project_path, 'lib/app/core/error/failures.dart')
        self.assertTrue(os.path.exists(failure_path))
        self.assertIn("abstract class Failure", open(failure_path).read())

    # ──────────────────────────────────────────────────────────
    # Phase 2 — Missing state management options
    # ──────────────────────────────────────────────────────────

    def test_scenario_mvc_provider(self):
        """Phase 2, Scenario 5: MVC + Provider — all Provider paths covered."""
        project_name = "mvc_provider_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()

        preferences = {
            "architecture": "MVC (Model-View-Controller)",
            "state_management": "Provider",
            "database": "None",
            "http_client": "None",
            "baas": "None",
            "folder_structure": "Standard (Layer First)",
        }
        ConfigManager.save_config(project_path, preferences)

        # Controller
        ctrl_dir = os.path.join(project_path, 'lib/controllers')
        generator.generate_file('controller', ctrl_dir, 'settings')
        ctrl_path = os.path.join(ctrl_dir, 'settings_controller.dart')
        self.assertTrue(os.path.exists(ctrl_path), "Controller not created for MVC+Provider")
        self.assert_class_name(ctrl_path, "SettingsController")

        # View (Provider branch in view_template)
        view_dir = os.path.join(project_path, 'lib/views')
        generator.generate_file('view', view_dir, 'settings')
        view_path = os.path.join(view_dir, 'settings_view.dart')
        self.assertTrue(os.path.exists(view_path), "View not created for MVC+Provider")

    def test_scenario_mvvm_mobx(self):
        """Phase 2, Scenario 6: MVVM + MobX — verifies MobX template path."""
        project_name = "mvvm_mobx_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()

        preferences = {
            "architecture": "MVVM (Model-View-ViewModel)",
            "state_management": "MobX",
            "database": "None",
            "http_client": "None",
            "baas": "None",
            "folder_structure": "Standard (Layer First)",
        }
        ConfigManager.save_config(project_path, preferences)

        vm_dir = os.path.join(project_path, 'lib/viewmodels')
        generator.generate_file('viewmodel', vm_dir, 'counter')
        vm_path = os.path.join(vm_dir, 'counter_viewmodel.dart')
        self.assertTrue(os.path.exists(vm_path), "ViewModel not created for MVVM+MobX")
        self.assert_class_name(vm_path, "CounterViewModel")

        # MobX view
        view_dir = os.path.join(project_path, 'lib/views')
        generator.generate_file('view', view_dir, 'counter')
        self.assertTrue(os.path.exists(os.path.join(view_dir, 'counter_view.dart')))

    def test_scenario_mvc_no_state_management(self):
        """Phase 2, Scenario 7: MVC + None — no state management must not crash."""
        project_name = "mvc_none_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()

        preferences = {
            "architecture": "MVC (Model-View-Controller)",
            "state_management": "None",
            "database": "None",
            "http_client": "None",
            "baas": "None",
            "folder_structure": "Standard (Layer First)",
        }
        ConfigManager.save_config(project_path, preferences)

        ctrl_dir = os.path.join(project_path, 'lib/controllers')
        generator.generate_file('controller', ctrl_dir, 'product')
        ctrl_path = os.path.join(ctrl_dir, 'product_controller.dart')
        self.assertTrue(os.path.exists(ctrl_path), "Controller not created for MVC+None")
        self.assert_class_name(ctrl_path, "ProductController")

        view_dir = os.path.join(project_path, 'lib/views')
        generator.generate_file('view', view_dir, 'product')
        self.assertTrue(os.path.exists(os.path.join(view_dir, 'product_view.dart')))

    def test_scenario_mvvm_bloc_standard(self):
        """Phase 2, Scenario 8: MVVM + BLoC (Standard) — BLoC ViewModel generation."""
        project_name = "mvvm_bloc_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()

        preferences = {
            "architecture": "MVVM (Model-View-ViewModel)",
            "state_management": "BLoC",
            "database": "None",
            "http_client": "Dio",
            "baas": "None",
            "folder_structure": "Standard (Layer First)",
        }
        ConfigManager.save_config(project_path, preferences)

        vm_dir = os.path.join(project_path, 'lib/viewmodels')
        generator.generate_file('viewmodel', vm_dir, 'login')
        vm_path = os.path.join(vm_dir, 'login_viewmodel.dart')
        self.assertTrue(os.path.exists(vm_path), "ViewModel not created for MVVM+BLoC")
        self.assert_class_name(vm_path, "LoginViewModel")

    def test_scenario_clean_no_state(self):
        """Phase 2, Scenario 9: Clean Architecture + None state — feature generation."""
        project_name = "clean_none_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()

        preferences = {
            "architecture": "Clean Architecture",
            "state_management": "None",
            "database": "None",
            "http_client": "None",
            "baas": "None",
            "folder_structure": "Standard (Layer First)",
        }
        ConfigManager.save_config(project_path, preferences)

        generator.generate_file('feature', os.path.join(project_path, 'lib'), 'profile')

        repo_path = os.path.join(project_path, 'lib/profile/data/repositories/profile_repository_impl.dart')
        self.assertTrue(os.path.exists(repo_path), "RepositoryImpl not created for Clean+None")
        self.assert_class_name(repo_path, "ProfileRepositoryImpl")

        entity_path = os.path.join(project_path, 'lib/profile/domain/entities/profile_entity.dart')
        self.assertTrue(os.path.exists(entity_path), "Entity not created for Clean+None")

    # ──────────────────────────────────────────────────────────
    # Phase 3 — Modular (Feature First) structure coverage
    # ──────────────────────────────────────────────────────────

    def test_scenario_clean_bloc_modular(self):
        """Phase 3, Scenario 10: Clean Architecture + BLoC + Modular."""
        project_path = self.run_full_scaffold("clean_bloc_mod_app", {
            "arch": "Clean", "state": "BLoC", "http": "Dio",
            "db": "none", "baas": "none", "structure": "Modular",
        })

        # Feature modules under lib/app/modules/
        modules_path = os.path.join(project_path, 'lib/app/modules/auth')
        self.assertTrue(os.path.isdir(modules_path), "Modular auth module not created for Clean+BLoC")

        # Clean arch subfolders
        self.assertTrue(os.path.isdir(os.path.join(modules_path, 'data')))
        self.assertTrue(os.path.isdir(os.path.join(modules_path, 'domain')))

        # BLoC-specific presentation folder
        bloc_dir = os.path.join(modules_path, 'presentation', 'bloc')
        self.assertTrue(os.path.isdir(bloc_dir), "BLoC presentation folder not created")

        # Global core still in lib/app
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/core/error/failures.dart')))

        # Config file saved
        self.assertTrue(os.path.exists(os.path.join(project_path, '.fpc.json')))

    def test_scenario_mvc_getx_modular(self):
        """Phase 3, Scenario 11: MVC + GetX + Modular — auth module with controllers/views."""
        project_path = self.run_full_scaffold("mvc_getx_mod_app", {
            "arch": "MVC", "state": "GetX", "http": "none",
            "db": "none", "baas": "none", "structure": "Modular",
        })

        auth_module = os.path.join(project_path, 'lib/app/modules/auth')
        self.assertTrue(os.path.isdir(auth_module), "Modular auth module not created for MVC+GetX")

        # MVC dirs inside auth module
        self.assertTrue(os.path.isdir(os.path.join(auth_module, 'controllers')))
        self.assertTrue(os.path.isdir(os.path.join(auth_module, 'views')))
        self.assertTrue(os.path.isdir(os.path.join(auth_module, 'models')))

        # GetX controller file and class
        ctrl_file = os.path.join(auth_module, 'controllers', 'auth_controller.dart')
        self.assertTrue(os.path.exists(ctrl_file), "auth_controller.dart not created for GetX/MVC/Modular")
        self.assert_class_name(ctrl_file, "AuthController")

    def test_scenario_mvvm_riverpod_modular(self):
        """Phase 3, Scenario 12: MVVM + Riverpod + Modular — verifies ProviderScope in main."""
        project_path = self.run_full_scaffold("mvvm_rp_mod_app", {
            "arch": "MVVM", "state": "Riverpod", "http": "Dio",
            "db": "none", "baas": "none", "structure": "Modular",
        })

        auth_module = os.path.join(project_path, 'lib/app/modules/auth')
        self.assertTrue(os.path.isdir(auth_module), "Modular auth module not created for MVVM+Riverpod")

        # MVVM dirs
        self.assertTrue(os.path.isdir(os.path.join(auth_module, 'viewmodels')))
        self.assertTrue(os.path.isdir(os.path.join(auth_module, 'views')))
        self.assertTrue(os.path.isdir(os.path.join(auth_module, 'models')))

        # Riverpod: main.dart must wrap app in ProviderScope
        main_path = os.path.join(project_path, 'lib/main.dart')
        main_content = open(main_path).read()
        self.assertIn("ProviderScope", main_content,
                      "main.dart missing ProviderScope for Riverpod")
        self.assertIn("package:flutter_riverpod/flutter_riverpod.dart", main_content,
                      "main.dart missing flutter_riverpod import")

    # ──────────────────────────────────────────────────────────
    # Phase 4 — Database options: Isar and ObjectBox
    # ──────────────────────────────────────────────────────────

    def test_scenario_clean_bloc_isar(self):
        """Phase 4, Scenario 13: Clean Architecture + BLoC + Isar."""
        project_path = self.run_full_scaffold("clean_bloc_isar_app", {
            "arch": "Clean", "state": "BLoC", "http": "Dio",
            "db": "isar", "baas": "none", "structure": "Standard",
        })
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/core/error/failures.dart')))
        import json
        config = json.load(open(os.path.join(project_path, '.fpc.json')))
        self.assertEqual(config.get('database'), 'Isar', "Config must record Isar")

    def test_scenario_mvc_getx_objectbox(self):
        """Phase 4, Scenario 14: MVC + GetX + ObjectBox."""
        project_path = self.run_full_scaffold("mvc_getx_objectbox_app", {
            "arch": "MVC", "state": "GetX", "http": "none",
            "db": "objectbox", "baas": "none", "structure": "Standard",
        })
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/main.dart')))
        import json
        config = json.load(open(os.path.join(project_path, '.fpc.json')))
        self.assertEqual(config.get('database'), 'ObjectBox', "Config must record ObjectBox")

    # ──────────────────────────────────────────────────────────
    # Phase 4 — BaaS options: Firebase main.dart, Supabase, Appwrite
    # ──────────────────────────────────────────────────────────

    def test_scenario_clean_bloc_firebase_main_content(self):
        """Phase 4, Scenario 15: Firebase — validates Firebase.initializeApp in main.dart."""
        project_path = self.run_full_scaffold("clean_bloc_firebase_main_app", {
            "arch": "Clean", "state": "BLoC", "http": "Dio",
            "db": "none", "baas": "firebase", "structure": "Standard",
        })
        main_content = open(os.path.join(project_path, 'lib/main.dart')).read()
        self.assertIn("firebase_core", main_content, "main.dart missing firebase_core import")
        self.assertIn("Firebase.initializeApp", main_content, "main.dart missing Firebase.initializeApp()")

    def test_scenario_mvvm_bloc_supabase(self):
        """Phase 4, Scenario 16: MVVM + BLoC + Supabase — Supabase init in main.dart and app_config.dart."""
        project_path = self.run_full_scaffold("mvvm_bloc_supabase_app", {
            "arch": "MVVM", "state": "BLoC", "http": "Dio",
            "db": "none", "baas": "supabase", "structure": "Standard",
        })
        main_content = open(os.path.join(project_path, 'lib/main.dart')).read()
        self.assertIn("supabase_flutter", main_content, "main.dart missing supabase_flutter import")
        self.assertIn("Supabase.initialize", main_content, "main.dart missing Supabase.initialize()")
        self.assertIn("app_config.dart", main_content, "main.dart missing app_config.dart import")

        config_file = os.path.join(project_path, 'lib/app/config/app_config.dart')
        self.assertTrue(os.path.exists(config_file), "app_config.dart not generated for Supabase")
        config_content = open(config_file).read()
        self.assertIn("supabaseUrl", config_content,     "app_config.dart missing supabaseUrl")
        self.assertIn("supabaseAnonKey", config_content, "app_config.dart missing supabaseAnonKey")

    def test_scenario_clean_riverpod_appwrite(self):
        """Phase 4, Scenario 17: Clean + Riverpod + Appwrite — Appwrite Client in main.dart and app_config.dart."""
        project_path = self.run_full_scaffold("clean_rp_appwrite_app", {
            "arch": "Clean", "state": "Riverpod", "http": "Dio",
            "db": "none", "baas": "appwrite", "structure": "Standard",
        })
        main_content = open(os.path.join(project_path, 'lib/main.dart')).read()
        self.assertIn("appwrite", main_content, "main.dart missing appwrite import")
        self.assertIn("Client()", main_content, "main.dart missing Appwrite Client() instantiation")

        config_file = os.path.join(project_path, 'lib/app/config/app_config.dart')
        self.assertTrue(os.path.exists(config_file), "app_config.dart not generated for Appwrite")
        config_content = open(config_file).read()
        self.assertIn("appwriteEndpoint", config_content,  "app_config.dart missing appwriteEndpoint")
        self.assertIn("appwriteProjectId", config_content, "app_config.dart missing appwriteProjectId")

    def test_scenario_full_mvvm_mobx_objectbox_appwrite(self):
        """Phase 4, Scenario 18: Full combination — MVVM + MobX + ObjectBox + Appwrite (maximum complexity)."""
        project_path = self.run_full_scaffold("mvvm_mobx_objectbox_appwrite_app", {
            "arch": "MVVM", "state": "MobX", "http": "Dio",
            "db": "objectbox", "baas": "appwrite", "structure": "Standard",
        })
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/main.dart')))
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/app_widget.dart')))

        config_file = os.path.join(project_path, 'lib/app/config/app_config.dart')
        self.assertTrue(os.path.exists(config_file), "app_config.dart not created for Appwrite")

        import json
        config = json.load(open(os.path.join(project_path, '.fpc.json')))
        self.assertEqual(config.get('database'), 'ObjectBox')
        self.assertEqual(config.get('baas'), 'Appwrite')
        self.assertEqual(config.get('state_management'), 'MobX')


if __name__ == "__main__":
    unittest.main()
