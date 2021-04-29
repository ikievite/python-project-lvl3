build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

page_loader:
	poetry run page_loader

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest

.PHONY: build package-install page_loader lint test
