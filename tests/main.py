"""Tests for the main module."""
import unittest
from unittest.mock import Mock, patch

from yala.main import LinterRunner


class TestLinterRunner(unittest.TestCase):
    """Test the LinterRunner class."""

    @patch('yala.main.Config')
    def test_chosen_not_found(self, mock_config):
        """Should print an error when chosen linter is not found."""
        # Usuário escolhe um linter
        name = 'my linter'
        cls = self._mock_linter_class(name)
        mock_config.get_linter_classes.return_value = [cls]
        mock_config.user_linters = [name]
        with patch('yala.main.subprocess.run', side_effect=FileNotFoundError):
            LinterRunner.config = mock_config
            results = LinterRunner.run(cls)
        self.assertIn('Did you install', results[0])

    @patch('yala.main.Config')
    def test_not_chosen_not_found(self, mock_config):
        """Should print an error when chosen linter is not found."""
        # Usuário escolhe um linter
        name = 'my linter'
        cls = self._mock_linter_class(name)
        mock_config.get_linter_classes.return_value = [cls]
        mock_config.user_linters = []
        with patch('yala.main.subprocess.run', side_effect=FileNotFoundError):
            LinterRunner.config = mock_config
            results = LinterRunner.run(cls)
        self.assertEqual(0, len(results))

    @staticmethod
    def _mock_linter_class(name):
        linter_class = Mock()
        linter = linter_class.return_value
        linter.command_with_options = linter.name = name
        return linter_class
