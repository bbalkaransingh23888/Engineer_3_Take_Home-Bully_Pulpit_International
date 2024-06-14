args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

build:
	@echo "Installing dependencies..."
	@if [ -z "$(shell which pipenv)" ]; then \
		echo "Pipenv is not installed. Installing it..."; \
		pip3 install pipenv --user; \
	fi
	@pipenv install

test:
	@echo "Running tests..."
	@pipenv run pytest

run:
	@echo "Running the application..."
	@pipenv run python -m src.cli $(call args,)

clean-up:
	@echo "Cleaning up..."
	@pipenv --rm
	@pip uninstall pipenv