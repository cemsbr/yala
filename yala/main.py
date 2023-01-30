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
from typing import List

from docopt import docopt

from . import __version__
from .config import Config
from .linters import LINTERS

LOG = logging.getLogger(__name__)


class LinterRunner:
    """Run linter and process results."""

    config = None
    targets: List[str] = []

    def __init__(self, linter_class):
        """Set linter class and its configuration."""
        linter_class.config = self.config.get_linter_config(linter_class.name)
        self._linter = linter_class()

    @classmethod
    def run(cls, linter_cfg_tgts):
        """Run a linter and return the results."""
        linter_class, cls.config, cls.targets = linter_cfg_tgts
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
            return list(stdout), self._format_stderr(stderr)
        except FileNotFoundError as exception:
            # Error if the linter was not found but was chosen by the user
            if self._linter.name in self.config.user_linters:
                error_msg = (
                    f"Could not find {self._linter.name}. "
                    f"Did you install it? Got exception: {exception}"
                )
                return [], [error_msg]
            # If the linter was not chosen by the user, do nothing
            return [], []

    def _get_command(self):
        """Return command with options and targets, ready for execution."""
        targets = " ".join(self.targets)
        cmd_str = self._linter.command_with_options + " " + targets
        cmd_shlex = shlex.split(cmd_str)
        return list(cmd_shlex)

    def _lint(self):
        """Run linter in a subprocess."""
        command = self._get_command()
        process = subprocess.run(  # nosec
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        LOG.info("Finished %s", self._linter.name)
        stdout, stderr = self._get_output_lines(process)
        return self._linter.parse(stdout, stderr)

    @staticmethod
    def _get_output_lines(process):
        return [
            (line for line in output.decode("utf-8").splitlines() if line)
            for output in (process.stdout, process.stderr)
        ]

    def _format_stderr(self, lines):
        return [f"[{self._linter.name}] {line}" for line in lines]


class Main:
    """Parse all linters and aggregate results."""

    # We only need the ``run`` method.

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
            linter_cfg_tgts = (
                (linter, self._config, targets)
                for linter in linters
            )  # fmt: skip
            linters_out_err = pool.map(LinterRunner.run, linter_cfg_tgts)
        stdouts, stderrs = zip(*linters_out_err)
        return (sorted(chain.from_iterable(stdouts)),
                chain.from_iterable(stderrs))  # fmt: skip

    def run_from_cli(self, args):
        """Read arguments, run and print results.

        Args:
            args (dict): Arguments parsed by docopt.

        """
        if args["--dump-config"]:
            self._config.print_config()
        else:
            stdout, stderr = self.lint(args["<path>"])
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
            print(":) No issues found.")

    @staticmethod
    def _print_stdout(stdout):
        for line in stdout:
            print(line)
        issue = "issues" if len(stdout) > 1 else "issue"
        sys.exit(f"\n:( {len(stdout)} {issue} found.")


def main():
    """Entry point for the console script."""
    args = docopt(__doc__, version=__version__)
    Main().run_from_cli(args)
