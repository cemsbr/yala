YALA - Yet Another Linter Aggregator
====================================

|build| |coveralls| |codecov| |codacy| |issue_time|

|version| |downloads|

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
- `Black <https://black.readthedocs.io/>`_


Install
-------
Tested with Python >= 3.6. You can specify multiple linters separated by commas:

- ``yala`` installs isort, pycodestyle, and pylint (minimal install);
- ``yala[all]`` adds *mypy*, *pydocstyle*, *pyflakes*, and *radon*;
- ``yala[all,flake8]`` also adds *flake8*;

.. code-block:: bash

  # Minimal: isort, pycodestyle and pylint
  sudo pip3 install --upgrade yala
  # OR (almost) all supported linters
  sudo pip3 install --upgrade yala[all]
  # OR choose your linters (+isort, pycodestyle and pylint)
  sudo pip3 install --upgrade yala[mypy,radon]

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

Besides the standard configuration files of each linter, as in their docs, you can specify any command-line option in *setup.cfg* with yala.

Writing command-line arguments for linters in *setup.cfg* is particularly useful for *pylint* because it ignores *setup.cfg* and requires you to write an extra file. Now, you don't have to.

The default configuration file is in ``yala/setup.cfg``. You can copy it to your project's root folder and customize it. If you need other configuration for a nested directory, just create another file there.


Linters' options
................

For example, to disable a specific pylint warning and output grades C and lower for Radon Maintainability Index (default is D or worse), add the following to *setup.cfg*:

.. code-block:: ini

  [yala]
  pylint args = --disable=TODO
  radon mi args = --min C

Besides `pylint`, you can define CLI options for `isort`, `pycodestyle`, `pydocstyle`, etc (the names are exactly as they are called in command line).


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

Run pydocstyle and pylint without missing-docstring errors (besides isort,
pycodestyle, and pylint that are installed by default):

.. code-block:: sh

  pip install --upgrade yala[pydocstyle]

.. code-block:: ini

   [pydocstyle]
   add-ignore = D1

   [yala]
   pylint args = --disable=C0114,C0115,C0116


If you're using `black` with `isort`, `pycodestyle` and `flake8`, make sure to set options that won't conflict, for instance:

.. code-block:: ini

  [isort]
  profile=black

  [pycodestyle]
  max-line-length = 88

  [flake8]
  max-line-length = 88


Hacking: Adding a linter
------------------------
Check the file *yala/linters.py* and feel free to ask for help.


.. |build| image:: https://travis-ci.org/cemsbr/yala.svg?branch=master
          :target: https://travis-ci.org/cemsbr/yala

.. |coveralls| image:: https://coveralls.io/repos/github/cemsbr/yala/badge.svg?branch=master
              :target: https://coveralls.io/github/cemsbr/yala?branch=master

.. |codecov| image:: https://codecov.io/gh/cemsbr/yala/branch/master/graph/badge.svg
            :target: https://codecov.io/gh/cemsbr/yala

.. |codacy| image:: https://app.codacy.com/project/badge/Grade/30067434a90c41c097fdf83ce6a1b677
           :target: https://www.codacy.com/gh/cemsbr/yala/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cemsbr/yala&amp;utm_campaign=Badge_Grade

.. |issue_time| image:: http://isitmaintained.com/badge/resolution/cemsbr/yala.svg
               :target: http://isitmaintained.com/project/cemsbr/yala

.. |version| image:: https://img.shields.io/pypi/v/yala
            :alt: PyPI
            :target: https://pypi.org/project/yala/

.. |downloads| image:: https://img.shields.io/pypi/dm/yala
              :target: https://pypi.org/project/yala/
