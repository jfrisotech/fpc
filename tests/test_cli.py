import sys
import pytest
from unittest.mock import patch, MagicMock
from fpc.cli import main

class TestCLI:
    @patch('fpc.cli.FlutterGenerator')
    @patch('fpc.cli.ConfigManager')
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_gen_command(self, mock_parse, mock_config, mock_gen, tmp_path):
        """Test if 'fpc gen controller login' calls the generator correctly."""
        # Setup mocks
        mock_args = MagicMock()
        mock_args.command = 'gen'
        mock_args.type = 'controller'
        mock_args.path = 'auth/login'
        mock_args.state = None
        mock_parse.return_value = mock_args
        
        generator_instance = mock_gen.return_value
        
        # Run main
        with patch('os.getcwd', return_value=str(tmp_path)):
            main()
        
        # Verify generator call
        # directory should be 'auth' relative to cwd, but here it's just 'auth'
        generator_instance.generate_file.assert_called_once()
        args, kwargs = generator_instance.generate_file.call_args
        assert args[0] == 'controller'
        assert args[2] == 'login'

    @patch('fpc.cli.ConfigManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('fpc.cli.Console')
    def test_cli_init_command(self, mock_console, mock_parse, mock_config):
        """Test if 'fpc init' triggers initialization logic."""
        mock_args = MagicMock()
        mock_args.command = 'init'
        mock_parse.return_value = mock_args
        
        mock_config.find_project_root.return_value = '/root'
        mock_config.is_fpc_initialized.return_value = False
        
        with patch('fpc.cli.FlutterGenerator') as mock_gen:
            gen_instance = mock_gen.return_value
            gen_instance.get_project_preferences.return_value = {'arch': 'MVC'}
            
            main()
            
            mock_config.save_config.assert_called_once_with('/root', {'arch': 'MVC'})

    @patch('fpc.cli.ConfigManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('fpc.cli.Console')
    def test_cli_config_set_command(self, mock_console, mock_parse, mock_config):
        """Test if 'fpc config --set key value' updates configuration."""
        mock_args = MagicMock()
        mock_args.command = 'config'
        mock_args.set = ['architecture', 'Clean Architecture']
        mock_parse.return_value = mock_args
        
        mock_config.find_project_root.return_value = '/root'
        mock_config.get_config.return_value = {'architecture': 'MVC'}
        
        main()
        
        # Verify save_config was called with updated data
        mock_config.save_config.assert_called_once_with('/root', {'architecture': 'Clean Architecture'})
