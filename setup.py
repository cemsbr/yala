"""A setuptools based setup module."""
from os import path

from setuptools import setup

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESC = f.read()

def read_packages(basename):
    """Return list of packages from a file with requirements.

    Remove in-line comments.
    """
    filename = f'requirements/{basename}.txt'
    if not path.exists(filename):
        return []
    with open(filename) as lines:
        return [line.split()[0] for line in lines
                if not line.startswith('#')]

requires = {r:read_packages(r) for r in ('install', 'test', 'dev')}

setup(
    name='yala',
    version='1.0.0rc1',
    description='Yet Another Linter Aggregator',
    long_description=LONG_DESC,
    url='https://github.com/cemsbr/yala',
    author='Carlos Eduardo Moreira dos Santos',
    author_email='cems@cemshost.com.br',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='linter check quality',
    packages=['yala'],
    install_requires=requires['install'],
    # $ pip install -e .[dev,test]
    extras_require={
        'test': requires['test'],
        'dev': requires['dev']
    },
    package_data={
        'yala': ['setup.cfg'],
    },
    entry_points={
        'console_scripts': [
            'yala=yala.main:main',
        ],
    },
)
