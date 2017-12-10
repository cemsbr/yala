"""Module for linters."""
# The less we need to code, the better!
# pylint: disable=too-few-public-methods
import re

from .base import Linter, LinterOutput


class Isort(Linter):
    """Isort parser."""

    name = 'isort'

    def parse(self, lines):
        """Get full path and message from each output line."""
        # E.g. "ERROR: /my/path/main.py Imports are incorrectly sorted."
        pattern = re.compile(r'''
                             ^.+?
                             :\ (?P<full_path>.+?)
                             \ (?P<msg>.+)$''', re.VERBOSE)
        return self._parse_by_pattern(lines, pattern)

    def _create_output_from_match(self, match_result):
        """As isort outputs full path, we change it to relative path."""
        full_path = match_result['full_path']
        path = self._get_relative_path(full_path)
        return LinterOutput(self.name, path, match_result['msg'])


class Pycodestyle(Linter):
    """Pycodestyle parser."""

    name = 'pycodestyle'

    def parse(self, lines):
        """Get :class:`base.Result` parameters using regex."""
        pattern = re.compile(r'''
                             ^(?P<path>.+?)
                             :(?P<line_nr>\d+?)
                             :(?P<col>\d+?)
                             :\ (?P<msg>.+)$''', re.VERBOSE)
        return self._parse_by_pattern(lines, pattern)


class Mypy(Linter):
    """Mypy parser."""

    name = 'mypy'

    def parse(self, lines):
        """Get :class:`base.Result` parameters using regex."""
        pattern = re.compile(r'''
                             ^(?P<path>.+?)
                             :(?P<line_nr>\d+?)
                             :\ (?P<msg>.+)$''', re.VERBOSE)
        return self._parse_by_pattern(lines, pattern)


class Pydocstyle(Linter):
    """Pydocstyle parser."""

    name = 'pydocstyle'

    def parse(self, lines):
        """Get :class:`base.Result` parameters using regex.

        There are 2 lines for each pydocstyle result:
            1. Filename and line number;
            2. Message for the problem found.
        """
        patterns = [re.compile(r'^(.+?):(\d+)'),
                    re.compile(r'^\s+(.+)$')]
        for i, line in enumerate(lines):
            if i % 2 == 0:
                path, line_nr = patterns[0].match(line).groups()
            else:
                msg = patterns[1].match(line).group(1)
                yield LinterOutput(self.name, path, msg, line_nr)


class Pyflakes(Linter):
    """Pyflakes parser."""

    name = 'pyflakes'

    def parse(self, lines):
        """Get :class:`base.Result` parameters using regex."""
        pattern = re.compile(r'''
                             ^(?P<path>.+?)
                             :(?P<line_nr>\d+?)
                             :\ (?P<msg>.+)$''', re.VERBOSE)
        return self._parse_by_pattern(lines, pattern)


class Pylint(Linter):
    """Pylint parser."""

    name = 'pylint'

    def parse(self, lines):
        """Get :class:`base.Result` parameters using regex."""
        pattern = re.compile(r"""^(?P<path>.+?)
                                 :(?P<msg>.+)
                                 :(?P<line_nr>\d+?)
                                 :(?P<col>\d+?)$""", re.VERBOSE)
        return self._parse_by_pattern(lines, pattern)


class RadonCC(Linter):
    """Parser for radon ciclomatic complexity."""

    name = 'radon cc'

    def parse(self, lines):
        """Get :class:`base.Result` parameters using regex.

        The output has one line with the file path followed by others with
        one problem per line.
        """
        # E.g. 'relative/path/to/file.py'
        pattern_path = re.compile(r'^(\S.*$)')
        # E.g. '    C 19:0 RadonCC - A'
        pattern_result = re.compile(r'\s+\w (\d+):(\d+) (.+)$')
        path = None
        for line in lines:
            match = pattern_path.match(line)
            if match:
                # We have the file path. Skip the remainder of the loop
                path = line
                continue
            match = pattern_result.match(line)
            if match:
                # Output found for the file stored in ``path``.
                line_nr, col, msg = match.groups()
                yield LinterOutput(self.name, path, msg, line_nr, col)


class RadonMI(Linter):
    """Parser for radon maintainability index."""

    name = 'radon mi'

    def parse(self, lines):
        """Get :class:`base.Result` parameters using regex."""
        pattern = re.compile(r'''
                             ^(?P<path>.+)
                             \ -\ (?P<msg>[A-F])$''', re.VERBOSE)
        return self._parse_by_pattern(lines, pattern)


#: dict: All Linter subclasses indexed by class name
LINTERS = {cls.name: cls for cls in Linter.__subclasses__()}
