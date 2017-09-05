"""Test Base module."""
from configparser import ConfigParser
from unittest import TestCase
from unittest.mock import Mock, patch

from yala.base import Config


class TestConfig(TestCase):
    """Test setup.cfg config."""

    def test_user_cfg_append(self):
        """User configuration should be appended to default values."""
        default_cfg = {'yala': {'lint args': '--def_param=1'}}
        user_cfg = {'yala': {'lint args': '--user_param=2'}}
        expected = '--def_param=1 --user_param=2'

        default = ConfigParser()
        default.read_dict(default_cfg)
        default.read_file = Mock()
        user = ConfigParser()
        user.read_dict(user_cfg)
        user.read = Mock()

        with patch('yala.base.ConfigParser', side_effect=(default, user)):
            config = Config(Mock(), 'user_cfg_filename')
            linter_cfg = config.get_linter_config('lint')
            self.assertEqual(expected, linter_cfg['args'])
