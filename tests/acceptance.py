"""Acceptance tests for yala executable."""
import re
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from yala.main import main


class TestAcceptance(TestCase):
    """Acceptance test."""

    @classmethod
    @patch('yala.main.sys.exit')
    @patch('yala.main.sys.stdout', new_callable=StringIO)
    @patch('yala.main.Pool')
    def setUpClass(cls, pool_mock, stdout_mock, exit_mock):
        """Get yala's output to be used in tests.

        As coverage outputs random results with --concurrency=multiprocessing,
        we use Python threads instead.
        """
        # Ignore params of patch decorators:
        # pylint: disable=arguments-differ
        cls._exit = exit_mock
        # Replace multiprocessing by Python threads
        pool_mock.return_value = ThreadPoolExecutor()
        with patch('yala.main.sys.argv', ['yala', 'tests_data/']):
            main()
        cls._output = stdout_mock.getvalue()

    def _assert_results(self, lines, linter_name):
        """Assert all lines are in the output."""
        for line in lines:
            self._assert_result(line, linter_name)

    def _assert_result(self, result, linter_name):
        self.assertTrue(self._output_has_result(result, linter_name),
                        'Couldn\'t match:\n{}\nOutput:\n{}'.format(
                            result, self._output))

    def _assert_any_result(self, results, linter_name):
        first_result = any(self._output_has_result(r, linter_name)
                           for r in results)
        self.assertTrue(first_result, 'None matched:\n{}\nOutput:\n{}'
                        .format('\n'.join(results), self._output))

    def _output_has_result(self, result, linter_name):
        expected_regex = self._get_expected_regex(result, linter_name)
        return re.match(expected_regex, self._output, re.M | re.S) is not None

    @staticmethod
    def _get_expected_regex(line, linter_name):
        """Return a regex to match both Linux and Windows paths."""
        regex = r'.*?^tests_data[/\\].*.py\|{} \[{}\]$'
        escaped_output = re.escape(line)
        return regex.format(escaped_output, linter_name)

    def test_exit_error(self):
        """Should exit with error if there's linter output."""
        arg = self._exit.call_args_list[0][0][0]
        self.assertTrue(arg, 'Exit argument should not be empty')

    def test_flake8(self):
        """Check pycodestyle output."""
        expected = (
            "1:1|F401 'os' imported but unused",
            "2:1|F401 'abc' imported but unused",
            "7:20|E211 whitespace before '('"
            )
        self._assert_results(expected, 'flake8')

    def test_isort(self):
        """Check isort output."""
        expected = 'None:None|Imports are incorrectly sorted and/or formatted.'
        self._assert_result(expected, 'isort')

    def test_mypy(self):
        """Check mypy output."""
        expected = "4:None|error: Need type comment for 'untyped_list' " + \
            '(hint: "untyped_list = ...  # type: List[<type>]")'
        expected_py37 = '4:None|error: Need type annotation for ' + \
            '\'untyped_list\' (hint: "untyped_list: List[<type>] = ...")'
        possible_results = expected, expected_py37
        self._assert_any_result(possible_results, 'mypy')

    def test_pycodestyle(self):
        """Check pycodestyle output."""
        expected = "7:20|E211 whitespace before '('"
        self._assert_result(expected, 'pycodestyle')

    def test_pydocstyle(self):
        """Check pydocstyle ouput."""
        expected = '1:None|D100: Missing docstring in public module'
        self._assert_result(expected, 'pydocstyle')

    def test_pyflakes(self):
        """Check Pyflakes output."""
        expected_any = (
            "1:1|'os' imported but unused",     # pyflakes 2.2.0
            "1:None|'os' imported but unused")  # pyflakes 2.1.1
        self._assert_any_result(expected_any, 'pyflakes')

        expected_any = (
            "2:1|'abc' imported but unused",
            "2:None|'abc' imported but unused")
        self._assert_any_result(expected_any, 'pyflakes')

    def test_pylint(self):
        """Check Pylint output."""
        expected = (
            '1:0|Missing module docstring (C0114, missing-module-docstring)',
            '1:0|Unused import os (W0611, unused-import)',
            '2:0|Unused import abc (W0611, unused-import)',
            '7:0|Too many branches (20/12) (R0912, too-many-branches)',
            '1:0|Similar lines in 2 files\n'
            '==tests_data.duplicate1:3\n'
            '==tests_data.duplicate2:3\n'
            'def dummy_function():\n'
            '    """Must have at least four lines."""\n'
            '    aaa = 0\n'
            '    bbb = 1\n'
            '    ccc = 2\n'
            '    print(aaa + bbb + ccc) (R0801, duplicate-code)',
        )
        self._assert_results(expected, 'pylint')

    def test_rest_radon_cc(self):
        """Check radon cc ouput."""
        expected = '7:0|high_complexity - D'
        self._assert_result(expected, 'radon cc')
