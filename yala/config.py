"""Yala configuration."""
import logging
from configparser import ConfigParser
from pathlib import Path

LOG = logging.getLogger(__name__)


class Config:
    """Deal with default and user configuration.

    Internal use only. If you are implementing your own linter, use
    ``self._config``.
    """

    # pylint: disable=too-few-public-methods

    _CFG_FILE = 'setup.cfg'
    #: str: Section of the config file.
    _CFG_SECTION = 'yala'

    def __init__(self):
        """Concatenate default and user config from filenames.

        Args:
            default_file (pathlib.Path): Yala's default file.
            user_file (pathlib.Path, str): User config file. May not exist.
        """
        default_cfg = self._read_default_file()
        user_cfg = self._read_user_files()
        self.config = self._merge(default_cfg, user_cfg)

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

    def get_linter_config(self, name):
        """Return linter options without linter name prefix."""
        prefix = name + ' '
        return {k[len(prefix):]: v
                for k, v in self.config.items()
                if k.startswith(prefix)}

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
