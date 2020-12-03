#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must install Twine:
#   $ pip install -r requirements_prod.txt

import io
import os
import subprocess
from shutil import rmtree

import sys
from setuptools import setup, Command

from pymocky import __version__

# Package meta-data.
NAME = "pymocky"
DESCRIPTION = "Send push notification from command line for single or multiple targets"
URL = "https://github.com/pymocky/pymocky"
EMAIL = "paulo@prsolucoes.com"
AUTHOR = "Paulo Coutinho"
REQUIRES_PYTHON = ">=3.5.0"
VERSION = __version__
LICENSE = "MIT"

# Packages required
REQUIRED = [
    "cherrypy>=18.0",
    "cherrypy_cors",
    "pyyaml",
    "watchdog",
    "colorama",
    "requests",
    "regex",
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    LONG_DESCRIPTION = "\n" + f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        subprocess.check_call(
            "{0} setup.py sdist bdist_wheel".format(sys.executable), shell=True
        )

        self.status("Uploading the package to PyPi via Twine…")
        subprocess.check_call("twine upload dist/*", shell=True)

        self.status("Pushing git tags…")
        subprocess.check_call("git tag v{0}".format(VERSION), shell=True)
        subprocess.check_call("git push origin v{0}".format(VERSION), shell=True)

        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=[NAME],
    entry_points={
        "console_scripts": ["pymocky=pymocky.cli:main"],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
