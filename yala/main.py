"""Run linters on files and directories and sort results.

Usage:
  yala <path>...
  yala --dump-config
  yala --version
  yala -h | --help

Options:
  --dump-config  Show all detected configurations
  --version  Show yala and linters' versions.
  -h --help  Show this help.

"""
import logging
import shlex
import subprocess
import sys
from itertools import chain
from multiprocessing import Pool

from docopt import docopt

from .base import Config
from .linters import Isort, Pycodestyle, Pydocstyle, Pylint, RadonCC, RadonMI

LOG = logging.getLogger(__name__)


class Main:
    """Parse all linters and aggregate results."""

    # We only need the ``run`` method.
    # pylint: disable=too-few-public-methods

    def __init__(self):
        """Extra arguments for all linters (path to lint)."""
        self._targets = []

    def lint(self, *targets):
        """Run linters in parallel and sort all results."""
        self._targets = targets
        linters = (Pylint(), Pycodestyle(), Pydocstyle(), Isort(), RadonCC(),
                   RadonMI())
        with Pool() as pool:
            linters_results = pool.map(self._parse_linter, linters)
        return sorted(chain.from_iterable(linters_results))

    def run(self, args):
        """Print results."""
        if args['--dump-config']:
            self.dump_config()
        else:
            results = self.lint(*args['<path>'])
            self.print_results(results)

    @staticmethod
    def dump_config():
        """Print all yala configurations, including default and user's."""
        if LOG.isEnabledFor(logging.INFO):
            print()  # blank line separator if log info is enabled
            # disable logging filenames again
            logger = logging.getLogger(Config.__module__)
            logger.setLevel(logging.NOTSET)
            logger.propagate = False
        for key, value in Config().config.items():
            print(f'{key}: {value}')

    @staticmethod
    def print_results(results):
        """Print linter results and exits with an error if there's any."""
        if LOG.isEnabledFor(logging.INFO):
            print()  # blank line separator if log info is enabled
        if results:
            for result in results:
                print(result)
            issue = 'issues' if len(results) > 1 else 'issue'
            sys.exit(f'\n:( {len(results)} {issue} found.')
        else:
            print(':) No issues found.')

    def _parse_linter(self, linter):
        """Run a linter and return its results."""
        cmd_str = ' '.join((linter.cmd, ' '.join(self._targets)))
        cmd = shlex.split(cmd_str)
        cmd = list(cmd)
        process = subprocess.run(cmd, stdout=subprocess.PIPE)
        LOG.info('Finished %s', ' '.join(cmd))
        output = process.stdout.decode('utf-8')
        lines = (line for line in output.split('\n') if line)
        return list(linter.parse(lines))


def main():
    """Entry point for the console script."""
    args = docopt(__doc__, version='1.3.0')
    Main().run(args)
