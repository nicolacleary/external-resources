.venv:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install .[dev]


# TODO - verfiy
build_qa:
	# TODO - replace with ruff
	.venv/bin/flake8 external_resources tests \
		--max-line-length 120
	.venv/bin/black external_resources tests \
		--line-length 120 --check
	.venv/bin/mypy external_resources tests
	.venv/bin/pytest tests


# TODO
build_wheel:
	echo "TODO"
