#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

test_requirements = []

extra_requirements = {
    ':python_version == "2.7"': [
        'singledispatch',
    ],
}

setup(
    name='pydatapipes',
    version='0.1.0',
    description="Python data pipelines",
    long_description=readme + '\n\n' + history,
    author="Jan Schulz",
    author_email='jasc@gmx.net',
    url='https://github.com/janschulz/pydatapipes',
    packages=[
        'pydatapipes',
    ],
    package_dir={'pydatapipes': 'pydatapipes'},
    include_package_data=True,
    install_requires=requirements,
    extras_require=extra_requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pydatapipes',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
