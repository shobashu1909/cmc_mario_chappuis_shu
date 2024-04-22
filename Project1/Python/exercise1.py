
from util.run_closed_loop import run_multiple
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt

import os
import numpy as np
import farms_pylog as pylog

from plot_results import plot_exercise_multiple
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows

from util.rw import load_object



def exercise1():

    pylog.info("Ex 1")
    pylog.info("Implement exercise 1")
    log_path = './logs/exercise1/'
    os.makedirs(log_path, exist_ok=True)

    nsim = 3

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    amp_values = list(np.linspace(0.05, 0.4, nsim))
    wavefrequency_values = list(np.linspace(0., 0.1, nsim))

    for i, amp in enumerate(amp_values):
        print(f"amp{i} = {amp}")

    for j, wavefrequency in enumerate(wavefrequency_values):
        print(f"wf{j} = {wavefrequency}")

    # Now, create the pars_list using a nested list comprehension
    pars_list = [
        SimulationParameters(
            simulation_i = i * nsim + j,
            n_iterations = 8001,
            log_path = log_path,
            video_record = False,
            compute_metrics = 2,
            amp = amp_values[i],
            wavefrequency = wavefrequency_values[j],
            headless = True,
            print_metrics = True,
            return_network = True
        )
        for i in range(nsim)
        for j in range(nsim)
    ]

    pylog.info("Running the simulation")
    run_multiple(pars_list, num_process=16)

    pylog.info("Plotting the result")
    plot_exercise_multiple(nsim**2, log_path)

if __name__ == '__main__':
    exercise1()
    plt.show()

