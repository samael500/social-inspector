test:
	. venv/bin/activate; nosetests --color --nologcapture inspector/

ci_test:
	nosetests --with-coverage --cover-package=inspector --color inspector/
	make pep8
	make pyflakes

pep8:
	pep8 --max-line-length=119 --show-source inspector/

pyflakes:
	pylama -l pyflakes inspector/
