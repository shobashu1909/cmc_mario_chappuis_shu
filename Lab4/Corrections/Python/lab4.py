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
matplotlib.rc('font', **{"size":8})

num_process=16 # number of processors



def single_unit(**kwargs):
    """
    run single unit sim with default params
    """
    pars = SimulationParameters(equation_type="single", **kwargs)

    network = run_simulation(pars=pars)

    return network


def single_unit_vary_alpha(**kwargs):
    """
    run single unit sim when varying parameter alpha
    """
    alphas=np.linspace(0,3,16*2)
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
    freqs    = [net.metrics["frequency"] for net in networks]
    amps     = [net.metrics["amp"] for net in networks]
    return alphas, freqs, amps



def two_coupled_units(**kwargs):
    """
    run coupled unit sim with default params
    """
    pars = SimulationParameters(equation_type="coupled", **kwargs)

    network = run_simulation(pars=pars)

    times = network.times
    state = network.state
    plt.plot(times, state[:,0], label="Neuron 1")
    plt.plot(times, state[:,2], label="Neuron 2")
    plt.xlabel("Time")
    plt.ylabel("Activity")
    plt.xlim([0,network.times[-1]])

    return network

def coupled_units_vary_I(**kwargs):
    """
    run simulations when varying parameter alpha
    """
    Is=np.linspace(0,10,16*2)
    par_list = [
        SimulationParameters(
            I=I,
            equation_type="coupled",
            show_metrics=False,
            **kwargs
            )
        for I in Is
    ]
    networks     = run_multiple(par_list, num_process=num_process)
    freqs        = [net.metrics["frequency"] for net in networks]
    sync_indexes = [net.metrics["sync"] for net in networks]
    amps     = [net.metrics["amp"] for net in networks]

    return Is, freqs, sync_indexes, amps


def coupled_units_vary_w(**kwargs):
    """
    run simulations when varying parameter alpha
    """
    ws=np.linspace(-2,5,16*4)
    par_list = [
        SimulationParameters(
            w=w,
            equation_type="coupled",
            show_metrics=False,
            **kwargs
            )
        for w in ws
    ]
    networks     = run_multiple(par_list, num_process=num_process)
    freqs        = [net.metrics["frequency"] for net in networks]
    sync_indexes = [net.metrics["sync"] for net in networks]
    amps     = [net.metrics["amp"] for net in networks]

    return ws, freqs, sync_indexes, amps



def exercise1(fig, alphas):

    grid = plt.GridSpec(3, 3, wspace=0.4, hspace=0.3)
    ymax = 0.0
    for i, alpha in enumerate(alphas):
        plt.subplot(grid[0, i])
        plt.title("alpha={}".format(alpha))
        network=single_unit(alpha=alpha)

        times = network.times
        state = network.state
        plt.plot(times, state[:,0], label="Neuron 1")
        plt.xlabel("Time")
        plt.ylabel("Activity")
        plt.xlim([0,network.times[-1]])

        # record state
        max_state=np.max(network.state[:,0])
        ymax = max(max_state, ymax)
        plt.grid('True')

    # set the same ylim for all top subplot
    for i, ax in enumerate(fig.axes):
        ax.set_ylim([0,ymax+0.1*ymax])

    # variation of alpha
    alphas, freqs, amps = single_unit_vary_alpha()

    plt.subplot(grid[1,:])
    plt.plot(alphas, freqs)
    plt.xlim([alphas[0],alphas[-1]])
    plt.ylabel("Freq (Hz)")
    plt.grid('True')
    plt.xticks([])

    plt.subplot(grid[2,:])
    plt.plot(alphas, amps)
    plt.xlim([alphas[0],alphas[-1]])
    plt.xlabel("Alpha")
    plt.ylabel("Amp")


