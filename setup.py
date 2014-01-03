import imp
from os import path
from setuptools import setup

VERSION = imp.load_source(
    'version',
    path.join('.',
              'zunzuncito',
              'version.py'))

VERSION = VERSION.version_commits

setup(
    name='zunzuncito',
    version=VERSION,
    author='Nicolas Embriz',
    author_email='nbari@dalmp.com',
    description="A micro-framework for creating REST API's.",
    license='BSD',
    keywords='wsgi web api framework rest http',
    url='https://github.com/nbari/zunzuncito',
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
)
