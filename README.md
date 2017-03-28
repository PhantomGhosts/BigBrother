<p align="center"><img alt="BigBrothe is watching you" src="docs/assets/logo.jpg" /></p>


[![Documentation Status](https://readthedocs.org/projects/bigbrother/badge/?version=latest)](http://bigbrother.readthedocs.io/en/latest/?badge=latest)
[![Code Climate](https://img.shields.io/codeclimate/github/PhantomGhosts/BigBrother.svg)](https://codeclimate.com/github/PhantomGhosts/BigBrother)
[![Github All Releases](https://img.shields.io/github/downloads/PhantomGhosts/BigBrother/total.svg)](https://github.com/PhantomGhosts/BigBrother/releases)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/PhantomGhosts/BigBrother/blob/master/LICENSE)

BigBrother is a collection of tools for the purpose of gaining information quietly.
With an embedded sqlite3 database to store all modules information and locations, thus not all modules need to be installed.

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

Integrations
============
Sentry
------
Sentry integartion can be found in:

	lib/sentry/sentry.py

It's installed to handle software-side issues.

Encryption
----------
Every tools is stored in a crypted tar.gz file on a server and the user needs an authentication key to install it.
The 'set' command is used to store own password.

Databases
=========
I'm unsure on which use:
* PostgreSQL
* MySQL

Or totally different:
* Redis

Commands
========
**coming soon**

New version 0.4.0 in pre-alpha phase.
Commands will come out in 0.4.0 alpha.

Setup
=====
**coming soon**

New version 0.4.0 in pre-alpha phase.
Setup file will come out in 0.4.0 alpha.

Contribute
=========
To contribute to this project please see [Contribute](docs/CONTRIBUTING.md).
