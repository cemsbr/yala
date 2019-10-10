# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/cemsbr/yala/compare/v1.2.0...HEAD
[2.0.0]: https://github.com/cemsbr/yala/compare/v1.8.0...v2.0.0
[1.8.0]: https://github.com/cemsbr/yala/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/cemsbr/yala/compare/v1.6.0...v1.7.0
