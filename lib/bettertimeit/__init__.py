#!/usr/bin/env python
from __future__ import print_function
import ast
import inspect
import types
import textwrap
import timeit

import six
import astunparse


__author__ = 'Simon Percivall'
__email__ = 'percivall@gmail.com'
__version__ = '1.1.2'

__all__ = ["bettertimeit"]


func_name_prefix = "timeit_"


class TimeitHolder(object):

    def __init__(self, name, setup, code):
        """
        :type setup: str | unicode
        :type code: str | unicode
        """
        self.name = name
        self.setup = setup
        self.code = code
        self._timer = None

    @property
    def timer(self):
        if not self._timer:
            self._timer = timeit.Timer(stmt=self.code, setup=self.setup)
        return self._timer

    def timeit(self, number=timeit.default_number):
        print(self.timer.timeit(number))

    def repeat(self, repeat=3, target_time=0.2):
        try:
            number = self._determine_number(target_time)
            r = self.timer.repeat(repeat=repeat, number=number)
        except:
            self.timer.print_exc()
            return

        best = min(r)
        print("%s: %d loops," % (self.name, number), end=' ')

        precision = 3
        usec = best * 1e6 / number
        if usec < 1000:
            print("best of %d: %.*g usec per loop" % (repeat, precision, usec))
        else:
            msec = usec / 1000
            if msec < 1000:
                print("best of %d: %.*g msec per loop" % (repeat, precision, msec))
            else:
                sec = msec / 1000
                print("best of %d: %.*g sec per loop" % (repeat, precision, sec))

    def _determine_number(self, target_time):
        # determine number so that 0.2 <= total time < 2.0
        for i in range(1, 10):
            number = 10 ** i
            x = self.timer.timeit(number)
            if x >= target_time:
                break
        return number

    def __str__(self):
        return self.timer.src

    def __repr__(self):
        return "<TimeitHolder %s>" % str(self)


def find_timeits(tree):
    """
    :param ast.AST tree: The container of one or more timeit_funcs.
    :rtype: list[TimeitHolder]

    The ``tree` may be:
        * an ast.Module containing the ``timeit_func``
        * an ast.Module containing a function containing the ``timeit_func``
        * the ``timeit_func`` directly as an ast.FunctionDef

    An AST parse tree will usually be an ast.Module, containing one or more
    items. But this function could also receive the timeit_func directly,
    or it could be nested within a function in the ast.Module.
    """
    setup = []
    timeits = []

    isfunc = lambda o: isinstance(o, ast.FunctionDef)

    # unwrap a top module containing only a function
    if isinstance(tree, ast.Module) and len(tree.body) == 1:
        tree = tree.body[0]

    if not hasattr(tree, 'body'):
        raise TypeError("Can't handle '%s'" % type(tree))

    # we might have the timeit func directly
    if isfunc(tree) and tree.name.startswith(func_name_prefix) \
            and not any(c for c in tree.body if isfunc(c)):
        timeits.append(TimeitHolder(name=tree.name[len(func_name_prefix):],
                                    setup="",
                                    code=astunparse.unparse(tree.body)))
    else:
        # otherwise, iterate the statement body and
        # find setup code and timeit funcs
        for child in tree.body:
            if isfunc(child) and child.name.startswith(func_name_prefix):
                timeits.append(TimeitHolder(name=child.name[len(func_name_prefix):],
                                            setup=astunparse.unparse(setup),
                                            code=astunparse.unparse(child.body)))
            else:
                setup.append(child)

    return timeits


def get_ast(target_func_or_module):
    """
    See :func:``bettertimeit`` for acceptable types.

    :returns: an AST for ``target_func_or_module``
    """
    if isinstance(target_func_or_module, ast.AST):
        return target_func_or_module

    if not isinstance(target_func_or_module,
                      (six.string_types, six.binary_type)):
        handled_types = (
            types.ModuleType,
            types.FunctionType,
            getattr(types, "UnboundMethodType", types.MethodType),
            types.MethodType,
        )
        if not isinstance(target_func_or_module, handled_types):
            raise TypeError("Don't know how to handle objects of types '%s'"
                            % type(target_func_or_module))
        target_func_or_module = inspect.getsource(target_func_or_module)
    target_func_or_module = textwrap.dedent(target_func_or_module)

    return ast.parse(target_func_or_module)


def bettertimeit(target_func_or_module, repeat=3, target_time=0.2):
    """
    ``target_func_or_module`` may be:
        * a string
        * a module
        * a function or method (unbound or bound)
        * an ast tree (returned untouched)
    """
    tree = get_ast(target_func_or_module)
    timeits = find_timeits(tree)

    for obj in timeits:
        obj.repeat(repeat=repeat, target_time=target_time)
