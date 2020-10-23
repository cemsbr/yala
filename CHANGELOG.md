# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.0.0] - 2020-10-23
## Changed
- Pylint's duplicate-code is not disabled anymore, since its parser has multi-line support.
- For yala devs: now, linter parsers receive both stdout and stderr. Reason: isort 5 prints results to stderr.

## Fixed
- Better support for isort 5:
  - No more `--recursive` flag;
  - Its output is now read from stderr instead of stdout.

## Removed
- Python 3.5 support (besides EOL, no isort-5 support)

## [2.2.1] - 2020-04-26
### Fixed
- Multiline results in pylint were not being captured, e.g. bad-whitespace and
  bad-continuation.
- Updated pyflakes output parser: now there's a column number.

### Changed
- Pipfile has Python 3.8 now that it is available in Ubuntu LTS 20.04. However,
  CI still tests under 3.5, 3.6, and 3.7, too.

## [2.2.0] - 2019-11-28
### Added
- Pylint as default (required) linter (as in v1)

## [2.1.0] - 2019-10-12
### Added
- Windows support

## [2.0.0] - 2019-10-10
### Added
- Flake8 support
- Pyflakes support
- Option to choose linters to install, or "all" (check README)

### Changed
- Install only isort and pycodestyle by default. For the old behaviour: `pip install yala[all]`

## [1.8.0] - 2019-10-06
### Added
- Radon is back - thanks CartoonFan [#136](https://github.com/cemsbr/yala/issues/136)
- Fixed linter issues

## [1.7.0] - 2018-08-25
### Added
- Support to pycodestyle >= 2.4.0

### Removed
- Radon (to support pycodestyle >= 2.4.0)
- Unused code to parse pyflakes and radon
- dev: dependency management via requirements file (use pipenv)

[Unreleased]: https://github.com/cemsbr/yala/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/cemsbr/yala/compare/v2.2.1...v3.0.0
[2.2.1]: https://github.com/cemsbr/yala/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/cemsbr/yala/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/cemsbr/yala/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/cemsbr/yala/compare/v1.8.0...v2.0.0
[1.8.0]: https://github.com/cemsbr/yala/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/cemsbr/yala/compare/v1.6.0...v1.7.0
