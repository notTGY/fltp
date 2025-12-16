REGEX ?= a|b
HARD ?= ((abb*a)|bb*)*

test:
	python3 -m unittest discover -s tests

run:
	python3 main.py --verbose "$(REGEX)"

hard:
	python3 main.py "$(HARD)"
