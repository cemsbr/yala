YALA - Yet Another Linter Aggregator
====================================

|Travis| |coveralls|

YALA combines many linters to improve the quality of your code. Other projects may come to your mind, but does anyone have all the features below?

Works with latest linters
    Yala uses linters' outputs and doesn't depend on their code.
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
Requires Python >= 3.6.

.. code-block:: bash

  sudo pip3.6 install --upgrade yala

If you are willing to hack yala's code, run the command below in this README's folder:

.. code-block:: bash

  sudo pip3.6 install -e .[dev,test]


Usage
-----
Just call ``yala`` followed by the files and/or folders to lint.

Linters' options
................

You can configure the linters as explained in their docs (e.g. *isort* section in *setup.cfg*). To change the **command line options** for a linter, create a *setup.cfg* file in the same folder you run yala from. The default configuration is in the file ``yala/setup.cfg`` that you can copy and customize (you can remove unchanged lines). For example, to output grades C and lower for Radon Maintainability Index (default is D and lower), add the following to *setup.cfg*:

.. code-block:: ini

  [yala]
  radon mi args = --min C
  pylint args = --disable=TODO

Besides "radon mi", it's possible to define cli options for "isort", "pycodestyle", "pydocstyle", "pyflakes", "pylint" and "radon cc" (the names are exactly as they are called in command line). Of course, you can still use other means provided by each linter (e.g. "isort" section).

Adding a linter
---------------
Check the file *yala/linters.py* and feel free to ask for help.


.. |Travis| image:: https://travis-ci.org/cemsbr/yala.svg?branch=master
           :target: https://travis-ci.org/cemsbr/yala
.. |coveralls| image:: https://coveralls.io/repos/github/cemsbr/yala/badge.svg?branch=master
              :target: https://coveralls.io/github/cemsbr/yala?branch=master
