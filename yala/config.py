"""Yala configuration."""
import logging
import re
from configparser import ConfigParser
from pathlib import Path

LOG = logging.getLogger(__name__)


class Config:
    """Deal with default and user configuration.

    Internal use only. If you are implementing your own linter, use
    ``self._config``.
    """

    _config = None

    _CFG_FILE = 'setup.cfg'
    #: str: Section of the config file.
    _CFG_SECTION = 'yala'

    def __init__(self, all_linters):
        """Read default and user config files.

        Args:
            all_linters (dict): Names and classes of all available linters.
        """
        self._all_linters = all_linters
        default_cfg = self._read_default_file()
        user_cfg = self._read_user_files()
        self._config = self._merge(default_cfg, user_cfg)
        if 'linters' in self._config:
            self._active_linters = self.user_linters = self._get_linters()
        else:
            self.user_linters = []
            self._active_linters = all_linters

    def print_config(self):
        """Print all yala configurations, including default and user's."""
        print('linters:', ', '.join(self._active_linters))
        for key, value in self._config.items():
            if key != 'linters':
                print(f'{key}: {value}')

    def get_linter_classes(self):
        """Return linters to be executed."""
        return (self._all_linters[linter]
                for linter in self._active_linters)

    def _get_linters(self):
        """Return linters' names found in config files."""
        linters = []
        user_value = self._config.get('linters', '')
        # For each line of "linters" value, use comma as separator
        for line in user_value.splitlines():
            line_linters = [linter for linter in re.split(r'\s*,\s*', line)
                            if linter]
            linters.extend(line_linters)
        return linters

    def get_linter_config(self, name):
        """Return linter options without linter name prefix."""
        prefix = name + ' '
        return {k[len(prefix):]: v
                for k, v in self._config.items()
                if k.startswith(prefix)}

    @classmethod
    def _read_default_file(cls):
        yala_dir = Path(__file__).parent
        default_file = yala_dir / cls._CFG_FILE
        config = ConfigParser()
        config.read(str(default_file))
        return config

    @classmethod
    def _read_user_files(cls):
        work_dir = Path.cwd()
        user_files = [work_dir / cls._CFG_FILE]
        # From current dir's file to root's file
        user_files += [parent / cls._CFG_FILE for parent in work_dir.parents]
        user_cfg = ConfigParser()
        # Reverse order so parent folder's file is overridden.
        for user_file in reversed(user_files):
            if user_file.is_file():
                LOG.info('Reading %s', user_file)
                user_cfg.read(str(user_file))
        return user_cfg

    @classmethod
    def _merge(cls, default, user):
        """Append user options to default options. Return yala section."""
        section = cls._CFG_SECTION
        merged = default[section]

        if section not in user:
            return merged

        user = user[section]
        for key, value in user.items():
            if key in merged:
                merged[key] += ' ' + value
            else:
                merged[key] = value
        return merged
