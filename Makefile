clean:
	rm -rf .eggs/ .tox/ build/ dist/ yala.egg-info/
upload:
	python setup.py sdist bdist_wheel upload -s
pip-update:
	@echo Upgrading packages...
	pip install -U .
	cd requirements && pip install -U -r dev.in -r test.in
	@echo Updating requirement files...
	pip-compile --output-file requirements/install.txt >/dev/null
	cd requirements && \
		pip-compile  dev.in >  dev.txt; \
		pip-compile test.in > test.txt; \
