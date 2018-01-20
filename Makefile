help:
	@echo 'Targets'
	@echo '======='
	@echo '      clean:  Remove generated files.'
	@echo '       help:  This message.'
	@echo "update-deps:  Update dev packages' pinned versions."
	@echo '     upload:  Upload signed Python package to PyPI.'
	@echo -n '      watch:  When code changes, run tests.'
	@echo ' Requires inotify-tools'

clean:
	rm -rf .eggs/ .tox/ build/ dist/ yala.egg-info/

update-deps:
	@echo Upgrading packages...
	pip-compile -Uo requirements/dev.txt requirements/dev.in >/dev/null
	@sed -i -e 's/^-e file.*/-e ./' requirements-dev.txt
	git diff requirements/dev.txt

upload: clean
	python setup.py clean sdist bdist_wheel upload -s

watch:
	while [ true ]; do \
		coverage run setup.py test; \
		coverage report; \
		inotifywait -e move_self -e modify -r --exclude .git .; \
	done
