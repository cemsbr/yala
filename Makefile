clean:
	rm -rf .eggs/ .tox/ build/ dist/ yala.egg-info/
upload:
	python setup.py sdist bdist_wheel upload -s
pip-update:
	@echo Upgrading packages...
	pip install -U -r requirements/install.in \
		       -r requirements/dev.in \
		       -r requirements/test.in
	@echo Updating requirement files...
	cd requirements && \
		for req in install dev test; do \
			pip-compile $$req.in > $$req.txt; \
		done
