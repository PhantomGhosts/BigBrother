<p align="center"><img alt="BigBrothe is watching you" src="docs/assets/logo.jpg" /></p> 

[![Documentation Status](https://readthedocs.org/projects/bigbrother/badge/?version=latest)](http://bigbrother.readthedocs.io/en/latest/?badge=latest)
[![MIT License](https://img.shields.io/badge/license-MIT-000000.svg)](LICENSE)

BigBrother is a collection of tools for the purpose of gaining information quietly.

Versioning
==========
The Semantic Versioning is used in this repository in this format:

	[major].[minor].[patch]-{status}

* **major** indicates incopatible changes
* **minor** indicates new features
* **patch** indicates bug fixies
* **status** show the status (alpha, beta, rc, etc.)

for more information see [Semantic Versioning](http://semver.org/)

Tools
=====
Tools are divided based on this [**Nomenclature**](docs/nomenclature.md).

## Encryption
Every tools is stored in a crypted tar.gz file on a server and the user needs an authentication key to install it.
The 'set' command is used to store own password.

Commands
========

	set <password>

The **set** command is used to set own secret password to decrypt the modules

	get <module>

The **get** command is used to download the module from the server.

Setup
=====
Extract all files from the archive, then pip to install all required dependencies:

	pip install -r requirements.txt

Then launch 'setup.py':

	python setup.py

This will install BigBrother by default in "/usr/share/BigBrother"

Contribute
=========
To contribute to this project please see [Contribute](docs/CONTRIBUTING.md).
