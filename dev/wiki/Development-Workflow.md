## Generating Documentation from Docstrings

1. From the `satchecker/src` directory run `sphinx-apidoc -o ../docs/source/ . ./satchecker.py`
2. From the `satchecker/docs` directory run `make html`
3. Make sure everything looks correct from `satchecker/docs/build/html/index.html`. Only the .rst files are part of source control - live documentation is updated from the `main` branch only.

## Formatting and Linting
Right now the code is set up to use [Black](https://black.readthedocs.io/en/stable/) for code formatting and [Ruff](https://docs.astral.sh/ruff/) for linting with the following rules turned on:
* E (pycodestyle errors)
* F (Pyflakes)
* I (isort)
* N (pep8-naming)
* UP (pyupgrade)
* S (flake8-bandit)
* B (flake8-bugbear)

Ruff and Black can be set up to run as pre-commit hooks, but they are also run on every push to a branch in the run_tests.yml workflow (which also runs all the tests)

## Type Checking
Type checking is done with [mypy](https://mypy.readthedocs.io/en/stable/).
To run type checking, run `mypy .` from the root satchecker directory.

## Deployment
Deployment is managed by NOIRLab IT using Kubernetes in AWS to manage containers with the API, Celery, and Redis - merges to `develop` are deployed to our develop/testing environment here: https://dev.satchecker.cps.iau.noirlab.edu/, and merges to the `main` branch will be deployed to the official version here: https://satchecker.cps.iau.org/
