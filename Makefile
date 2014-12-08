test:
	venv/bin/nosetests --color --nologcapture inspector/

test_cover:
	venv/bin/nosetests --with-coverage --cover-package=inspector/

ci_test:
	nosetests --with-coverage --cover-package=inspector --color inspector/
	make pep8
	make pyflakes

pep8:
	pep8 --max-line-length=119 --show-source inspector/

pyflakes:
	pylama -l pyflakes inspector/

install:
	mkdir venv && echo "Virtualenv directory was created!"
	virtualenv --no-site-packages --prompt="(social-inspector)" venv
	venv/bin/pip install -r requirements.txt
	venv/bin/python -c "import nltk; nltk.download('punkt')"
