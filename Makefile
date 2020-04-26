help:
	@echo 'Targets'
	@echo '======='
	@echo '      clean:  Remove generated files.'
	@echo '       help:  This message.'
	@echo '     upload:  Upload signed Python package to PyPI.'
	@echo -n '      watch:  When code changes, run tests.'
	@echo -n '  sonarqube:  Update SonarQube code metrics.'
	@echo ' Requires inotify-tools'

clean:
	rm -rf .eggs/ .tox/ build/ dist/ yala.egg-info/

upload: clean
	python setup.py clean sdist bdist_wheel
	twine upload dist/*

watch:
	while [ true ]; do \
		coverage run setup.py test; \
		coverage report; \
		inotifywait -e move_self -e modify -r --exclude .git .; \
	done

sonarqube:
	# Analyze code and upload results to SonarQube
	# Requires sonar-scanner
	coverage run --source=yala setup.py test
	coverage xml -i
	nosetests --with-xunit
	pylint yala -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" >pylint-report.txt
	sonar-scanner
