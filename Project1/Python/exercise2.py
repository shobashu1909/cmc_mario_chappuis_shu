
from util.run_closed_loop import run_multiple, run_single
from simulation_parameters import SimulationParameters
import os
import numpy as np
import farms_pylog as pylog

import matplotlib.pyplot as plt
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows



def exercise2(**kwargs):

    pylog.info("Ex 2")
    pylog.info("Implement exercise 2")
    log_path = './logs/exercise2/'
    os.makedirs(log_path, exist_ok=True)

    all_pars = SimulationParameters(
        n_iterations=4001,
        controller="sine",
        square = True,
        log_path=log_path,
        compute_metrics=3,
        return_network=True,
        **kwargs
    )

    pylog.info("Running the simulation")
    controller = run_single(
        all_pars
    )

    pylog.info("Plotting the result")

    left_idx = controller.muscle_l
    right_idx = controller.muscle_r

    # example plot using plot_left_right
    plt.figure("Left & Right muscle activity")

    plot_left_right(
        controller.times,
        controller.state,
        left_idx,
        right_idx,
        cm="green",
        offset=0.1)

    # example plot using plot_trajectory
    plt.figure("trajectory")
    plot_trajectory(controller)

    

if __name__ == '__main__':
    exercise2(headless=False)
    plt.show()

