#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest


def suite():
    """suite that tests all banks"""
    def my_import(name):
        # See http://docs.python.org/lib/built-in-funcs.html#l2h-6
        components = name.split('.')
        try:
            # python setup.py test
            mod = __import__(name)
            for comp in components[1:]:
                mod = getattr(mod, comp)
        except ImportError:
            # python tests/alltests.py
            mod = __import__(components[1])
        return mod

    modules_to_test = [
        'tests.test_banco_banrisul',
        'tests.test_banco_bradesco',
        'tests.test_banco_caixa',
        'tests.test_banco_do_brasil',
        'tests.test_banco_hsbc',
        'tests.test_banco_hsbc_com_registro',
        'tests.test_banco_itau',
        'tests.test_banco_real',
        'tests.test_banco_santander',
    ]
    alltests = unittest.TestSuite()
    for module in [my_import(x) for x in modules_to_test]:
        alltests.addTest(module.suite)
    return alltests


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
