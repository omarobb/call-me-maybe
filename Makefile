.PHONY: install env run clean debug lint 
path = $(shell pwd)

all: env run

env:
	cd /goinfre/$(USER)/ &&\
	mkdir call -p && \
	cd call && \
	python3 -m venv .venv && \
	ln -s -f /goinfre/$(USER)/call/.venv $(path)
	export UV_LINK_MODE=copy

install:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync

run:
	uv run python -m src --functions_definition data/input/functions_definition.json \
									   --input data/input/function_calling_tests.json \
									   --output data/output/function_calls.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

debug:
	uv run python -m pdb -m src

lint:
	flake8 . 
	mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs
