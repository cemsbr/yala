"""Test Base module."""
from configparser import ConfigParser
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from yala.config import Config


class TestConfig(TestCase):
    """Test setup.cfg config."""

    def test_user_cfg_append(self):
        """User configuration should be appended to default values."""
        config = self._get_config(
            user_cfg={'my linter args': '--user_param=2'},
            default_cfg={'my linter args': '--def_param=1'}
        )
        expected = '--def_param=1 --user_param=2'
        linter_cfg = config.get_linter_config('my linter')
        self.assertEqual(expected, linter_cfg['args'])

    @patch('sys.stdout', new_callable=StringIO)
    def test_dump_no_linters(self, mock_stdout):
        """Test default configuration dump."""
        all_linters = ('linter a', 'linter b')
        config = self._get_config(all_linters)
        config.print_config()
        expected_lines = [
            '[yala]',
            'linters: linter a, linter b',
            'isort args: --check',
            'pylint args: --msg-template="{path}:{msg}'
            ' ({msg_id}, {symbol}):{line}:{column}"',
            'radon cc args: --min D',
            'radon mi args: --min D']
        self.assertSequenceEqual(expected_lines,
                                 mock_stdout.getvalue().splitlines())

    @patch('sys.stdout', new_callable=StringIO)
    def test_dump_with_linters(self, mock_stdout):
        """Test default configuration dump."""
        all_linters = {'linter a': 'LinterA', 'linter b': 'LinterB'}
        user_config = {'linters': 'linter b'}
        config = self._get_config(all_linters, user_config)
        config.print_config()
        expected_lines = [
            '[yala]',
            'linters: linter b',
            'isort args: --check',
            'pylint args: --msg-template="{path}:{msg}'
            ' ({msg_id}, {symbol}):{line}:{column}"',
            'radon cc args: --min D',
            'radon mi args: --min D']
        self.assertSequenceEqual(expected_lines,
                                 mock_stdout.getvalue().splitlines())

    @classmethod
    def _get_config(cls, all_linters=None, user_cfg=None, default_cfg=None):
        """Return real config with mocked ConfigParser."""
        all_linters = all_linters or {}
        user_cfg = user_cfg or {}
        default_cfg = default_cfg or {}
        default = cls._get_config_parser({'yala': default_cfg})
        user = cls._get_config_parser({'yala': user_cfg})
        with patch('yala.config.ConfigParser', side_effect=(default, user)):
            return Config(all_linters)

    @staticmethod
    def _get_config_parser(dictionary):
        config = ConfigParser()
        config.read_dict(dictionary)
        return config
