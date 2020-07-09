import setuptools

from ivy_cms import __about__ as project

PACKAGES = setuptools.find_packages(
    exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
)


REQUIREMENTS = ["tabulate", "tablib", "xlrd", "xlwt"]

DEV_REQUIREMENTS = ["black", "prospector", "pre-commit", "pytest", "rope"]

OPTIONAL_DEPENDECIES = {"dev": DEV_REQUIREMENTS}


TEAM_NAME = "Your Team"
TEAM_EMAIL = "developers@ubitec.com"

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "License :: Copyright (C) ubitec AG",
    "Operating System :: OS Independent",
]


setuptools.setup(
    name=project.name,
    version=project.version,
    author=TEAM_NAME,
    author_email=TEAM_EMAIL,
    description=project.description,
    long_description=project.long_description,
    long_description_content_type="text/markdown",
    url="https://ubitec.io/",
    packages=PACKAGES,
    install_requires=REQUIREMENTS,
    extras_require=OPTIONAL_DEPENDECIES,
    classifiers=CLASSIFIERS,
)