def exercise2(fig, Is, **kwargs):

    grid = plt.GridSpec(4, 3, wspace=0.4, hspace=0.3)
    ymax = 0.0
    for i, drive in enumerate(Is):
        plt.subplot(grid[0, i])
        plt.title("I={}".format(drive))
        network=two_coupled_units(I=drive, **kwargs)
        max_state=np.max(network.state[:,0])
        ymax = max(max_state, ymax)
        plt.grid('True')
    # set the same ylim for all top subplot
    for i, ax in enumerate(fig.axes):
        ax.set_ylim([0,ymax+0.1*ymax])

    # variation of I
    Is, freqs, sync_indexes, amps = coupled_units_vary_I(**kwargs)
    plt.subplot(grid[1,:])
    plt.plot(Is, freqs)
    plt.ylabel("Freq (Hz)")
    plt.xlim([Is[0],Is[-1]])
    plt.grid('True')
    plt.xticks([])

    plt.subplot(grid[2,:])
    plt.plot(Is, sync_indexes)
    plt.ylabel("Sync")
    plt.xlim([Is[0],Is[-1]])
    plt.ylim([0,1])
    plt.grid('True')
    plt.xticks([])

    plt.subplot(grid[3,:])
    plt.plot(Is, amps)
    plt.xlabel("I")
    plt.ylabel("Amp")
    plt.xlim([Is[0],Is[-1]])
    plt.grid('True')


def exercise3(fig, ws, **kwargs):

    grid = plt.GridSpec(4, 3, wspace=0.4, hspace=0.3)
    ymax = 0.0
    for i, w in enumerate(ws):
        plt.subplot(grid[0, i])
        plt.title("w={}".format(w))
        network=two_coupled_units(w=w, **kwargs)
        max_state=np.max(network.state[:,0])
        ymax = max(max_state, ymax)

        plt.grid('True')
    # set the same ylim for all top subplot
    for i, ax in enumerate(fig.axes):
        ax.set_ylim([0,ymax+0.1*ymax])

    # variation of I
    ws, freqs, sync_indexes, amps = coupled_units_vary_w(**kwargs)
    plt.subplot(grid[1,:])
    plt.plot(ws, freqs)
    plt.ylabel("Freq (Hz)")
    plt.xlim([ws[0],ws[-1]])
    plt.grid('True')
    plt.xticks([])

    plt.subplot(grid[2,:])
    plt.plot(ws, sync_indexes)
    plt.ylabel("Sync")
    plt.xlim([ws[0],ws[-1]])
    plt.ylim([0,1])
    plt.grid('True')
    plt.xticks([])

    plt.subplot(grid[3,:])
    plt.plot(ws, amps)
    plt.xlabel("w")
    plt.ylabel("Amp")
    plt.xlim([ws[0],ws[-1]])
    plt.grid('True')


def main():
    """ Lab 4 exercise """
    pylog.info('Runnig exercise 4a')



    figname="one unit activities"
    fig = plt.figure(figname)
    exercise1(fig, [0.1,1,2.5])
    save_figure(figname)

    pylog.info('Runnig exercise 4b')
    figname="coupled inhibitory units - low inhibition and sigmoid gain"
    fig = plt.figure(figname)
    exercise2(fig, [0.2,3,5])
    save_figure(figname)

    pylog.info('Runnig exercise 4c')
    figname="coupled inhibitory units - high inhibition and sigmoid gain"
    fig = plt.figure(figname)
    exercise2(fig, [1,4,7], w=3.8)
    save_figure(figname)

    pylog.info('Runnig exercise 4d')
    figname="coupled inhibitory units and max gain"
    fig = plt.figure(figname)
    exercise2(fig, [1,4,7], w=2, gain="max")
    save_figure(figname)

    figname="coupled inhibitory units with max-sqrt gain"
    fig = plt.figure(figname)
    exercise2(fig, [1,3,9], w=2.5, gain="sqrt_max")
    save_figure(figname)

    pylog.info('Runnig exercise 4f')
    figname="coupled units - vary w"
    fig = plt.figure(figname)
    exercise3(fig, [-1,0,1])
    save_figure(figname)

    if DEFAULT['save_figures'] is False:
        plt.show()

if __name__ == '__main__':

    from cmcpack import parse_args
    parse_args()
    main()