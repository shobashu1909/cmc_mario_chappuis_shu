#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Lab 4 """

# pylint: disable=invalid-name

import numpy as np
import matplotlib.pyplot as plt
import farms_pylog as pylog
from util.run_open_loop import run_simulation, run_multiple
from simulation_parameters import SimulationParameters
from cmcpack import DEFAULT
from cmcpack.plot import save_figure
import matplotlib
matplotlib.rc('font', **{"size": 8})

num_process = 16  # number of processors


def single_unit(**kwargs):
    """
    Example run a single simulation.
    ----------
    **kwargs: optional parameters that will replace the default parameters
    of the SimulationParameters class
    """
    pylog.info(
        "Run single unit simulation with default parameter and plot the rate of the state")
    pars = SimulationParameters(equation_type="single", **kwargs)
    network = run_simulation(pars=pars)
    times = network.times
    state = network.state
    plt.plot(times, state[:, 0], label="Neuron 1")
    plt.xlabel("Time")
    plt.ylabel("Activity")
    plt.xlim([0, network.times[-1]])
    pylog.info("The metrics are stored in network.metrics")


def single_unit_vary_alpha(**kwargs):
    """
    Example run of multiple simulation in parallel from a list of SimulationParameters() classes
    ----------
    **kwargs: optional parameters that will replace the default parameters
    of the SimulationParameters class
    """
    pylog.info(
        "Run multiple simulations in parallel varying parameter alpha in [0,3]")
    alphas = np.linspace(0, 3, 6)
    par_list = [
        SimulationParameters(
            equation_type="single",
            alpha=alpha,
            show_metrics=False,
            **kwargs
        )
        for alpha in alphas
    ]
    networks = run_multiple(par_list, num_process=num_process)
    pylog.info(
        "The metric list are stored in [network.metrics for network in networks]")


def main():
    """ Lab 4 exercise """
    pylog.info('Runnig exercise 4a')

    single_unit()
    single_unit_vary_alpha()

    pylog.warning('Implement here the various excercises of Lab 4')

    if DEFAULT['save_figures'] is False:
        plt.show()


if __name__ == '__main__':

    from cmcpack import parse_args
    parse_args()
    main()

