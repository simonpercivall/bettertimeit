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

``bettertimeit`` will time any function which is named "timeit_<something>".
The "timeit_" functions may be contained within a function or in a module.
Each "timeit_" function will be timed separately::

    from bettertimeit import bettertimeit

    def container():
        a = 5

        def timeit_calculation():
            a**10

        b = 3

        def timeit_calculation_2():
            a**b

    bettertimeit(container)


Features
--------

* Lets you write your timing test code as regular code instead of strings,
  but without the overhead of a function call.
* Put your timing test code in a module or inside a function
* Uses the same method as timeit.main to calculate the optimal number of
  passes to run.
