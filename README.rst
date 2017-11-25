|Travis| |Coverage| |Code Health| |PyPI Version|

GitHub Token
============

Creating an app token might not be the simplest task, use this utility
and forget about all the issues.

Install
=======

``pip install github_token``

Usage
=====

::

        import github_token
        user = input("Username: ")
        password = getpass.getpass()
        app_name = input("App Name to create: ")
        token_factory = github_token.TokenFactory(user, password, app_name,
                                                  github_token.Scopes.all)

        print(token_factory(
            tfa_token_callback=lambda: input("TFA Token: ")
        ))

Develop
=======

When working locally in the project

Test
----

::

        python3 -m venv venv3
        . venv3/bin/activate
        python3 -m pip install -r dev-requirements.txt
        python3 -m pytest tests.py

Release
-------

::

        rm -rf dist/*
        python3 -m pip install twine
        python3 setup.py sdist bdist_wheel
        twine upload dist/*

.. |PyPI Version| image:: https://img.shields.io/pypi/v/github_token.svg
   :target: https://pypi.python.org/pypi/github_token/
.. |Code Health| image:: https://landscape.io/github/mariocj89/github-token/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mariocj89/github-token/master
.. |Coverage| image:: https://coveralls.io/repos/github/mariocj89/github-token/badge.svg?branch=master
   :target: https://coveralls.io/github/mariocj89/github-token?branch=master
.. |Travis| image:: https://travis-ci.org/mariocj89/github-token.svg?branch=master
   :target: https://travis-ci.org/mariocj89/github-token
