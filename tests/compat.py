# -*- coding: utf-8 -*-
import unittest


def _skipIf(check, message=''):
    def _deco(meth):
        if check:
            return lambda *a, **kw: None
        else:
            return meth
    return _deco

if hasattr(unittest, 'skipIf'):
    skipIf = unittest.skipIf
else:
    skipIf = _skipIf
