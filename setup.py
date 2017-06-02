"""A setuptools based setup module."""
from os import path

from setuptools import setup

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESC = f.read()

setup(
    name='yala',
    version='1.0.0b2',
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='linter check quality',
    packages=['yala'],
    install_requires=[
        'isort>=4.2.13',
        'pycodestyle>=2.3.1',
        'pydocstyle>=2.0.0',
        'pyflakes>=1.5.0',
        'pylint>=1.7.1',
        'radon>=2.0.1'
    ],
    # $ pip install -e .[dev,test]
    extras_require={
        'test': [
            'coverage',
            'tox'
        ],
    },
    package_data={
        'yala': ['setup.cfg']
    },
    entry_points={
        'console_scripts': [
            'yala=yala.main:main',
        ],
    },
)
