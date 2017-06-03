"""Run linters, process output and display results."""
import logging
import shlex
import subprocess
import sys
from itertools import chain
from multiprocessing import Pool

from yala.linters import (Isort, Pycodestyle, Pydocstyle, Pyflakes, Pylint,
                          RadonCC, RadonMI)

LOG = logging.getLogger(__name__)


class Main:
    """Parse all linters and aggregate results."""

    # We only need the ``run`` method.
    # pylint: disable=too-few-public-methods

    def __init__(self):
        """Extra arguments for all linters (path to lint)."""
        self._args = None

    def get_results(self, args):
        """Run linters in parallel and sort all results."""
        self._args = args
        linters = (Pylint(), Pycodestyle(), Pydocstyle(), Pyflakes(), Isort(),
                   RadonCC(), RadonMI())
        with Pool() as pool:
            linters_results = pool.map(self._parse_linter, linters)
        return sorted(chain.from_iterable(linters_results))

    def run(self, args):
        """Print results."""
        results = self.get_results(args)
        if results:
            print()
            for result in results:
                print(result)
            issue = 'issues' if len(results) > 1 else 'issue'
            sys.exit(f'\n:( {len(results)} {issue} found.')
        else:
            print('\n:) No issues found.')

    def _parse_linter(self, linter):
        """Run a linter and return its results."""
        cmd_str = ' '.join((linter.cmd, ' '.join(self._args)))
        cmd = shlex.shlex(cmd_str, posix=True, punctuation_chars=True)
        cmd = list(cmd)
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        LOG.info('Finished %s.', cmd_str)
        output = process.stdout.decode('utf-8')
        lines = (line for line in output.split('\n') if line)
        return list(linter.parse(lines))


def main():
    """Entry point for the console script."""
    logging.basicConfig(level=logging.INFO)
    extra_args = sys.argv[1:]
    Main().run(extra_args)
