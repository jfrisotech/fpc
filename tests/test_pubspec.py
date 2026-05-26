import pytest
import subprocess
from unittest.mock import patch, MagicMock
from fpc.generators.pubspec import update_pubspec


# ─────────────────────────────────────────────────────────
# Helper decorator to reduce boilerplate for all tests
# ─────────────────────────────────────────────────────────

def _run_pubspec(tmp_path, preferences):
    """Run update_pubspec with all external calls mocked. Returns the args list passed to subprocess."""
    mock_run_obj = MagicMock(returncode=0)

    with patch('fpc.generators.pubspec._find_flutter', return_value='flutter'), \
         patch('fpc.generators.pubspec._flutter_env', return_value={}), \
         patch('fpc.generators.pubspec.subprocess.run', return_value=mock_run_obj) as mock_run, \
         patch('fpc.generators.pubspec.Console'):
        update_pubspec(str(tmp_path), preferences)
        if mock_run.called:
            return mock_run.call_args[0][0]  # list of args passed to subprocess
        return []


class TestPubspecUpdater:

    # ──────────────────────────────────────────────────────
    # Original tests (kept intact)
    # ──────────────────────────────────────────────────────

    @patch('fpc.generators.pubspec._find_flutter', return_value='flutter')
    @patch('fpc.generators.pubspec.subprocess.run')
    @patch('fpc.generators.pubspec.Console')
    def test_update_pubspec_construction(self, mock_console, mock_run, mock_find, tmp_path):
        """Test if the correct dependencies are added based on preferences."""
        mock_run.return_value = MagicMock(returncode=0)

        preferences = {
            'architecture': 'Clean Architecture',
            'state_management': 'BLoC',
            'http_client': 'Dio',
            'database': 'Hive',
            'baas': 'None'
        }

        update_pubspec(str(tmp_path), preferences)

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]

        assert 'flutter' in args
        assert 'pub' in args
        assert 'add' in args

        assert 'dartz' in args          # Clean Arch
        assert 'flutter_bloc' in args   # BLoC
        assert 'dio' in args            # Dio
        assert 'hive' in args           # Hive
        assert 'dev:hive_generator' in args  # Hive dev dep
        assert 'get_it' in args         # Clean Arch + BLoC

    @patch('fpc.generators.pubspec._find_flutter', return_value='flutter')
    @patch('fpc.generators.pubspec.subprocess.run')
    @patch('fpc.generators.pubspec.Console')
    def test_update_pubspec_error_handling(self, mock_console, mock_run, mock_find, tmp_path):
        """Test handling of flutter pub add failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd', stderr='Conflict detected')

        with patch('fpc.generators.pubspec.print_color') as mock_print:
            update_pubspec(str(tmp_path), {'state_management': 'Provider', 'baas': 'None'})
            assert mock_print.called
            # call_args_list[0] is the error call; call_args_list[-1] is the success message
            first_call_args = mock_print.call_args_list[0][0][0]
            assert 'Error resolving dependencies' in first_call_args
            assert 'Conflict detected' in first_call_args

    # ──────────────────────────────────────────────────────
    # Database coverage — all 4 options
    # ──────────────────────────────────────────────────────

    def test_database_sqlite(self, tmp_path):
        """SQLite (sqflite): should add sqflite, path_provider and path."""
        args = _run_pubspec(tmp_path, {
            'database': 'SQLite (sqflite)', 'state_management': 'None',
            'http_client': 'None', 'baas': 'None', 'architecture': 'MVC'
        })
        assert 'sqflite' in args,       "sqflite missing for SQLite"
        assert 'path_provider' in args, "path_provider missing for SQLite"
        assert 'path' in args,          "path missing for SQLite"

    def test_database_hive(self, tmp_path):
        """Hive: should add hive, hive_flutter, path, build_runner, hive_generator."""
        args = _run_pubspec(tmp_path, {
            'database': 'Hive', 'state_management': 'None',
            'http_client': 'None', 'baas': 'None', 'architecture': 'MVC'
        })
        assert 'hive' in args,                  "hive missing"
        assert 'hive_flutter' in args,           "hive_flutter missing"
        assert 'path' in args,                   "path missing for Hive"
        assert 'dev:hive_generator' in args,     "hive_generator dev dep missing"
        assert 'dev:build_runner' in args,       "build_runner dev dep missing for Hive"

    def test_database_isar(self, tmp_path):
        """Isar: should add isar, isar_flutter_libs, path_provider, path, isar_generator, build_runner."""
        args = _run_pubspec(tmp_path, {
            'database': 'Isar', 'state_management': 'None',
            'http_client': 'None', 'baas': 'None', 'architecture': 'MVC'
        })
        assert 'isar' in args,                  "isar missing"
        assert 'isar_flutter_libs' in args,      "isar_flutter_libs missing"
        assert 'path_provider' in args,          "path_provider missing for Isar"
        assert 'path' in args,                   "path missing for Isar"
        assert 'dev:isar_generator' in args,     "isar_generator dev dep missing"
        assert 'dev:build_runner' in args,       "build_runner dev dep missing for Isar"

    def test_database_objectbox(self, tmp_path):
        """ObjectBox: should add objectbox, objectbox_flutter_libs, path_provider, path, objectbox_generator, build_runner."""
        args = _run_pubspec(tmp_path, {
            'database': 'ObjectBox', 'state_management': 'None',
            'http_client': 'None', 'baas': 'None', 'architecture': 'MVC'
        })
        assert 'objectbox' in args,                  "objectbox missing"
        assert 'objectbox_flutter_libs' in args,      "objectbox_flutter_libs missing"
        assert 'path_provider' in args,               "path_provider missing for ObjectBox"
        assert 'path' in args,                        "path missing for ObjectBox"
        assert 'dev:objectbox_generator' in args,     "objectbox_generator dev dep missing"
        assert 'dev:build_runner' in args,            "build_runner dev dep missing for ObjectBox"

    def test_database_none_no_path(self, tmp_path):
        """No database: 'path' package must NOT be added (it's a DB-only dep)."""
        args = _run_pubspec(tmp_path, {
            'database': 'None', 'state_management': 'None',
            'http_client': 'None', 'baas': 'None', 'architecture': 'MVC'
        })
        assert 'path' not in args, "'path' package should not be added when no DB is selected"

    # ──────────────────────────────────────────────────────
    # HTTP client coverage — all 3 options
    # ──────────────────────────────────────────────────────

    def test_http_client_dio(self, tmp_path):
        """Dio: should add 'dio' package."""
        args = _run_pubspec(tmp_path, {
            'http_client': 'Dio', 'state_management': 'None',
            'database': 'None', 'baas': 'None', 'architecture': 'MVC'
        })
        assert 'dio' in args, "dio missing for Dio http client"
        assert 'http' not in args, "'http' package should NOT be added when Dio is selected"

    def test_http_client_http(self, tmp_path):
        """http: should add 'http' package."""
        args = _run_pubspec(tmp_path, {
            'http_client': 'http', 'state_management': 'None',
            'database': 'None', 'baas': 'None', 'architecture': 'MVC'
        })
        assert 'http' in args, "http package missing"
        assert 'dio' not in args, "'dio' should NOT be added when http is selected"

    def test_http_client_none(self, tmp_path):
        """No HTTP client: neither 'dio' nor 'http' should be added."""
        args = _run_pubspec(tmp_path, {
            'http_client': 'None', 'state_management': 'None',
            'database': 'None', 'baas': 'None', 'architecture': 'MVC'
        })
        assert 'dio' not in args,  "'dio' should not be added when http_client=None"
        assert 'http' not in args, "'http' should not be added when http_client=None"

    # ──────────────────────────────────────────────────────
    # BaaS coverage — all 3 options
    # ──────────────────────────────────────────────────────

    def test_baas_firebase(self, tmp_path):
        """Firebase: should add firebase_core, firebase_auth, cloud_firestore."""
        args = _run_pubspec(tmp_path, {
            'baas': 'Firebase', 'state_management': 'None',
            'http_client': 'None', 'database': 'None', 'architecture': 'MVC'
        })
        assert 'firebase_core' in args,    "firebase_core missing"
        assert 'firebase_auth' in args,    "firebase_auth missing"
        assert 'cloud_firestore' in args,  "cloud_firestore missing"

    def test_baas_supabase(self, tmp_path):
        """Supabase: should add supabase_flutter."""
        args = _run_pubspec(tmp_path, {
            'baas': 'Supabase', 'state_management': 'None',
            'http_client': 'None', 'database': 'None', 'architecture': 'MVC'
        })
        assert 'supabase_flutter' in args, "supabase_flutter missing"
        # Must NOT add Firebase packages
        assert 'firebase_core' not in args, "firebase_core must not appear for Supabase"

    def test_baas_appwrite(self, tmp_path):
        """Appwrite: should add appwrite package."""
        args = _run_pubspec(tmp_path, {
            'baas': 'Appwrite', 'state_management': 'None',
            'http_client': 'None', 'database': 'None', 'architecture': 'MVC'
        })
        assert 'appwrite' in args, "appwrite missing"
        # Must NOT add Firebase or Supabase packages
        assert 'firebase_core' not in args,    "firebase_core must not appear for Appwrite"
        assert 'supabase_flutter' not in args, "supabase_flutter must not appear for Appwrite"

    def test_baas_none(self, tmp_path):
        """No BaaS: none of the BaaS packages should appear."""
        args = _run_pubspec(tmp_path, {
            'baas': 'None', 'state_management': 'None',
            'http_client': 'None', 'database': 'None', 'architecture': 'MVC'
        })
        assert 'firebase_core' not in args,    "firebase_core must not appear for BaaS=None"
        assert 'supabase_flutter' not in args, "supabase_flutter must not appear for BaaS=None"
        assert 'appwrite' not in args,         "appwrite must not appear for BaaS=None"

    # ──────────────────────────────────────────────────────
    # Always-present common dependencies
    # ──────────────────────────────────────────────────────

    def test_common_deps_always_present(self, tmp_path):
        """logger, shared_preferences and intl must always be added regardless of preferences."""
        args = _run_pubspec(tmp_path, {
            'state_management': 'None', 'http_client': 'None',
            'database': 'None', 'baas': 'None', 'architecture': 'MVC'
        })
        assert 'logger' in args,              "logger always required"
        assert 'shared_preferences' in args,  "shared_preferences always required"
        assert 'intl' in args,                "intl always required"
