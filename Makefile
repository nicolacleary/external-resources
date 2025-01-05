.venv:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install .[dev]


build_qa: .venv
	.venv/bin/ruff check external_resources tests
	.venv/bin/ruff format external_resources tests \
		--check --line-length 120
	.venv/bin/mypy external_resources tests \
		--strict
	.venv/bin/pytest tests


# TODO
build_wheel:
	echo "TODO"
