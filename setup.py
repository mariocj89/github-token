#!/usr/bin/env python
from setuptools import setup
LONG_DESCRIPTION="GitHub Helper to create auth tokens"

try:
    # attempt to build a long description from README.md
    # run sudo apt-get install pandoc and pip install pypandoc first
    import pypandoc
    LONG_DESCRIPTION=pypandoc.convert('README.md', 'rst')
except (ImportError, RuntimeError, OSError):
    pass


setup(
    name='github_token',
    packages=['github_token'],
    version='0.1.0',
    description='Library to create github personal auth token',
    long_description=LONG_DESCRIPTION,
    author='Mario Corchero',
    author_email='mariocj89@gmail.com',
    url='https://github.com/Mariocj89/github_token',
    keywords=['github', 'authorization', 'tfa', 'token', 'twofactor'],
    license='MIT',
    test_suite='nose.collector',
    use_2to3=True,
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'github_token=github_token.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Version Control',
    ],
)
