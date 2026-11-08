import os
import tempfile
import shutil
import pytest
from fpc.templates.common.environment_template import get_environment_content
from fpc.templates.shared.assets.app_assets_template import get_app_assets_content
from fpc.templates.common.analysis_options_template import get_analysis_options_content
from fpc.templates.common.makefile_template import get_makefile_content
from fpc.templates.common.app_routes_template import get_app_routes_content
from fpc.templates.mvc.views.splash_view_template import get_splash_view_content
from fpc.templates.clean_arch.presentation.splash_page_template import get_splash_page_content
from fpc.templates.clean_arch.presentation.home_page_template import get_clean_home_page_content
from fpc.templates.shared.network.dio_client_template import get_dio_client_content
from fpc.templates.shared.network.http_client_template import get_http_client_content
from fpc.generators.pubspec import configure_pubspec_assets
from fpc.generators.structure import generate_project_structure
from fpc.templates.templates import create_template_files


class TestEnhancedFeatures:
    @pytest.fixture(autouse=True)
    def setup_tmp(self):
        self.test_dir = tempfile.mkdtemp()
        yield
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_environment_template(self):
        """Test environment template has AppEnvironment, apiBaseUrl, name, enableLogging."""
        content = get_environment_content()
        assert 'enum AppEnvironment' in content
        assert 'class Environment' in content
        assert 'apiBaseUrl' in content
        assert 'enableLogging' in content
        assert 'String.fromEnvironment' in content
        assert 'bool.fromEnvironment' in content
        assert 'isProduction' in content

    def test_app_assets_template(self):
        """Test app_assets template provides type-safe image and icon paths."""
        content = get_app_assets_content()
        assert 'class AppAssets' in content
        assert "static const String logo = '$imagesPath/logo.png';" in content
        assert "static const String placeholder = '$imagesPath/placeholder.png';" in content
        assert "static const String appIcon = '$iconsPath/app_icon.png';" in content

    def test_analysis_options_template(self):
        """Test strict analysis_options.yaml content."""
        content = get_analysis_options_content()
        assert 'strict-casts: true' in content
        assert 'strict-inference: true' in content
        assert 'strict-raw-types: true' in content
        assert 'avoid_relative_lib_imports' in content
        assert 'prefer_const_constructors' in content

    def test_splash_view_and_page(self):
        """Test splash views verify session using SecureStorageService."""
        mvc_splash = get_splash_view_content()
        assert 'class SplashView' in content if (content := mvc_splash) else False
        assert 'SecureStorageService' in mvc_splash
        assert 'getToken()' in mvc_splash
        assert '/home' in mvc_splash
        assert '/login' in mvc_splash
        assert 'Key(\'splash_loading_indicator\')' in mvc_splash

        clean_splash = get_splash_page_content()
        assert 'class SplashPage' in clean_splash
        assert 'SecureStorageService' in clean_splash
        assert 'getToken()' in clean_splash
        assert '/home' in clean_splash
        assert '/login' in clean_splash

    def test_clean_home_page(self):
        """Test Clean Architecture home page has logout button and responsive layout."""
        content = get_clean_home_page_content()
        assert 'class HomePage' in content
        assert 'home_logout_button' in content
        assert 'home_welcome_text' in content
        assert 'OrientationLayout' in content

    def test_app_routes_initial_route(self):
        """Test AppRoutes sets initialRoute to /splash for MVC, MVVM, and Clean Arch."""
        content = get_app_routes_content({'architecture': 'Clean Architecture', 'state_management': 'Cubit'})
        assert "static const String initialRoute = '/splash';" in content
        assert "'/splash': (context) => const SplashPage()" in content
        assert "'/login': (context) => const LoginPage()" in content
        assert "'/home': (context) => const HomePage()" in content

        content_mvc = get_app_routes_content({'architecture': 'MVC (Model-View-Controller)', 'state_management': 'None'})
        assert "static const String initialRoute = '/splash';" in content_mvc
        assert "'/splash': (context) => const SplashView()" in content_mvc
        assert "'/login': (context) => const LoginView()" in content_mvc
        assert "'/home': (context) => const HomeView()" in content_mvc

    def test_dio_and_http_client_environment_integration(self):
        """Test DioClient and HttpClient use Environment.apiBaseUrl."""
        dio_content = get_dio_client_content()
        assert 'Environment.apiBaseUrl' in dio_content
        assert 'Environment.enableLogging' in dio_content
        assert 'environment.dart' in dio_content

        http_content = get_http_client_content()
        assert 'Environment.apiBaseUrl' in http_content
        assert 'environment.dart' in http_content

    def test_configure_pubspec_assets(self):
        """Test declaring assets in pubspec.yaml."""
        pubspec_path = os.path.join(self.test_dir, 'pubspec.yaml')
        with open(pubspec_path, 'w') as f:
            f.write("name: test_app\n\nflutter:\n  uses-material-design: true\n")

        configure_pubspec_assets(self.test_dir)

        with open(pubspec_path, 'r') as f:
            updated = f.read()

        assert 'assets:' in updated
        assert '- assets/images/' in updated
        assert '- assets/icons/' in updated

    def test_scaffolding_creates_all_new_files(self):
        """Test that project structure and template generation produce all required files."""
        project_path = os.path.join(self.test_dir, 'sample_project')
        os.makedirs(project_path)
        with open(os.path.join(project_path, 'pubspec.yaml'), 'w') as f:
            f.write("name: sample_project\n")

        preferences = {
            'architecture': 'Clean Architecture',
            'state_management': 'Cubit',
            'http_client': 'Dio',
            'database': 'Drift',
            'baas': 'None',
            'folder_structure': 'Standard (Layer First)',
        }

        generate_project_structure(project_path, preferences)
        create_template_files(project_path, preferences)

        # Check assets directories and gitkeep
        assert os.path.isfile(os.path.join(project_path, 'assets', 'images', '.gitkeep'))
        assert os.path.isfile(os.path.join(project_path, 'assets', 'icons', '.gitkeep'))

        # Check AppAssets
        assert os.path.isfile(os.path.join(project_path, 'lib', 'app', 'shared', 'assets', 'app_assets.dart'))

        # Check Environment
        assert os.path.isfile(os.path.join(project_path, 'lib', 'app', 'config', 'environment.dart'))

        # Check analysis_options.yaml
        assert os.path.isfile(os.path.join(project_path, 'analysis_options.yaml'))

        # Check Makefile
        assert os.path.isfile(os.path.join(project_path, 'Makefile'))

        # Check Splash and Home pages
        assert os.path.isfile(os.path.join(project_path, 'lib', 'app', 'presentation', 'pages', 'splash_page.dart'))
        assert os.path.isfile(os.path.join(project_path, 'lib', 'app', 'presentation', 'pages', 'home_page.dart'))

        # Check pubspec.yaml assets config
        with open(os.path.join(project_path, 'pubspec.yaml'), 'r') as f:
            pub_content = f.read()
        assert 'assets/images/' in pub_content
        assert 'assets/icons/' in pub_content

    def test_makefile_template(self):
        """Test Makefile targets, tab recipes, and help screen."""
        content = get_makefile_content()
        assert '.DEFAULT_GOAL := help' in content
        assert 'help:' in content
        assert 'setup:' in content
        assert 'clean:' in content
        assert 'upgrade:' in content
        assert 'generate:' in content
        assert 'watch:' in content
        assert 'lint:' in content
        assert 'format:' in content
        assert 'test:' in content
        assert 'test-coverage:' in content
        # Run
        assert 'run-dev:' in content
        assert 'run-staging:' in content
        assert 'run-prod:' in content
        # Build APK
        assert 'build-apk-dev:' in content
        assert 'build-apk-staging:' in content
        assert 'build-apk-prod:' in content
        # Build AAB
        assert 'build-aab-dev:' in content
        assert 'build-aab-staging:' in content
        assert 'build-aab-prod:' in content
        # Build IPA
        assert 'build-ipa-dev:' in content
        assert 'build-ipa-staging:' in content
        assert 'build-ipa-prod:' in content
        # Ensure recipes use TAB indentation
        for line in content.split('\n'):
            if line.startswith('flutter ') or line.startswith('dart '):
                # Should not start with bare spaces or bare commands without tabs
                assert False, f"Recipe line missing tab: {line}"
        assert '\tflutter pub get' in content
        assert '\tdart run build_runner build' in content


