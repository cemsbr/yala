"""Parser module to abstract different parsers."""
import logging
from abc import ABCMeta, abstractmethod
from configparser import ConfigParser
from pathlib import Path

LOG = logging.getLogger(__name__)


class LinterOutput:
    """A one-line linter result. It can be sorted and printed as string."""

    # We only override magic methods.
    # pylint: disable=too-few-public-methods

    def __init__(self, linter_name, path, msg, line_nr=None, col=None):
        """Optionally set all attributes.

        Args:
            path (str): Relative file path.
            line (int): Line number.
            msg (str): Explanation of what is wrong.
            col (int): Column where the problem begins.
        """
        # Set all attributes in the constructor for convenience.
        # pylint: disable=too-many-arguments
        if line_nr:
            line_nr = int(line_nr)
        if col:
            col = int(col)
        self._linter_name = linter_name
        self.path = path
        self.line_nr = line_nr
        self.msg = msg
        self.col = col

    def __str__(self):
        """Output shown to the user."""
        return f'{self.path}|{self.line_nr}:{self.col}|{self.msg} ' + \
            f'[{self._linter_name}]'

    def _cmp_key(self, obj=None):
        """Comparison key for sorting results from all linters.

        The sort should group files and lines from different linters to make it
        easier for refactoring.
        """
        if not obj:
            obj = self
        line_nr = int(obj.line_nr) if obj.line_nr else 0
        col = int(obj.col) if obj.col else 0
        return (obj.path, line_nr, col, obj.msg)

    def __lt__(self, other):
        """Use ``_cmp_key`` to compare two lines."""
        if isinstance(other, type(self)):
            return self._cmp_key() < self._cmp_key(other)


class Linter(metaclass=ABCMeta):
    """Linter implementations should inherit from this class."""

    # Most methods are to be used by the child class only.
    #: pylint: disable=too-few-public-methods

    #: list: Configuration files.
    _CFG_FILES = (
        Path(__file__).parent / 'setup.cfg',  # default
        'setup.cfg'  # User's. May be absent.
    )
    #: str: Section of the config file.
    _CFG_SECTION = 'yala'

    #: dict: yala configuration only (can be empty).
    _config = ConfigParser()
    _config.read(_CFG_FILES)
    _config = _config[_CFG_SECTION]

    def __init__(self, cmd, name=None):
        """At least, the executable name.

        cmd (str): Linter executable name. For arguments, config file is
            recommended.
        name (str): Name to be displayed in the results. Defaults to ``cmd``.
        """
        self._name = cmd if name is None else name
        self._config = self.__get_config(self._name)
        self.cmd = self._get_cmd(cmd)

    @classmethod
    def __get_config(cls, name):
        prefix = name + ' '
        return {k[len(prefix):]: v
                for k, v in cls._config.items()
                if k.startswith(prefix)}

    def _get_cmd(self, cmd):
        """Add arguments from config and quote."""
        if 'args' in self._config:
            return ' '.join((cmd, self._config['args']))
        return cmd

    @abstractmethod
    def parse(self, lines):
        """Parse linter output and return results.

        Args:
            lines (iterable): Lines of the output.

        Returns:
            iterable of Result: Linter results.

        """
        raise NotImplementedError

    def _get_relative_path(self, full_path):
        """Return the relative path from current path."""
        try:
            rel_path = Path(full_path).relative_to(Path().absolute())
        except ValueError:
            LOG.error("%s: Couldn't find relative path of '%s' from '%s'.",
                      self._name, full_path, Path().absolute())
            return full_path
        return str(rel_path)

    def _parse_by_pattern(self, lines, pattern):
        """Match pattern line by line and return Results.

        Use ``_create_output_from_match`` to convert pattern match groups to
        Result instances.

        Args:
            lines (iterable): Output lines to be parsed.
            pattern: Compiled pattern to match against lines.
            result_fn (function): Receive results of one match and return a
                Result.

        Return:
            generator: Result instances.
        """
        for line in lines:
            match = pattern.match(line)
            if match:
                params = match.groupdict()
                if not params:
                    params = match.groups()
                yield self._create_output_from_match(params)

    def _create_output_from_match(self, match_result):
        """Create Result instance from pattern match results.

        Args:
            match: Pattern match.
        """
        if isinstance(match_result, dict):
            return LinterOutput(self._name, **match_result)
        return LinterOutput(self._name, *match_result)
