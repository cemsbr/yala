"""A setuptools based setup module."""
from os import path

from setuptools import setup

from yala import __version__

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.rst')) as f:
    LONG_DESC = f.read()

setup(
    name='yala',
    version=__version__,
    description='Yet Another Linter Aggregator',
    long_description=LONG_DESC,
    url='https://github.com/cemsbr/yala',
    author='Carlos Eduardo Moreira dos Santos',
    author_email='cems@cemshost.com.br',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='linter check quality',
    packages=['yala'],
    install_requires=[
        'docopt',
        'isort',
        'pycodestyle',
        'pydocstyle',
        'pylint',
    ],
    # $ pip install -e .[dev]
    extras_require={
        'dev': [
            # https://bitbucket.org/ned/coveragepy/issues/578/
            # incomplete-file-path-in-xml-report
            'bandit',
            'coverage<4.4',
            'eradicate',
            'pip-tools',
            'pipenv',
            'rstcheck',
            'safety',
            'tox',
        ]
    },
    package_data={
        'yala': ['setup.cfg', 'logging.ini'],
    },
    entry_points={
        'console_scripts': [
            'yala=yala.main:main',
        ],
    },
    test_suite='tests',
)
