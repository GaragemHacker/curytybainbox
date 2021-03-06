clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

test:
	python setup.py test

release: clean
	git tag `python setup.py -q version`
	git push origin `python setup.py -q version`
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*

deploy:
	systemctl stop curytybainboxweb
	systemctl stop curytybainboxd
	python setup.py install
	systemctl start curytybainboxd
	systemctl start curytybainboxweb

stop:
	systemctl stop curytybainboxweb
	systemctl stop curytybainboxd
	python shutdown.py

start:
	systemctl start curytybainboxd
	systemctl start curytybainboxweb
