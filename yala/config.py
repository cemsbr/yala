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
        self.user_linters = []  # chosen by the user
        self.linters = {}       # chosen by the user or all of them
        self._set_linters()

    def _set_linters(self):
        """Do not use pyflakes unless it was specified.

        We can't ignore a pyflakes error, so we don't use it by default.
        """
        if 'linters' in self._config:
            self.user_linters = list(self._parse_cfg_linters())
            self.linters = {linter: self._all_linters[linter]
                            for linter in self.user_linters}
        else:
            self.linters = self._all_linters
            if 'pyflakes' in self.linters:
                self.linters.pop('pyflakes')

    def print_config(self):
        """Print all yala configurations, including default and user's."""
        linters = self.user_linters or list(self.linters)
        print('linters:', ', '.join(linters))
        for key, value in self._config.items():
            if key != 'linters':
                print('{}: {}'.format(key, value))

    def get_linter_classes(self):
        """Return linters to be executed."""
        return (self._all_linters[linter] for linter in self.linters)

    def _parse_cfg_linters(self):
        """Return valid linter names found in config files."""
        user_value = self._config.get('linters', '')
        # For each line of "linters" value, use comma as separator
        for line in user_value.splitlines():
            yield from self._parse_linters_line(line)

    def _parse_linters_line(self, line):
        linters = (linter for linter in re.split(r'\s*,\s*', line))
        for linter in linters:
            if linter in self._all_linters:
                yield linter
            elif linter:
                LOG.warning('%s is not a valid linter', linter)

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
