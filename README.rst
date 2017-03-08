========
pyboleto
========
|travis| |pypi|

.. |travis| image:: https://secure.travis-ci.org/eduardocereto/pyboleto.png?branch=master
   :target: http://travis-ci.org/#!/eduardocereto/pyboleto
   
.. |pypi| image:: https://img.shields.io/pypi/v/pyboleto.svg
    :target: https://pypi.python.org/pypi/pyboleto/
 

.. _pyboleto-synopsis:

pyboleto provides a python class to generate "boletos de cobranca" as these
are the Brazilian equivalent for invoices.

It's easy to implement classes for new banks.

This class is still in development and currently has no documented API.

.. contents::
    :local:

.. _pyboleto-implemented-bank:

Implemented Banks
=================

You can help writing code for more banks or printing and testing current
implementations.

For now here's where we are.

 +----------------------+----------------+-----------------+------------+
 | **Bank**             | **Carteira /** | **Implemented** | **Tested** |
 |                      | **Convenio**   |                 |            |
 +======================+================+=================+============+
 | **Banco do Brasil**  | 18             | Yes             | Yes        |
 +----------------------+----------------+-----------------+------------+
 | **Banrisul**         | x              | Yes             | Yes        |
 +----------------------+----------------+-----------------+------------+
 | **Bradesco**         | 06, 03         | Yes             | Yes        |
 +----------------------+----------------+-----------------+------------+
 | **Caixa Economica**  | SR             | Yes             | No         |
 +----------------------+----------------+-----------------+------------+
 | **HSBC**             | CNR, CSB       | Yes             | No         |
 +----------------------+----------------+-----------------+------------+
 | **Itau**             | 157            | Yes             | Yes        |
 +----------------------+----------------+-----------------+------------+
 | **Itau**             | 175, 174, 178, | Yes             | No         |
 |                      | 104, 109       |                 |            |
 +----------------------+----------------+-----------------+------------+
 | **Real**             | 57             | Yes             | No         |
 +----------------------+----------------+-----------------+------------+
 | **Santander**        | 102            | Yes             | Yes        |
 +----------------------+----------------+-----------------+------------+
 | **Santander**        | 101, 201       | Yes             | No         |
 +----------------------+----------------+-----------------+------------+

.. _pyboleto-docs:

Documentation
=============

http://packages.python.org/pyboleto/

The best way to learn how to create Boletos using pyboleto is to look at the
examples at `pdf_pyboleto_sample.py`_ or `html_pyboleto_sample.py`_


.. _pdf_pyboleto_sample.py: https://github.com/eduardocereto/pyboleto/blob/master/bin/pdf_pyboleto_sample.py

.. _html_pyboleto_sample.py: https://github.com/eduardocereto/pyboleto/blob/master/bin/html_pyboleto_sample.py

.. _pyboleto-installation:

Installation
============

You can install pyboleto either via the Python Package Index (PyPI)
or from source.

To install using pip,::

    $ pip install pyboleto

To install using easy_install,::

    $ easy_install pyboleto


.. _pyboleto-installing-from-source:

Downloading and installing from source
--------------------------------------

Download the latest version of pyboleto from
http://pypi.python.org/pypi/pyboleto/

You can install it by doing the following,::

    $ tar xvfz pyboleto-0.0.0.tar.gz
    $ cd pyboleto-0.0.0
    $ python setup.py build
    # python setup.py install # as root

.. _pyboleto-installing-from-hg:

Using the development version
-----------------------------

You can clone the repository by doing the following::

    $ git clone https://github.com/eduardocereto/pyboleto.git

.. _pyboleto-unittests:

Executing unittests
===================

You need either setuptools or distribute in order to execute the tests. Chances are you already have one or another. You also need `pdftohtml`_.::

    $ cd pyboleto
    $ python setup.py test


.. _pdftohtml: http://poppler.freedesktop.org/

.. _pyboleto-license:

License
=======

This software is licensed under the `New BSD License`. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. vim:tw=0:sw=4:et
