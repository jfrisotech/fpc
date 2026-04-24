import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
from fpc.generators.generator import FlutterGenerator

class TestFlutterGenerator:
    @pytest.fixture
    def mock_services(self):
        return {
            'config': MagicMock(),
            'project': MagicMock(),
            'template': MagicMock(),
            'console': MagicMock()
        }

    @pytest.fixture
    def generator(self, mock_services):
        gen = FlutterGenerator()
        gen.config_manager = mock_services['config']
        gen.project_manager = mock_services['project']
        gen.template_manager = mock_services['template']
        gen.console = mock_services['console']
        return gen

    def test_generate_file_success(self, generator, mock_services):
        """Test generating a single file."""
        mock_services['config'].get_config.return_value = {'state_management': 'Provider'}
        mock_services['template'].get_template_content.return_value = "content"
        
        with patch('os.path.exists', return_value=False):
            with patch('os.makedirs'):
                with patch('builtins.open', mock_open()) as mocked_file:
                    generator.generate_file('controller', '/path/to/lib', 'Auth')
                    
                    # Verify template was requested
                    mock_services['template'].get_template_content.assert_called_with(
                        'controller', 'auth', 'Provider'
                    )
                    
                    # Verify file was written
                    mocked_file.assert_called_once()
                    mocked_file().write.assert_called_once_with("content")

    @patch('os.makedirs')
    def test_generate_feature_clean_arch(self, mock_makedirs, generator, mock_services):
        """Test generating a feature with Clean Architecture structure."""
        mock_services['config'].get_config.return_value = {
            'architecture': 'Clean Architecture',
            'state_management': 'BLoC'
        }
        
        with patch.object(generator, 'generate_file') as mock_gen_file:
            generator._generate_feature('/lib', 'auth', 'BLoC')
            
            # Verify subfolders were created (at least some of them)
            # We check if makedirs was called for domain, data, presentation
            calls = [call[0][0] for call in mock_makedirs.call_args_list]
            assert any('domain' in c for c in calls)
            assert any('data' in c for c in calls)
            assert any('presentation' in c for c in calls)
            
            # Verify individual files were generated
            assert mock_gen_file.call_count >= 4 # controller, view, service, model
