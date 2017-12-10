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

from .linters import LINTERS

LOG = logging.getLogger(__name__)


class LinterRunner:
    """Run linter and process results."""

    config = None
    targets = ''

    def __init__(self, linter_class):
        """Set the linter class."""
        self._linter = linter_class()

    @classmethod
    def run(cls, linter_class):
        """Run a linter and return its results."""
        return cls(linter_class).get_results()

    def get_results(self):
        """Run the linter, parse, and return result list.

        If a linter specified by the user is not found, return an error message
        as a result.
        """
        try:
            return list(self._parse_output())
        except FileNotFoundError as exception:
            # Error if the linter not found was chosen by the user
            if self._is_user_choice():
                error_msg = 'Did you install "{}"? Got exception: {}'.format(
                    self._linter.name, exception)
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
        cmd_str = self._linter.command_with_options + ' ' + self.targets
        cmd_shlex = shlex.split(cmd_str)
        return list(cmd_shlex)

    def _is_user_choice(self):
        """Return whether the linter was explicitly chosen by the user."""
        return self._linter.name in self.config.linters


class Main:
    """Parse all linters and aggregate results."""

    # We only need the ``run`` method.
    # pylint: disable=too-few-public-methods

    def __init__(self):
        """Initialize the only Config instance and set it in other classes."""
        self._config = Config()
        LinterRunner.config = self._config
        for name, cls in LINTERS.items():
            cls.config = self._config.get_linter_config(name)

    def lint(self, targets):
        """Run linters in parallel and sort all results."""
        LinterRunner.targets = ' '.join(targets)
        linters = self._config.get_linter_classes(LINTERS)
        with Pool() as pool:
            linters_results = pool.map(LinterRunner.run, linters)
        return sorted(chain.from_iterable(linters_results))

    def run(self, args):
        """Print results."""
        if args['--dump-config']:
            self._config.dump_config(LINTERS.values())
        else:
            results = self.lint(args['<path>'])
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
            print('{}: {}'.format(key, value))

    @staticmethod
    def print_results(results):
        """Print linter results and exits with an error if there's any."""
        if LOG.isEnabledFor(logging.INFO):
            print()  # blank line separator if log info is enabled
        if results:
            for result in results:
                print(result)
            issue = 'issues' if len(results) > 1 else 'issue'
            sys.exit('\n:( {} {} found.'.format(len(results), issue))
        else:
            print(':) No issues found.')


def main():
    """Entry point for the console script."""
    args = docopt(__doc__, version='1.4.0')
    Main().run(args)
