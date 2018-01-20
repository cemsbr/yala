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

from .config import Config
from .linters import LINTERS

LOG = logging.getLogger(__name__)


class LinterRunner:
    """Run linter and process results."""

    config = None
    targets = []

    def __init__(self, linter_class):
        """Set linter class and its configuration."""
        linter_class.config = self.config.get_linter_config(linter_class.name)
        self._linter = linter_class()

    @classmethod
    def run(cls, linter_class):
        """Run a linter and return the results."""
        runner = cls(linter_class)
        return runner.get_results()

    def get_results(self):
        """Run the linter, parse, and return result list.

        If a linter specified by the user is not found, return an error message
        as result.
        """
        try:
            return list(self._parse_output())
        except FileNotFoundError as exception:
            # Error if the linter was not found but was chosen by the user
            if self._linter.name in self.config.user_linters:
                error_msg = 'Could not find {}. Did you install it? ' \
                    'Got exception: {}'.format(self._linter.name, exception)
                return [error_msg]
            # If the linter was not chosen by the user, do nothing
            return tuple()

    def _parse_output(self):
        """Return parsed output."""
        output = self._lint()
        lines = (line for line in output.split('\n') if line)
        return self._linter.parse(lines)

    def _lint(self):
        """Run linter in a subprocess."""
        command = self._get_command()
        process = subprocess.run(command, stdout=subprocess.PIPE)
        LOG.info('Finished %s', ' '.join(command))
        return process.stdout.decode('utf-8')

    def _get_command(self):
        """Return command with options and targets, ready for execution."""
        targets = ' '.join(self.targets)
        cmd_str = self._linter.command_with_options + ' ' + targets
        cmd_shlex = shlex.split(cmd_str)
        return list(cmd_shlex)


class Main:
    """Parse all linters and aggregate results."""

    # We only need the ``run`` method.
    # pylint: disable=too-few-public-methods

    def __init__(self, config=None, all_linters=None):
        """Initialize the only Config object and assign it to other classes.

        Args:
            config (Config): Config object.
            all_linters (dict): Names and classes of all available linters.
        """
        self._classes = all_linters or LINTERS
        self._config = config or Config(self._classes)
        LinterRunner.config = self._config

    def lint(self, targets):
        """Run linters in parallel and sort all results.

        Args:
            targets (list): List of files and folders to lint.
        """
        LinterRunner.targets = targets
        linters = self._config.get_linter_classes()
        with Pool() as pool:
            linters_results = pool.map(LinterRunner.run, linters)
        return sorted(chain.from_iterable(linters_results))

    def run_from_cli(self, args):
        """Read arguments, run and print results.

        Args:
            args (dict): Arguments parsed by docopt.
        """
        if args['--dump-config']:
            self._config.print_config()
        else:
            results = self.lint(args['<path>'])
            self.print_results(results)

    @staticmethod
    def print_results(results):
        """Print linter results and exits with an error if there's any."""
        if results:
            for result in results:
                print(result)
            issue = 'issues' if len(results) > 1 else 'issue'
            sys.exit('\n:( {} {} found.'.format(len(results), issue))
        else:
            print(':) No issues found.')


def main():
    """Entry point for the console script."""
    args = docopt(__doc__, version='1.5.0')
    Main().run_from_cli(args)
