import pytest
from unittest.mock import patch, MagicMock
from fpc.doctor import Doctor

class TestDoctor:
    @pytest.fixture
    def doctor(self):
        return Doctor()

    @patch('subprocess.run')
    def test_check_command_success(self, mock_run, doctor):
        mock_run.return_value = MagicMock(stdout='version 1.0\nline2', returncode=0)
        status, detail = doctor._check_command(['cmd'])
        
        assert "[green]OK[/green]" in status
        assert "version 1.0" in detail

    @patch('subprocess.run')
    def test_check_command_failure(self, mock_run, doctor):
        mock_run.side_effect = FileNotFoundError()
        status, detail = doctor._check_command(['cmd'])
        
        assert "[red]Missing[/red]" in status

    @patch('fpc.doctor.ConfigManager')
    @patch('fpc.doctor.Table')
    @patch('fpc.doctor.Console')
    def test_doctor_run_flow(self, mock_console, mock_table, mock_config, doctor):
        # Mocking check_command to return OK for all
        with patch.object(doctor, '_check_command', return_value=("[green]OK[/green]", "Details")):
            mock_config.find_project_root.return_value = "/root"
            mock_config.is_fpc_initialized.return_value = True
            mock_config.get_config.return_value = {"architecture": "MVC"}
            
            doctor.run()
            
            # Verify table add_row was called for Python, Flutter, Git, and Project
            assert mock_table.return_value.add_row.call_count >= 4
