"""Alexa MD python package configuration."""

from setuptools import setup

setup(
    name='alexamd_upload',
    version='0.1.0',
    packages=['alexamd_upload'],
    include_package_data=True,
    install_requires=[
        'flask',
        'boto',
        'boto3',
        'numpy',
        'pypng',
        'pydicom',
        'numpngw'
    ],
    tests_require=[
        'bs4',
        'requests'
    ],
    test_suite='alexamd_upload.tests'
)
