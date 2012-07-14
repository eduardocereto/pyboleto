# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2011-2012 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##
"""Test pyflakes on stoq, stoqlib and plugins directories

Useful to early find syntax errors and other common problems.

"""
import _ast
import sys
import unittest

from .testutils import SourceTest
from .compat import skipIf


try:
    from pyflakes import checker
except ImportError as err:
    if sys.version_info >= (3,):
        pass  # Pyflakes doesn't support Python3
    else:
        raise(err)


@skipIf(sys.version_info >= (3,),
        "Pyflakes unavailable on this version")
class TestPyflakes(SourceTest, unittest.TestCase):
    def setUp(self):
        pass

    # stolen from pyflakes
    def _check(self, codeString, filename, warnings):
        try:
            tree = compile(codeString, filename, "exec", _ast.PyCF_ONLY_AST)
        except (SyntaxError, IndentationError) as value:
            msg = value.args[0]

            (lineno, offset, text) = value.lineno, value.offset, value.text

            # If there's an encoding problem with the file, the text is None.
            if text is None:
                # Avoid using msg, since for the only known case, it contains a
                # bogus message that claims the encoding the file declared was
                # unknown.
                print >> sys.stderr, "%s: problem decoding source" % (
                    filename,
                )
            else:
                line = text.splitlines()[-1]

                if offset is not None:
                    offset = offset - (len(text) - len(line))

                print >> sys.stderr, '%s:%d: %s' % (filename, lineno, msg)
                print >> sys.stderr, line

                if offset is not None:
                    print >> sys.stderr, " " * offset, "^"

            return 1
        except UnicodeError as msg:
            print >> sys.stderr, 'encoding error at %r: %s' % (filename, msg)
            return 1
        else:
            # Okay, it's syntactically valid.
            # Now parse it into an ast and check it.
            w = checker.Checker(tree, filename)
            warnings.extend(w.messages)
            return len(warnings)

    def check_filename(self, root, filename):
        warnings = []
        msgs = []
        result = 0
        try:
            fd = open(filename, 'U')
            try:
                result = self._check(fd.read(), filename, warnings)
            finally:
                fd.close()
        except IOError as msg:
            print >> sys.stderr, "%s: %s" % (filename, msg.args[1])
            result = 1

        warnings.sort(key=lambda w: w.lineno)
        for warning in warnings:
            msg = str(warning).replace(root, '')
            print msg
            msgs.append(msg)
        if result:
            raise AssertionError(
                "%d warnings:\n%s\n" % (len(msgs), '\n'.join(msgs), ))

suite = unittest.TestLoader().loadTestsFromTestCase(TestPyflakes)

if __name__ == '__main__':
    unittest.main()
