import imp
from os import path
from setuptools import setup

VERSION = imp.load_source(
    'version',
    path.join('.',
              'zunzuncito',
              'version.py'))

VERSION = VERSION.__version__

readme = open('README.rst', 'r')

setup(
    name='zunzuncito',
    version=VERSION,
    author='Nicolas Embriz',
    author_email='nbari@dalmp.com',
    description="A micro-framework for creating REST API's",
    license='BSD',
    keywords='wsgi web api framework rest http',
    url='http://www.zunzun.io',
    download_url='https://github.com/nbari/zunzuncito/tarball/master',
    platforms="any",
    packages=['zunzuncito'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    long_description=readme.read()
)
