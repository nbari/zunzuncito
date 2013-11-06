import imp
import sys
from os import path
from setuptools import setup

VERSION = imp.load_source(
    'version',
    path.join('.',
              'zunzuncito',
              'version.py'))

VERSION = VERSION.__version__

setup(
    name='zunzuncito',
    version=VERSION,
    author='Nicolas Embriz',
    author_email='nbari@dalmp.com',
    description='A micro-framework for creating REST APIs.',
    license='BSD',
    keywords='wsgi web api framework rest http',
    url='https://github.com/nbari/zunzuncito',
    packages=['zunzuncito'],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: BSD License',
    ],
)
