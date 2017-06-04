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
	@echo setup.py
	@echo --------
	@rg -o "        '\w+>=\d.+'" setup.py | cut -d"'" -f2 | sort
	@echo
	@echo Current
	@echo -------
	@pip freeze | grep -E "`rg -o "        '\w+>=\d.+'" setup.py | cut -d"'" -f2 | cut -f1 -d'>' | sort | xargs | sed -e 's/ /|/g' | tail -n 1`" | sed -e 's/==/>=/'
