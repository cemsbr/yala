clean:
	rm -rf build/ dist/ yala.egg-info/
build: clean
	python setup.py bdist_wheel
	python setup.py sdist
sign: build
	cd dist/ && \
	for file in yala-*.whl yala-*.tar.gz; do \
		gpg --detach-sign --armor $$file; \
	done
upload: sign
	cd dist/ && \
	for file in yala-*.whl yala-*.tar.gz; do \
		twine upload $$file $$file.asc; \
	done

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
