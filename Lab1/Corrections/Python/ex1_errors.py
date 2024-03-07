""" Exercise 1 - Error evaluation """

from typing import List, Callable, Any
import numpy as np
from nptyping import NDArray
import matplotlib.pyplot as plt

from cmcpack.plot import save_figure

# pylint: disable=invalid-name


def error(errors: NDArray[(Any,), float], n: Any = 0) -> float:
    """ Compute and return error

    This function should receive a vector of errors of same size as the time
    vector in the integration. It should return a single value based on these
    errors.

    The variable n can be optionally be used to implement different errors and
    compare them.

    """
    err_abs = np.abs(errors)
    if n == 0:
        err = max(err_abs)
    else:
        err = np.sum([e**n for e in err_abs])/len(err_abs)
    return err


def plot_error(
        dt_list: List[float],
        err: NDArray[(Any,), float],
        figure: str = 'Average_error',
        label: str = 'Error',
):
    """ Plot """
    plt.figure(figure)
    plt.plot(dt_list, err, label=label, linewidth=2.0, marker='.')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(loc='best')
    plt.xlabel('Time step [s]')
    plt.ylabel('Error')
    plt.grid(True)
    save_figure(figure)


def compute_error(
        func: Callable,
        analytical: Callable,
        method: Callable,
        x0: NDArray[(Any,), float],
        dt_list: List[float],
        **kwargs,
):
    """ Compute integration error wrt time step """
    time_max = kwargs.pop('time_max', 5)
    n = kwargs.pop('n', 0)
    err = np.zeros(len(dt_list))
    for i, dt in enumerate(dt_list):
        time = np.arange(0, time_max, dt)
        method_result = method(func, x0, time_max, dt)
        method_state = method_result.state
        errors = method_state[:, 0] - analytical(time)
        err[i] = error(errors, n=n)
    plot_error(
        dt_list, err,
        kwargs.pop('figure', 'Average error'),
        kwargs.pop('label', 'Error')
    )