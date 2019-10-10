YALA - Yet Another Linter Aggregator
====================================

|build| |coveralls| |codecov| |codacy| |issue_time|

YALA combines many linters to improve the quality of your code. Other projects may come to your mind, but does anyone have all the features below?

Works with latest linters
    Yala uses linters' outputs and doesn't break when their APIs change.
Same defaults
    No changes to linters' default configuration.
Easy to configure
    Set any command-line option for any linter (even pylint!) in setup.cfg.
Fast
    Run linters in parallel.

Current Status
--------------
Currently supported Python tools:

- `Flake8 <https://pypi.org/project/flake8/>`_
- `Isort <https://pypi.org/project/isort/>`_
- `MyPy <http://www.mypy-lang.org/>`_
- `Pycodestyle <https://pycodestyle.readthedocs.io/>`_
- `Pydocstyle <http://pydocstyle.org/>`_
- `Pyflakes <https://pypi.org/project/pyflakes/>`_
- `Pylint <http://pylint.pycqa.org/>`_
- `Radon <https://radon.readthedocs.org/>`_


Install
-------
Tested with Python >= 3.5.

.. code-block:: bash

  # Minimal: isort and pycodestyle
  sudo pip3 install --upgrade yala
  # OR all supported linters
  sudo pip3 install --upgrade yala[all]
  # OR choose your linters (+isort and pycodestyle)
  sudo pip3 install --upgrade yala[mypy,pylint]

If you are willing to hack yala's code, run the command below in this README's folder:

.. code-block:: sh

  # Use pip
  sudo pip3 install --editable .[all,dev]
  # OR pipenv
  pipenv sync --dev


Usage
-----
Just call ``yala`` followed by the files and/or folders to lint.


Configuration
-------------

Besides the configuration of each linter, as in their docs, you can specify other options in *setup.cfg*.

It's possible to define command line arguments for linters in *setup.cfg*, which is particularly useful for *pylint*, a linter that ignores this file and requires you to write an extra one only for itself.

The default configuration file is ``yala/setup.cfg`` that you can copy and customize.

You can have this file in upper directories and override it in lower directories if needed.


Linters' options
................

For example, to disable a specific pylint warning and output grades C and lower for Radon Maintainability Index (default is D or worse), add the following to *setup.cfg*:

.. code-block:: ini

  [yala]
  pylint args = --disable=TODO

Besides `pylint`, you can define CLI options for `isort`, `pycodestyle` and `pydocstyle` (the names are exactly as they are called in command line).


Choosing linters
................

All supported and installed linters are enabled by default.

You can customize the linters in *setup.cfg* by either:

.. code-block:: ini

  [yala]
  linters = isort, pycodestyle

or

.. code-block:: ini

  [yala]
  linters = 
    isort
    pycodestyle

Or even a mix of both: multiple linters in multiple lines.


Example
.......

Run pydocstyle and pylint without missing-docstring errors (besides isort and
pycodestyle that are installed by default):

.. code-block:: sh

  pip install --upgrade yala[pycodestyle,pylint]

.. code-block:: ini

   [pydocstyle]
   add-ignore = D1

   [yala]
   pylint args = --disable=C0114,C0115,C0116


Hacking: Adding a linter
------------------------
Check the file *yala/linters.py* and feel free to ask for help.


.. |build| image:: https://travis-ci.org/cemsbr/yala.svg?branch=master
          :target: https://travis-ci.org/cemsbr/yala

.. |coveralls| image:: https://coveralls.io/repos/github/cemsbr/yala/badge.svg?branch=master
              :target: https://coveralls.io/github/cemsbr/yala?branch=master

.. |codecov| image:: https://codecov.io/gh/cemsbr/yala/branch/master/graph/badge.svg
            :target: https://codecov.io/gh/cemsbr/yala

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/e435a65c5dd44ecf9369010b29616bd0
           :target: https://www.codacy.com/app/cems/yala?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cemsbr/yala&amp;utm_campaign=Badge_Grade

.. |issue_time| image:: http://isitmaintained.com/badge/resolution/cemsbr/yala.svg
               :target: http://isitmaintained.com/project/cemsbr/yala
