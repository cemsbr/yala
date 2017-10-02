"""Run linters on files and directories and sort results.

Usage:
  yala <path>...
  yala -h | --help
  yala --version

Options:
  -h --help  Show this help.
  --version  Show yala and linters' versions.

"""
import logging
import shlex
import subprocess
import sys
from itertools import chain
from multiprocessing import Pool

from docopt import docopt

from yala.linters import (Isort, Pycodestyle, Pydocstyle, Pylint, RadonCC,
                          RadonMI)

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
        linters = (Pylint(), Pycodestyle(), Pydocstyle(), Isort(), RadonCC(),
                   RadonMI())
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
        cmd = shlex.split(cmd_str)
        cmd = list(cmd)
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        LOG.info('Finished %s', ' '.join(cmd))
        output = process.stdout.decode('utf-8')
        lines = (line for line in output.split('\n') if line)
        return list(linter.parse(lines))


def main():
    """Entry point for the console script."""
    logging.basicConfig(level=logging.INFO)
    args = docopt(__doc__, version='1.2.0')
    Main().run(args['<path>'])
