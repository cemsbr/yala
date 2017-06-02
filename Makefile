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
