lint:
	black *.py fixedWidthParser/*.py
	flake8 fixedWidthParser/*.py --ignore=E203
