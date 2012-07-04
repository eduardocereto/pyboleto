# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = 'pyboleto',
    version = __import__('pyboleto').__version__,
    author = 'Eduardo Cereto Carvalho',
    author_email = 'eduardocereto@gmail.com',
    url = 'https://github.com/eduardocereto/pyboleto',
    packages = find_packages(),
    package_data = {
        '': ['LICENSE'],
        'pyboleto': ['media/*.jpg'],
    },
    zip_safe = False,
    install_requires = [
        'reportlab>=2.5',
    ],
    provides = [
        'pyboleto'
    ],
    license = 'BSD',
    description = 'Python Library to create "boletos de cobrança bancária" for several Brazilian banks',
    long_description = open('README.rst', 'r').read(),
    download_url = 'http://pypi.python.org/pypi/pyboleto',
    scripts = ['bin/pyboleto_sample.py'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Portuguese (Brazilian)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests.alltests.suite',
)

