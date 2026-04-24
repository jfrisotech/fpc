import pytest
from unittest.mock import patch, MagicMock
from fpc.template_manager import TemplateManager

class TestTemplateManager:
    @pytest.fixture
    def template_manager(self):
        return TemplateManager()

    def test_get_template_content_generic(self, template_manager):
        """Test getting generic template content."""
        with patch('builtins.__import__') as mock_import:
            mock_module = MagicMock()
            mock_module.get_controller_template.return_value = "generic_content"
            mock_import.return_value = mock_module
            
            content = template_manager.get_template_content('controller', 'Auth', 'None')
            assert content == "generic_content"

    def test_get_template_content_sm_specific(self, template_manager):
        """Test getting state-management specific template content."""
        with patch('builtins.__import__') as mock_import:
            mock_module = MagicMock()
            mock_module.get_provider_controller_template.return_value = "provider_content"
            mock_import.return_value = mock_module
            
            content = template_manager.get_template_content('controller', 'Auth', 'Provider')
            assert content == "provider_content"

    def test_get_template_content_fallback_to_generic(self, template_manager):
        """Test fallback to generic when SM-specific fails or is missing."""
        with patch('builtins.__import__') as mock_import:
            # First call (SM-specific) raises ImportError
            # Second call (Generic) returns module
            mock_module = MagicMock()
            mock_module.get_controller_template.return_value = "fallback_content"
            
            mock_import.side_effect = [ImportError(), mock_module]
            
            content = template_manager.get_template_content('controller', 'Auth', 'UnknownSM')
            assert content == "fallback_content"

    def test_get_template_content_viewmodel_fallback(self, template_manager):
        """Test that viewmodel falls back to controller templates if specific vm template is missing."""
        with patch('builtins.__import__') as mock_import:
            mock_module = MagicMock()
            # Simulate module having get_controller_template but NOT get_viewmodel_template
            del mock_module.get_viewmodel_template
            mock_module.get_controller_template.return_value = "vm_fallback_content"
            mock_import.return_value = mock_module
            
            content = template_manager.get_template_content('viewmodel', 'Auth', 'None')
            assert content == "vm_fallback_content"
