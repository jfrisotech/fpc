import pytest
from unittest.mock import patch, MagicMock
from fpc.project_manager import ProjectManager

class TestProjectManager:
    @pytest.fixture
    def project_manager(self):
        return ProjectManager()

    @patch('subprocess.run')
    def test_run_flutter_command_success(self, mock_run, project_manager):
        """Test successful execution of a flutter command."""
        mock_run.return_value = MagicMock(returncode=0)
        
        success = project_manager.run_flutter_command('/root', ['pub', 'get'], "Getting deps...")
        
        assert success is True
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args == ['flutter', 'pub', 'get']

    @patch('subprocess.run')
    def test_run_flutter_command_failure(self, mock_run, project_manager):
        """Test failure of a flutter command."""
        mock_run.side_effect = Exception("Command failed")
        
        success = project_manager.run_flutter_command('/root', ['pub', 'get'])
        
        assert success is False

    @patch('fpc.project_manager.ProjectManager.run_flutter_command')
    def test_create_project(self, mock_flutter, project_manager):
        """Test create_project calls flutter create correctly."""
        mock_flutter.return_value = True
        
        with patch('os.path.exists', return_value=True):
            path = project_manager.create_project('my_app', '/projects')
            
            assert '/projects/my_app' in path
            mock_flutter.assert_called_once()
            args = mock_flutter.call_args[0][1]
            assert 'create' in args
            assert 'my_app' in args

    @patch('fpc.project_manager.ProjectManager.run_flutter_command')
    def test_run_build_runner(self, mock_flutter, project_manager):
        """Test run_build_runner calls correct command."""
        project_manager.run_build_runner('/root')
        
        mock_flutter.assert_called_once()
        args = mock_flutter.call_args[0][1]
        assert 'pub' in args
        assert 'run' in args
        assert 'build_runner' in args
        assert 'build' in args
