========
pyboleto
========

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
 | `Bradesco`_          | 06             | Yes             | No         |
 +----------------------+----------------+-----------------+------------+
 | `Caixa Economica`_   | SR             | Yes             | No         |
 +----------------------+----------------+-----------------+------------+
 | `Real`_              | 57             | Yes             | No         |
 +----------------------+----------------+-----------------+------------+ 
 | `Banco do Brasil`_   | 18             | Yes             | No         |
 +----------------------+----------------+-----------------+------------+ 

.. _Bradesco: https://bitbucket.org/eduardo.cereto/pyboleto/wiki/BoletoBradesco
.. _Caixa Economica: https://bitbucket.org/eduardo.cereto/pyboleto/wiki/BoletoCaixa 
.. _Real: https://bitbucket.org/eduardo.cereto/pyboleto/wiki/BoletoReal
.. _Banco do Brasil: https://bitbucket.org/eduardo.cereto/pyboleto/wiki/BoletoBB


.. _pyboleto-docs:

Documentation
=============

Current documents are avilable here:

http://packages.python.org/pyboleto/

.. _pyboleto-installation:

Installation
============

You can install pyboleto either via the Python Package Index (PyPI)
or from source.

To install using `pip`,::

    $ pip install pyboleto

To install using `easy_install`,::

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

.. _pyboleto-license:

License
=======

This software is licensed under the `New BSD License`. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. vim:tw=0:sw=4:et
