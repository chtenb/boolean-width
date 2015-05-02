# encoding: utf-8
# filename: profile.py
"""
Profiling utilities.
"""

# Import profile tools
import pstats, cProfile


def profile(function, filename='Profile.prof'):
    """Evaluate and profile given string."""
    cProfile.runctx('print(function())', globals(), locals(), filename)
    report = pstats.Stats(filename)
    report.strip_dirs().sort_stats('time').print_stats()

def compare(functions, filename='Profile.prof'):
    """Profile a sequence of functions."""
    for function in functions:
        profile(function, filename)

