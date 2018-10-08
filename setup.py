"""Alexa MD python package configuration."""

from setuptools import setup

setup(
    name='alexamd',
    version='0.1.0',
    packages=['alexamd'],
    include_package_data=True,
    install_requires=[
        'Flask==0.12.1',
        'Flask-Ask==0.9.8',
        'boto==2.49.0',
        'boto3==1.9.18',
        'cryptography<2.2'
    ],
)
