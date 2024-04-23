
from util.run_closed_loop import run_multiple
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt

import os
import numpy as np
import farms_pylog as pylog

from plot_results import plot_exercise_multiple
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows, plot_2d

from util.rw import load_object



def exercise1():

    pylog.info("Ex 1")
    pylog.info("Implement exercise 1")
    log_path = './logs/exercise1/'
    os.makedirs(log_path, exist_ok=True)

    nsim = 5

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    # amp_values = list(np.linspace(0.5, 2, nsim))
    # wavefrequency_values = list(np.linspace(0.5, 2, nsim))

    # for i, amp in enumerate(amp_values):
    #     print(f"amp{i} = {amp}")

    # for j, wavefrequency in enumerate(wavefrequency_values):
    #     print(f"wf{j} = {wavefrequency}")

    # Now, create the pars_list using a nested list comprehension
    pars_list = [
        SimulationParameters(
            simulation_i = i * nsim + j,
            n_iterations = 10001,
            log_path = log_path,
            video_record = False,
            compute_metrics = 2,
            amplitude = amp,
            wave_frequency = wavefrequency,
            headless = True,
            print_metrics = True,
            return_network = True
        )
        for i, amp in enumerate(np.linspace(0.05, 2, nsim))
        for j, wavefrequency in enumerate(np.linspace(0., 2, nsim))
    ]

    # pylog.info("Running the simulation")
    # controllers = run_multiple(pars_list, num_process=16)

    fspeeds = np.zeros([nsim*nsim, 3])
    lspeeds = np.zeros([nsim*nsim, 3])
    fspeeds_PCA = np.zeros([nsim*nsim, 3])
    lspeeds_PCA = np.zeros([nsim*nsim, 3])
    torque = np.zeros([nsim*nsim, 3])

    # Plot the results
    # fspeeds
    for i in range(nsim*nsim):
        # load the controller
        controller = load_object(log_path+"controller"+str(i))
        fspeeds[i] = [
            controller.pars.amplitude,
            controller.pars.wave_frequency,
            np.mean(controller.metrics["fspeed_cycle"])
        ]
    # print(fspeeds)
    # print(controller.metrics["fspeed_cycle"])

    plt.figure('Forward Speed [m/s]', figsize=[10, 10])
    plot_2d(
        fspeeds,
        ['Amp', 'wavefrequency', 'Forward Speed [m/s]'],
        cmap='nipy_spectral'
    )
    plt.savefig('fspeed.png') 

    # fspeeds_PCA
    for i in range(nsim*nsim):
        # load the controller
        controller = load_object(log_path+"controller"+str(i))
        fspeeds_PCA[i] = [
            controller.pars.amplitude,
            controller.pars.wave_frequency,
            np.mean(controller.metrics["fspeed_PCA"])
        ]
    
    plt.figure('Forward Speed PCA[m/s] ', figsize=[10, 10])
    plot_2d(
        fspeeds_PCA,
        ['Amp', 'wavefrequency', 'Forward Speed PCA[m/s]'],
        cmap='nipy_spectral'
    )
    plt.savefig('fspeed_PCA.png')

    # lspeeds
    for i in range(nsim):
        # load the controller
        controller = load_object(log_path+"controller"+str(i))
        lspeeds[i] = [
            controller.pars.amplitude,
            controller.pars.wave_frequency,
            np.mean(controller.metrics["lspeed_cycle"])
        ]
    
    plt.figure('L Speed[m/s]', figsize=[10, 10])
    plot_2d(
        lspeeds,
        ['Amp', 'wavefrequency', 'L Speed[m/s]'],
        cmap='nipy_spectral'
    )
    plt.savefig('lspeed.png')

    # lspeeds_PCA
    for i in range(nsim):
        # load the controller
        controller = load_object(log_path+"controller"+str(i))
        lspeeds_PCA[i] = [
            controller.pars.amplitude,
            controller.pars.wave_frequency,
            np.mean(controller.metrics["lspeed_PCA"])
        ]
    
    plt.figure('L Speed PCA[m/s]', figsize=[10, 10])
    plot_2d(
        lspeeds_PCA,
        ['Amp', 'wavefrequency', 'L Speed PCA[m/s]'],
        cmap='nipy_spectral'
    )
    plt.savefig('lspeed_PCA.png')


    # torque
    for i in range(nsim):
        # load the controller
        controller = load_object(log_path+"controller"+str(i))
        torque[i] = [
            controller.pars.amplitude,
            controller.pars.wave_frequency,
            np.mean(controller.metrics["torque"])
        ]
    
    plt.figure('Torque', figsize=[10, 10])
    plot_2d(
        torque,
        ['Amp', 'wavefrequency', 'Torque'],
        cmap='nipy_spectral'
    )
    plt.savefig('torque.png') 


if __name__ == '__main__':
    exercise1()
    plt.show()

