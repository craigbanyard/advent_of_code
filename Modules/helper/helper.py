from time import perf_counter_ns
from functools import wraps, partial
import numpy as np
import math


def aoc_timer(func=None, *, repeat=1, metric=min, **margs):
    """
    Decorator that times the call of a function, func, and prints its execution time.
    If func is called with keyword argument time=False, the print will be surpressed.

    With optional repeat, run func repeat times, appending successive execution times
    to list (or numpy array) [times].
    With optional metric, apply the function metric to the array [times] to calculate
    execution time to display. Default is min, i.e. display minimum execution time.
      Expected built-ins: {min, max, list, sorted}
      Expected custom: {'mean', 'mean_std', 'std', 'var', ... any numpy array method}
      https://numpy.org/doc/stable/reference/routines.statistics.html
      Keyword arguments of metric must be specified as **margs.
    """

    def format_time(t):
        units = ['ns', 'μs', 'ms', 's']
        if t < 1:
            return f"{float(t):.4} ns"
        digits = math.floor(math.log10(t))
        idx = min(len(units) - 1, digits // 3)
        return f"{float(t / 10**(3*idx)):.4} {units[idx]}"

    def mean_std(times):
        m, s = np.mean(times), np.std(times)
        return f"{format_time(m)} ± {format_time(s)}"

    # Handle invalid metrics
    def err(times, metric=metric):
        return f'Invalid metric: {metric}'

    if isinstance(metric, str):
        # Not using built-in => numpy likely quicker
        times = np.zeros(repeat)
        try:
            metric = locals()[metric]
        except KeyError:
            # Try numpy, else err
            metric = getattr(np, metric, err)
    else:
        # Using built-in => list likely quicker
        times = [None] * repeat

    if func is None:
        return partial(aoc_timer, repeat=repeat, metric=metric, **margs)

    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        if kwargs.get("time") is False:
            return func(*args, **kwargs)

        for t in range(repeat):
            t0 = perf_counter_ns()
            result = func(*args, **kwargs)
            t1 = perf_counter_ns() - t0
            times[t] = t1

        if 'get_input' in func.__name__:
            label = 'Data'
        else:
            label = 'Time'

        disp = metric(times, **margs)
        # Check if disp is iterable before attempting to format time
        try:
            _ = iter(disp)
        except TypeError:
            # Not iterable => format time
            disp = format_time(disp)

        print(f"-----\n{label}: {disp}")
        return result

    return wrapper_timer


def main():
    pass


if __name__ == '__main__':
    main()
