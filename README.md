# `axonivy-cms-export`

A small tool to export Axon.ivy Project's CMS into Excel file without using Axon.ivy Designer.

## Install

You need Python 3.7+
This tool uses "tablib" and its extra "xls" to create the Excel file.

```bash
$ pip install https://github.com/Genzer/axonivy-cms-export/archive/{{ version }}.tar.gz
```

## Usage

```bash
❯ python -m ivy_cms.export -h
usage: export.py [-h] project output

Export Axon.ivy Project's CMS

positional arguments:
  project     Path to the Axon.ivy Project
  output      Path to the output file

optional arguments:
  -h, --help  show this help message and exit
```

## Develop

If you choose to have a local virtual environment that is project-specific (recommended), that will be located at `.venv/` (unless other constraints on the project prevent you from doing that).

Using the correct python version, you would then run

```sh
python --version #make sure it is the version you want the project to follow, It must be >=3.5
python -m venv .venv

source ./.venv/bin/activate
```

## Running tests

To run tests, we expect the following command to find and run all commands.

```sh
python -m unittest discover
```

## Development dependencies

Development dependancies are installed with

```sh
pip install -e .[dev]
```

## Committing code

To commit code, make sure you have the pre-commit hooks installed. For that, after you have installed the dev dependancies, it will have install [*pre-commit*](https://pre-commit.com/hooks.html). To install the hooks do the following

```sh
pre-commit install
```

If you just want to run the checks,
```sh
pre-commit run --all-files
```

Nonetheless, on commit, it will check that the checks are passed. If they are not, some of the hooks related only to formatting will have modified the files, so you need to add those changes as well

```sh
# Example
git commit -m "Simple commit with a nondescriptive message"
# > ERROR: <file> Imports are incorrectly sorted.
# > Fixing <file>
# > [WARNING] Stashed changes conflicted with hook auto-fixes... Rolling back fixes...
# > INFO] Restored changes from ...
git add .
git commit -m "Even less descriptive message"
# And now it should work, as long as the error is not something it couldn't fix
```
