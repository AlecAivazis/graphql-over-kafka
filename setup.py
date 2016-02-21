#! /usr/bin/env python3

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name = 'nautilus',
    version = '0.3.4',
    description = 'A library for creating microservice applications',
    author = 'Alec Aivazis',
    author_email = 'alec@aivazis.com',
    url = 'https://github.com/aaivazis/nautilus',
    download_url = 'https://github.com/aaivazis/nautilus/tarball/0.3.2',
    keywords = ['microservice', 'flask', 'graphql'],
    classifiers = [],
    test_suite = 'nose2.collector.collector',
    packages = find_packages(exclude=['example', 'tests']),
    install_requires = [
        'bcrypt',
        'flask',
        'flask_admin',
        'flask_cors',
        'flask_graphql',
        'flask_jsontools',
        'flask_login',
        'flask_script',
        'flask_sqlalchemy',
        'flask_wtf',
        'graphene',
        'sqlalchemy',
        'nose2',
        'pika',
        'python-consul',
        'singledispatch',
        'wtforms',
    ]
)
