#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_bettertimeit
----------------------------------

Tests for `bettertimeit` module.
"""
import sys
import unittest
if not hasattr(unittest.TestCase, "assertRegexpMatches"):
    import unittest2 as unittest
from six import StringIO

from bettertimeit import bettertimeit


class redirect_stdout(object):
    """Context manager for temporarily redirecting stdout to another file

        # How to send help() to stderr
        with redirect_stdout(sys.stderr):
            help(dir)

        # How to write help() to a file
        with open('help.txt', 'w') as f:
            with redirect_stdout(f):
                help(pow)
    """

    def __init__(self, new_target):
        self._new_target = new_target
        # We use a list of old targets to make this CM re-entrant
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(sys.stdout)
        sys.stdout = self._new_target
        return self._new_target

    def __exit__(self, exctype, excinst, exctb):
        sys.stdout = self._old_targets.pop()


class TestBettertimeit(unittest.TestCase):

    def setUp(self):
        def timeit_func():
            a = range(10)

            def timeit_1():
                for i in a:
                    print(i**2)

        self.timeit_func = timeit_func

    def _test(self, target):
        f = StringIO()
        with redirect_stdout(f):
            bettertimeit(target, target_time=0.002)
        return f.getvalue()

    def test_basic_func(self):
        output = self._test(self.timeit_func)
        self.assertRegexpMatches(output, r"81")
        self.assertRegexpMatches(output, r"loops")

    def test_module(self):
        from . import module
        output = self._test(module)
        self.assertRegexpMatches(output, r"8")
        self.assertRegexpMatches(output, r"16")
        self.assertRegexpMatches(output, r"loops")
        self.assertEqual(2, output.count("loops"))

    def test_str(self):
        s = """\
        def timeit_1():
            pass
        """
        output = self._test(s)
        self.assertRegexpMatches(output, r"loops")

    def test_ast(self):
        import ast
        import inspect
        from . import module

        tree = ast.parse(inspect.getsource(module))

        output = self._test(tree)
        self.assertRegexpMatches(output, r"loops")

    def test_method(self):
        class C(object):
            def meth(self):
                a = 1
                b = 2
                def timeit_1():
                    a + b

        self._test(C.meth)
        self._test(C().meth)


if __name__ == '__main__':
    unittest.main()
