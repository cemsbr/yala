help:
	@echo 'Targets: clean, upload, pip-update.'

clean:
	rm -rf .eggs/ .tox/ build/ dist/ yala.egg-info/

upload:
	python setup.py sdist bdist_wheel upload -s

pip-update:
	@echo Upgrading packages...
	pip-compile --upgrade --output-file requirements/run.txt
	pip-compile --upgrade --output-file requirements/dev.txt requirements/dev.in
