import pytest
from unittest.mock import patch, MagicMock
from fpc.generators.pubspec import update_pubspec

class TestPubspecUpdater:
    @patch('subprocess.run')
    @patch('fpc.generators.pubspec.Console')
    def test_update_pubspec_construction(self, mock_console, mock_run, tmp_path):
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
        
        # Verify subprocess.run was called
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        
        assert 'flutter' in args
        assert 'pub' in args
        assert 'add' in args
        
        # Verify specific dependencies
        assert 'dartz' in args # Clean Arch
        assert 'flutter_bloc' in args # BLoC
        assert 'dio' in args # Dio
        assert 'hive' in args # Hive
        assert 'dev:hive_generator' in args # Hive dev dep
        assert 'get_it' in args # Clean Arch + BLoC

    @patch('subprocess.run')
    @patch('fpc.generators.pubspec.Console')
    def test_update_pubspec_error_handling(self, mock_console, mock_run, tmp_path):
        """Test handling of flutter pub add failure."""
        import subprocess
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd', stderr='Conflict detected')
        
        # Should not raise exception but print error
        with patch('fpc.generators.pubspec.print_color') as mock_print:
            update_pubspec(str(tmp_path), {'state_management': 'Provider'})
            assert mock_print.called
            args = mock_print.call_args[0][0]
            assert 'Error resolving dependencies' in args
            assert 'Conflict detected' in args
