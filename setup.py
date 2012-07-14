# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys


extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True
    #extra['convert_2to3_doctests'] = ['src/your/module/README.txt']
    #extra['use_2to3_fixers'] = ['your.fixers']
    extra['tests_require'] = [
        'pep8>=0.6.1',
        'pep8<1.3',
    ],
else:
    extra['install_requires'] = [
        'reportlab>=2.5',
    ]
    extra['tests_require'] = [
        'pep8>=0.6.1',
        'pep8<1.3',
        'pyflakes>=0.5.0',
    ]

setup(
    name='pyboleto',
    version='0.2.5',
    author='Eduardo Cereto Carvalho',
    author_email='eduardocereto@gmail.com',
    url='https://github.com/eduardocereto/pyboleto',
    packages=find_packages(),
    package_data={
        '': ['LICENSE'],
        'pyboleto': ['media/*.jpg'],
    },
    zip_safe=False,
    provides=[
        'pyboleto'
    ],
    license='BSD',
    description='Python Library to create "boletos de cobrança bancária" for several Brazilian banks',
    long_description=open('README.rst', 'r').read(),
    download_url='http://pypi.python.org/pypi/pyboleto',
    scripts=['bin/pyboleto_sample.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Portuguese (Brazilian)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.6',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
    test_suite='tests.alltests.suite',
    **extra
)
