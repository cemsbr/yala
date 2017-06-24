clean:
	rm -rf .eggs/ .tox/ build/ dist/ yala.egg-info/
upload:
	python setup.py sdist bdist_wheel upload -s
pip-update:
	@echo Upgrading packages...
	pip install -U .
	pip install -U -r requirements/dev.in -r requirements/test.in
	@echo Updating requirement files...
	pip-compile --output-file requirements/install.txt
	cd requirements && \
		pip-compile  dev.in >  dev.txt; \
		pip-compile test.in > test.txt; \
