install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

page_loader:
	poetry run page_loader

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest --cov=page_loader --cov-report xml tests/	

.PHONY: install build package-install page_loader lint test
