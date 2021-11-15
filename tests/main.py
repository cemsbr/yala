"""Tests for the main module."""
import unittest
from unittest.mock import Mock, patch

from yala.main import LinterRunner


class TestLinterRunner(unittest.TestCase):
    """Test the LinterRunner class."""

    @patch("yala.main.Config")
    def test_chosen_not_found(self, mock_config):
        """Should print an error when chosen linter is not found."""
        # Linter chosen by the user
        name = "my linter"
        mock_config.user_linters = [name]
        _, stderr = self._path_and_run(mock_config, name)
        self.assertIn("Did you install", stderr[0])

    @patch("yala.main.Config")
    def test_not_chosen_not_found(self, mock_config):
        """Should not print an error when chosen linter is not found."""
        # No linters chosen by the user
        mock_config.user_linters = []
        stdout, stderr = self._path_and_run(mock_config)
        self.assertEqual(0, len(stdout))
        self.assertEqual(0, len(stderr))

    def _path_and_run(self, mock_config, name="my linter"):
        cls = self._mock_linter_class(name)
        mock_config.get_linter_classes.return_value = [cls]
        with patch("yala.main.subprocess.run", side_effect=FileNotFoundError):
            linter_cfg_tgts = cls, mock_config, []
            return LinterRunner.run(linter_cfg_tgts)

    @staticmethod
    def _mock_linter_class(name):
        linter_class = Mock()
        linter = linter_class.return_value
        linter.command_with_options = linter.name = name
        return linter_class
