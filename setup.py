#! /usr/bin/env python3

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='nautilus',
    version='0.4.8',
    description='A library for creating microservice applications',
    author='Alec Aivazis',
    author_email='alec@aivazis.com',
    url='https://github.com/AlecAivazis/nautilus',
    download_url='https://github.com/aaivazis/nautilus/tarball/0.4.7',
    keywords=['microservice', 'tornado', 'graphql'],
    test_suite='nose2.collector.collector',
    packages=find_packages(exclude=['example', 'tests']),
    include_package_data=True,
    entry_points={'console_scripts': [
        'naut = nautilus.management:cli',
    ]},
    install_requires=[
        'bcrypt',
        'click',
        'tornado',
        'peewee',
        'graphene',
        'jinja2',
        'nose2',
        'pika',
        'python-consul',
        'wtforms',
    ]
)
