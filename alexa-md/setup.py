"""Alexa MD python package configuration."""

from setuptools import setup

setup(
    name='alexamd',
    version='0.1.0',
    packages=['alexamd'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_ask',
        'boto',
        'boto3',
        'pyOpenSSL'
    ],
    tests_require=[
        'requests'
    ],
    test_suite='alexamd.tests'
)
