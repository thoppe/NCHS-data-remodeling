lint:
	black *.py fixedWidthParser/*.py
	flake8 fixedWidthParser/*.py --ignore=E203,E501
	python fixedWidthParser/build_README.py
