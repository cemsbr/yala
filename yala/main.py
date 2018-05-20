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
            stdout, stderr = self._lint()
            # Can't return a generator from a subprocess
            return list(stdout), stderr or []
        except FileNotFoundError as exception:
            # Error if the linter was not found but was chosen by the user
            if self._linter.name in self.config.user_linters:
                error_msg = 'Could not find {}. Did you install it? ' \
                    'Got exception: {}'.format(self._linter.name, exception)
                return [[], [error_msg]]
            # If the linter was not chosen by the user, do nothing
            return [[], []]

    def _get_command(self):
        """Return command with options and targets, ready for execution."""
        targets = ' '.join(self.targets)
        cmd_str = self._linter.command_with_options + ' ' + targets
        cmd_shlex = shlex.split(cmd_str)
        return list(cmd_shlex)

    def _lint(self):
        """Run linter in a subprocess."""
        command = self._get_command()
        process = subprocess.run(command, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        LOG.info('Finished %s', ' '.join(command))
        stdout, stderr = self._get_output_lines(process)
        return self._linter.parse(stdout), self._parse_stderr(stderr)

    @staticmethod
    def _get_output_lines(process):
        return [(line for line in output.decode('utf-8').split('\n') if line)
                for output in (process.stdout, process.stderr)]

    def _parse_stderr(self, lines):
        return ['[{}] {}'.format(self._linter.name, line) for line in lines]


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
            out_err_none = pool.map(LinterRunner.run, linters)
        out_err = [item for item in out_err_none if item is not None]
        stdout, stderr = zip(*out_err)
        return sorted(chain.from_iterable(stdout)), chain.from_iterable(stderr)

    def run_from_cli(self, args):
        """Read arguments, run and print results.

        Args:
            args (dict): Arguments parsed by docopt.
        """
        if args['--dump-config']:
            self._config.print_config()
        else:
            stdout, stderr = self.lint(args['<path>'])
            self.print_results(stdout, stderr)

    @classmethod
    def print_results(cls, stdout, stderr):
        """Print linter results and exits with an error if there's any."""
        for line in stderr:
            print(line, file=sys.stderr)
        if stdout:
            if stderr:  # blank line to separate stdout from stderr
                print(file=sys.stderr)
            cls._print_stdout(stdout)
        else:
            print(':) No issues found.')

    @staticmethod
    def _print_stdout(stdout):
        for line in stdout:
            print(line)
        issue = 'issues' if len(stdout) > 1 else 'issue'
        sys.exit('\n:( {} {} found.'.format(len(stdout), issue))


def main():
    """Entry point for the console script."""
    args = docopt(__doc__, version='1.6.0')
    Main().run_from_cli(args)
