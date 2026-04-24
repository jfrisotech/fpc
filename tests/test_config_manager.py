import os
import json
import pytest
from unittest.mock import patch, mock_open
from fpc.config_manager import ConfigManager

class TestConfigManager:
    @pytest.fixture
    def config_manager(self):
        return ConfigManager()

    def test_find_project_root_success(self, config_manager):
        """Test finding project root when pubspec.yaml exists."""
        with patch('os.path.exists') as mock_exists:
            # Mock exists to return True only for a specific path
            mock_exists.side_effect = lambda p: 'pubspec.yaml' in p
            
            root = config_manager.find_project_root('/home/user/project/lib/src')
            assert root == '/home/user/project'

    def test_find_project_root_not_found(self, config_manager):
        """Test returning None when no project root is found."""
        with patch('os.path.exists', return_value=False):
            root = config_manager.find_project_root('/some/random/path')
            assert root is None

    def test_get_config_file_exists(self, config_manager):
        """Test getting config when .fpc.json exists."""
        mock_data = '{"architecture": "MVC"}'
        with patch('fpc.config_manager.ConfigManager.find_project_root', return_value='/root'):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', mock_open(read_data=mock_data)):
                    config = config_manager.get_config('/root/lib')
                    assert config['architecture'] == 'MVC'

    def test_get_config_file_not_exists(self, config_manager):
        """Test getting empty config when .fpc.json is missing."""
        with patch('fpc.config_manager.ConfigManager.find_project_root', return_value='/root'):
            with patch('os.path.exists', return_value=False):
                config = config_manager.get_config('/root/lib')
                assert config == {}

    def test_save_config(self, config_manager):
        """Test saving configuration to file."""
        preferences = {"architecture": "MVVM"}
        with patch('builtins.open', mock_open()) as mocked_file:
            config_manager.save_config('/root', preferences)
            
            # Check if open was called with correct path
            mocked_file.assert_called_once_with(os.path.join('/root', '.fpc.json'), 'w')
            
            # Check if json.dump was called (it's called inside open block)
            handle = mocked_file()
            # We check if write was called with the json string
            # Note: json.dump calls write multiple times or once depending on implementation
            # We can just verify the content written
