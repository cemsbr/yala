YALA - Yet Another Linter Aggregator
====================================

|build| |coveralls| |codecov| |codacy| |codeclimate| |sonarcloud| |issue_time|

YALA combines many linters to improve the quality of your code. Other projects may come to your mind, but does anyone have all the features below?

Works with latest linters
    Yala uses linters' outputs and doesn't break on API changes.
Same defaults
    No changes to linters' default configuration.
Easy to configure
    Set any command-line option for any linter (even pylint!) in one INI file: setup.cfg.
Language-agnostic
    Add any linter to any language.
Extensible
    Just a few lines do add your preferred linter.
Fast
    Run linters in parallel and sort output by filename and line number.

Current Status
--------------
For now, there are some Python linters available: isort, Pylint, Pycodestyle, Pydocstyle, Pyflakes and Radon (cyclomatic complexity and maintainability index).

Install
-------
Tested with Python >= 3.5.

.. code-block:: bash

  sudo pip3 install --upgrade yala

If you are willing to hack yala's code, run the command below in this README's folder:

.. code-block:: bash

  sudo pip3 install -e .[dev]


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
  radon mi args = --min C

Besides `pylint` and `radon mi`, you can define CLI options for `isort`, `pycodestyle`, `pydocstyle`, `pyflakes`, `pylint` and `radon cc` (the names are exactly as they are called in command line).


Choosing linters
................

Default linters are: isort, pycodestyle, pydocstyle, pylint, radon (cc/mi).
Optionals are: pyflakes and mypy (you need to install them manually). 

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


Hacking: Adding a linter
------------------------
Check the file *yala/linters.py* and feel free to ask for help.


.. |build| image:: https://semaphoreci.com/api/v1/cemsbr/yala/branches/master/shields_badge.svg
          :target: https://semaphoreci.com/cemsbr/yala

.. |coveralls| image:: https://coveralls.io/repos/github/cemsbr/yala/badge.svg?branch=master
              :target: https://coveralls.io/github/cemsbr/yala?branch=master

.. |codecov| image:: https://codecov.io/gh/cemsbr/yala/branch/master/graph/badge.svg
            :target: https://codecov.io/gh/cemsbr/yala

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/e435a65c5dd44ecf9369010b29616bd0
           :target: https://www.codacy.com/app/cems/yala?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cemsbr/yala&amp;utm_campaign=Badge_Grade

.. |codeclimate| image:: https://api.codeclimate.com/v1/badges/26b718c43a08555bf9c8/maintainability
                :target: https://codeclimate.com/github/cemsbr/yala/maintainability

.. |sonarcloud| image:: https://sonarcloud.io/api/badges/gate?key=github-com-cemsbr-yala
               :target: https://sonarcloud.io/dashboard?id=github-com-cemsbr-yala

.. |issue_time| image:: http://isitmaintained.com/badge/resolution/cemsbr/yala.svg
               :target: http://isitmaintained.com/project/cemsbr/yala
