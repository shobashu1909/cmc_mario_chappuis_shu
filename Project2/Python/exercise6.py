from simulation_parameters import SimulationParameters
from util.run_closed_loop import run_multiple, run_single
import numpy as np
import farms_pylog as pylog
import os
import matplotlib.pyplot as plt
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows_modified
from metrics import compute_controller


def exercise6(**kwargs):
    pylog.info("Ex 6")
    log_path = './logs/exercise6/'
    os.makedirs(log_path, exist_ok=True)
    all_pars = SimulationParameters(
        n_iterations=10001,
        log_path=log_path,
        compute_metrics=3,
        return_network=True,
        g_ss = 3,
        stretch_feedback = True,
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
    plt.figure('muscle_activities_single')
    plot_left_right(
        controller.times,
        controller.state,
        left_idx,
        right_idx,
        cm="green",
        offset=0.1)

    # plot CPG activities
    plt.figure('CPG_activities_single')
    plot_left_right(
        controller.times,
        controller.state,
        controller.r_L_ind,
        controller.r_R_ind,
        cm='green',
        offset=0.1    
    )

    # plot sensory neurons activities
    plt.figure('sensory_neurons_activities_single')
    plot_left_right(
        controller.times,
        controller.state,
        controller.s_L_ind,
        controller.s_R_ind,
        cm='green',
        offset=0.1    
    )

    # example plot using plot_trajectory
    #plt.figure("trajectory_single")
    #plot_trajectory(controller)

    # example plot using plot_time_histories_multiple_windows
    plt.figure("joint positions_single")
    plot_time_histories_multiple_windows_modified(
        controller.times,
        controller.joints_positions,
        offset=-0.4,
        colors="green",
        ylabel="joint positions",
        lw=1
    )

    print(compute_controller(controller))



if __name__ == '__main__':
    exercise6(headless = False)
    plt.show()

