"""Parser module to abstract different parsers."""
import logging
from abc import ABCMeta, abstractmethod
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
        return '{}|{}:{}|{} [{}]'.format(self.path, self.line_nr, self.col,
                                         self.msg, self._linter_name)

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
        return super().__lt__(other)


class Linter(metaclass=ABCMeta):
    """Linter implementations should inherit from this class."""

    # Most methods are for child class only, not public.

    #: dict: Configuration for a specific linter
    config = None

    @property
    @classmethod
    @abstractmethod
    def name(cls):
        """Name of this linter. Recommended to be the same as its command."""
        pass  # pragma: no cover

    @property
    def command(self):
        """Command to execute. Defaults to :attr:`name`.

        The options in config files are appended in
        :meth:`command_with_options`.
        """
        return self.name

    @property
    def command_with_options(self):
        """Add arguments from config to :attr:`command`."""
        if 'args' in self.config:
            return ' '.join((self.command, self.config['args']))
        return self.command

    @abstractmethod
    def parse(self, lines):
        """Parse linter output and return results.

        Args:
            lines (iterable): Output lines.

        Returns:
            iterable of Result: Linter results.

        """
        pass  # pragma: no cover

    def _get_relative_path(self, full_path):
        """Return the relative path from current path."""
        try:
            rel_path = Path(full_path).relative_to(Path().absolute())
        except ValueError:
            LOG.error("%s: Couldn't find relative path of '%s' from '%s'.",
                      self.name, full_path, Path().absolute())
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
            return LinterOutput(self.name, **match_result)
        return LinterOutput(self.name, *match_result)
