#! /usr/bin/python3

from setuptools import setup

setup(
    name = 'glue',
    version = '2.0.0',
    license = 'MIT',
    author="Daniel Filonik",
    author_email = 'daniel.filonik@qut.edu.au',
    description = 'Python OpenGL Utilities and Extensions.',
    url = 'http://github.com/filonik/glue',
    packages = [
        'glue',
        'glue.gl',
        'glue.wgl',
    ],
)