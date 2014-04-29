from setuptools import Command


class TimeIt(Command):
    user_options = [
        ('timeit-suite=', 's',
         "Timeit suite to run (e.g. 'some_module.timeit_suite')"),
    ]

    def initialize_options(self):
        self.timeit_suite = None

    def finalize_options(self):
        if self.timeit_suite is None:
            self.timeit_suite = self.distribution.timeit_suite

    def run(self):
        from . import bettertimeit

        if self.timeit_suite:
            module = __import__(self.timeit_suite,
                                globals(),
                                locals(),
                                self.timeit_suite.split('.')[-1],
                                -1)
            bettertimeit(module)

    @staticmethod
    def validate_keyword(dist, attr, value):
        pass
