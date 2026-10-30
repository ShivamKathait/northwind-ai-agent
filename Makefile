PY ?= python3

.PHONY: run test

run:
	PYTHONPATH=src $(PY) -m consol.run --data data --out output

test:
	$(PY) -m pytest -q
