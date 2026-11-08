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

    def test_scenario_mvvm_riverpod_drift(self):
        """Scenario 2: MVVM + Riverpod + Drift (Rigid)"""
        project_name = "mvvm_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()

        preferences = {
            "architecture": "MVVM",
            "state_management": "Riverpod",
            "database": "Drift",
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
            "db": "Drift", "baas": "Firebase", "structure": "Standard"
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

    def test_scenario_clean_bloc_drift(self):
        """Phase 4, Scenario 13: Clean Architecture + BLoC + Drift."""
        project_path = self.run_full_scaffold("clean_bloc_drift_app", {
            "arch": "Clean", "state": "BLoC", "http": "Dio",
            "db": "drift", "baas": "none", "structure": "Standard",
        })
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/core/error/failures.dart')))
        import json
        config = json.load(open(os.path.join(project_path, '.fpc.json')))
        self.assertEqual(config.get('database'), 'Drift', "Config must record Drift")

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

    def test_scenario_clean_arch_cubit_scaffold(self):
        """Clean Architecture + Cubit + Standard scaffolding test."""
        project_path = self.run_full_scaffold("clean_cubit_app", {
            "arch": "Clean", "state": "Cubit", "http": "Dio",
            "db": "None", "baas": "None", "structure": "Standard"
        })

        # Presentation cubit directory and files
        cubit_dir = os.path.join(project_path, 'lib/app/presentation/cubit/auth')
        self.assertTrue(os.path.isdir(cubit_dir), "Cubit auth dir not created")

        cubit_file = os.path.join(cubit_dir, 'auth_cubit.dart')
        self.assertTrue(os.path.exists(cubit_file), "auth_cubit.dart not created")
        cubit_content = open(cubit_file).read()
        self.assertIn("class AuthCubit extends Cubit<AuthState>", cubit_content)
        self.assertIn("final LoginUseCase loginUseCase;", cubit_content)

        state_file = os.path.join(cubit_dir, 'auth_state.dart')
        self.assertTrue(os.path.exists(state_file), "auth_state.dart not created")
        state_content = open(state_file).read()
        self.assertIn("abstract class AuthState extends Equatable", state_content)
        self.assertIn("class AuthInitial extends AuthState", state_content)

        # Login page using BlocConsumer
        page_file = os.path.join(project_path, 'lib/app/presentation/pages/login_page.dart')
        self.assertTrue(os.path.exists(page_file), "login_page.dart not created")
        page_content = open(page_file).read()
        self.assertIn("BlocConsumer<AuthCubit, AuthState>", page_content)

        # Service locator and main.dart
        sl_file = os.path.join(project_path, 'lib/app/config/service_locator.dart')
        self.assertTrue(os.path.exists(sl_file), "service_locator.dart not created for Cubit")

        main_content = open(os.path.join(project_path, 'lib/main.dart')).read()
        self.assertIn("MultiBlocProvider", main_content)
        self.assertIn("sl.init()", main_content)

    def test_scenario_clean_cubit_modular(self):
        """Clean Architecture + Cubit + Modular scaffolding test."""
        project_path = self.run_full_scaffold("clean_cubit_mod_app", {
            "arch": "Clean", "state": "Cubit", "http": "Dio",
            "db": "None", "baas": "None", "structure": "Modular"
        })
        modules_path = os.path.join(project_path, 'lib/app/modules/auth')
        self.assertTrue(os.path.isdir(modules_path), "Modular auth module not created for Clean+Cubit")
        cubit_dir = os.path.join(modules_path, 'presentation', 'cubit', 'auth')
        self.assertTrue(os.path.isdir(cubit_dir), "Cubit presentation folder not created")
        self.assertTrue(os.path.exists(os.path.join(cubit_dir, 'auth_cubit.dart')))

    def test_clean_scaffolding_no_unnecessary_files(self):
        """Clean Architecture: verifies shared/utils/responsively.dart and no orphan directories."""
        project_path = self.run_full_scaffold("clean_lean_app", {
            "arch": "Clean", "state": "BLoC", "http": "Dio",
            "db": "None", "baas": "None", "structure": "Standard"
        })
        # Shared utils
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/shared/utils/responsively.dart')))
        self.assertFalse(os.path.exists(os.path.join(project_path, 'lib/app/utils')))
        # Core util removed
        self.assertFalse(os.path.exists(os.path.join(project_path, 'lib/app/core/util')))
        # l10n removed
        self.assertFalse(os.path.exists(os.path.join(project_path, 'lib/app/l10n')))
        # Remote data source in remote/
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/data/datasources/remote/auth_remote_data_source.dart')))
        # No local datasource when db is None
        self.assertFalse(os.path.exists(os.path.join(project_path, 'lib/app/data/datasources/local')))
        # No presentation/widgets empty folder
        self.assertFalse(os.path.exists(os.path.join(project_path, 'lib/app/presentation/widgets')))

    def test_mvc_scaffolding_clean_structure(self):
        """MVC: verifies no empty repositories/widgets folders and correct shared utils import."""
        project_path = self.run_full_scaffold("mvc_lean_app", {
            "arch": "MVC", "state": "None", "http": "None",
            "db": "None", "baas": "None", "structure": "Standard"
        })
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/shared/utils/responsively.dart')))
        self.assertFalse(os.path.exists(os.path.join(project_path, 'lib/app/repositories')))
        self.assertFalse(os.path.exists(os.path.join(project_path, 'lib/app/widgets')))
        self.assertTrue(os.path.exists(os.path.join(project_path, 'lib/app/services/auth_service.dart')))
        login_view_content = open(os.path.join(project_path, 'lib/app/views/login_view.dart')).read()
        self.assertIn("../shared/utils/responsively.dart", login_view_content)
        # Accessibility & Testing Keys
        self.assertIn("key: const Key('login_email_input')", login_view_content)
        self.assertIn("key: const Key('login_submit_button')", login_view_content)
        self.assertIn("Semantics(", login_view_content)
        self.assertIn("ExcludeSemantics(", login_view_content)

        home_view_content = open(os.path.join(project_path, 'lib/app/views/home_view.dart')).read()
        self.assertIn("key: const Key('home_logout_button')", home_view_content)
        self.assertIn("ExcludeSemantics(", home_view_content)

    def test_network_dio_and_drift_cache_scaffolding(self):
        """Verifies DioClient, Drift AppDatabase, and offline cache local data source."""
        project_path = self.run_full_scaffold("network_drift_app", {
            "arch": "Clean", "state": "BLoC", "http": "Dio",
            "db": "Drift", "baas": "None", "structure": "Standard"
        })
        # DioClient
        dio_file = os.path.join(project_path, 'lib/app/shared/network/dio_client.dart')
        self.assertTrue(os.path.exists(dio_file), "dio_client.dart not created")
        dio_content = open(dio_file).read()
        self.assertIn("class DioClient", dio_content)
        self.assertIn("LogInterceptor", dio_content)

        # Drift Database
        db_file = os.path.join(project_path, 'lib/app/shared/database/app_database.dart')
        self.assertTrue(os.path.exists(db_file), "app_database.dart not created")
        db_content = open(db_file).read()
        self.assertIn("class AppDatabase", db_content)
        self.assertIn("@DriftDatabase", db_content)

        # Local data source with FlutterSecureStorage
        local_ds = os.path.join(project_path, 'lib/app/data/datasources/local/auth_local_data_source.dart')
        self.assertTrue(os.path.exists(local_ds), "auth_local_data_source.dart not created")
        local_ds_content = open(local_ds).read()
        self.assertIn("class AuthLocalDataSourceImpl", local_ds_content)
        self.assertIn("FlutterSecureStorage", local_ds_content)
        self.assertIn("jsonEncode(user.toJson())", local_ds_content)

        # Secure Storage Service
        storage_file = os.path.join(project_path, 'lib/app/shared/storage/secure_storage_service.dart')
        self.assertTrue(os.path.exists(storage_file), "secure_storage_service.dart not created")
        storage_content = open(storage_file).read()
        self.assertIn("class SecureStorageService", storage_content)
        self.assertIn("saveToken", storage_content)

        # Repository caching logic
        repo_impl = os.path.join(project_path, 'lib/app/data/repositories/auth_repository_impl.dart')
        repo_content = open(repo_impl).read()
        self.assertIn("localDataSource?.cacheUser", repo_content)
        self.assertIn("localDataSource?.getLastUser()", repo_content)

        # Clean Arch LoginPage Accessibility & Testing Keys
        login_page = os.path.join(project_path, 'lib/app/presentation/pages/login_page.dart')
        login_page_content = open(login_page).read()
        self.assertIn("key: const Key('login_submit_button')", login_page_content)
        self.assertIn("key: const Key('login_title_text')", login_page_content)
        self.assertIn("Semantics(", login_page_content)
        self.assertIn("ExcludeSemantics(", login_page_content)

    def test_clean_arch_feature_generation_usecase(self):
        """Verifies that fpc gen feature creates {feature}_usecase.dart in Clean Architecture."""
        project_name = "clean_feat_app"
        project_path = self.setup_fake_project(project_name)
        generator = FlutterGenerator()

        preferences = {
            "architecture": "Clean Architecture",
            "state_management": "BLoC",
            "database": "None",
            "http_client": "None",
            "baas": "None"
        }
        ConfigManager.save_config(project_path, preferences)

        generator.generate_file('feature', os.path.join(project_path, 'lib'), 'orders')

        usecase_file = os.path.join(project_path, 'lib/orders/domain/usecases/orders_usecase.dart')
        self.assertTrue(os.path.exists(usecase_file), "orders_usecase.dart was not generated")
        usecase_content = open(usecase_file).read()
        self.assertIn("class GetOrdersUseCase implements UseCase<OrdersEntity, OrdersParams>", usecase_content)

    def test_full_scaffolding_enhanced_features_validation(self):
        """Verifies Makefile, Environment, AppAssets, strict linter, and Splash session flow."""
        project_path = self.run_full_scaffold("enhanced_app", {
            "arch": "Clean", "state": "Cubit", "http": "Dio",
            "db": "Drift", "baas": "None", "structure": "Standard"
        })

        # Validate with official validation criteria
        from tests.validation_criteria import validate_directory_structure, validate_app_routes
        struct_errors = validate_directory_structure(project_path, "clean", "cubit", "standard", "drift")
        self.assertEqual(len(struct_errors), 0, f"Structure validation errors: {struct_errors}")

        route_errors = validate_app_routes(project_path, "clean", "cubit", "standard")
        self.assertEqual(len(route_errors), 0, f"Route validation errors: {route_errors}")

        # Check Makefile
        makefile_path = os.path.join(project_path, 'Makefile')
        self.assertTrue(os.path.exists(makefile_path))
        makefile_content = open(makefile_path).read()
        self.assertIn(".DEFAULT_GOAL := help", makefile_content)
        self.assertIn("build-apk-prod:", makefile_content)
        self.assertIn("build-ipa-prod:", makefile_content)

        # Check Environment
        env_path = os.path.join(project_path, 'lib/app/config/environment.dart')
        self.assertTrue(os.path.exists(env_path))
        env_content = open(env_path).read()
        self.assertIn("class Environment", env_content)

        # Check AppAssets
        assets_path = os.path.join(project_path, 'lib/app/shared/assets/app_assets.dart')
        self.assertTrue(os.path.exists(assets_path))

        # Check Splash and Home
        splash_path = os.path.join(project_path, 'lib/app/presentation/pages/splash_page.dart')
        self.assertTrue(os.path.exists(splash_path))
        home_path = os.path.join(project_path, 'lib/app/presentation/pages/home_page.dart')
        self.assertTrue(os.path.exists(home_path))

        # Check AppRoutes
        routes_path = os.path.join(project_path, 'lib/app/config/app_routes.dart')
        routes_content = open(routes_path).read()
        self.assertIn("initialRoute = '/splash'", routes_content)
        self.assertIn("'/splash': (context) => const SplashPage()", routes_content)
        self.assertIn("'/home': (context) => const HomePage()", routes_content)


if __name__ == "__main__":
    unittest.main()
