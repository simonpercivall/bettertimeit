=============
Better Timeit
=============

.. image:: https://badge.fury.io/py/bettertimeit.png
    :target: http://badge.fury.io/py/bettertimeit

.. image:: https://travis-ci.org/simonpercivall/bettertimeit.png?branch=master
    :target: https://travis-ci.org/simonpercivall/bettertimeit

.. image:: https://pypip.in/d/bettertimeit/badge.png
    :target: https://crate.io/packages/bettertimeit?version=latest


A Better Timeit

* Free software: BSD license
* Documentation: http://bettertimeit.rtfd.org.

Example
-------

``bettertimeit`` will time any function which is named "timeit\_<something>".
The "timeit\_" functions may be contained within a function or in a module.
Each "timeit\_" function will be timed separately::

    from bettertimeit import bettertimeit

    def container():
        a = 5

        def timeit_calculation():
            a**10

        b = 3

        def timeit_calculation_2():
            a**b

    bettertimeit(container)


To run timings from setup.py, you could add this to :func:`setup`::

    setup(
        ...
        timeit_suite="timings",
    )


And then run::

    % python setup.py timeit


This would run timeit functions in ``timings.py``.

Features
--------

* Lets you write your timing test code as regular code instead of strings,
  but without the overhead of a function call.
* Put your timing test code in a module or inside a function
* Uses the same method as timeit.main to calculate the optimal number of
  passes to run.
* Adds a ``timeit_suite`` option to setup() in setup.py, and a distutils
  command ``timeit`` to run timings from setup.py.
