help:
	@echo 'Targets'
	@echo '======='
	@echo '     clean:  Remove generated files'
	@echo '      help:  This message'
	@echo 'pip-update:  Update dev pinned packages'
	@echo '    upload:  Upload signed Python package to PyPI'
	@echo -n '     watch:  After any source change, run Python unittest.'
	@echo ' Requires inotify-tools'

clean:
	rm -rf .eggs/ .tox/ build/ dist/ yala.egg-info/

pip-update:
	@echo Upgrading packages...
	pip-compile --upgrade --output-file requirements/run.txt
	pip-compile --upgrade --output-file requirements/dev.txt requirements/dev.in

upload: clean
	python setup.py clean sdist bdist_wheel upload -s

watch:
	while [ true ]; do \
		coverage run setup.py test; \
		coverage report; \
		inotifywait -e move_self -e modify -r --exclude .git .; \
	done
