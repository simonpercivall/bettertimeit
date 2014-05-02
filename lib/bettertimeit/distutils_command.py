from setuptools import Command


class TimeIt(Command):
    user_options = [
        ('timeit-suite=', 's',
         "Timeit suite to run (e.g. 'some_module.timeit_suite')"),
        ('target-time=', 't',
         "Timeit target time per run (default 0.2s)")
    ]

    def initialize_options(self):
        self.timeit_suite = None
        self.target_time = None

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
            extra = {}
            if self.target_time:
                extra['target_time'] = float(self.target_time)
            bettertimeit(module, **extra)

    @staticmethod
    def validate_keyword(dist, attr, value):
        pass
