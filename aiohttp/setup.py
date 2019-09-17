#!/usr/bin/env python

import os
from setuptools import setup


def read(readme_file):
    return open(os.path.join(os.path.dirname(__file__), readme_file)).read()


setup(
    name='aiohttp-jinja2-haggle',
    version='0.0.0',
    author='Ross Fenning',
    author_email='pypi@rossfenning.co.uk',
    py_modules=['aiohttp_jinja2_haggle'],
    description='HTTP content negotiation for aiohttp and jinja2.',
    url='http://github.com/avengerpenguin/aiohttp_jinja2_haggle',
    install_requires=['aiohttp', 'jinja2', 'accept-types', 'aiohttp-jinja2'],
    tests_require=[],
    setup_requires=[],
)
