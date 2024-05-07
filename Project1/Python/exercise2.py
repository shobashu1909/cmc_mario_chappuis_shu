
from util.run_closed_loop import run_multiple, run_single
from simulation_parameters import SimulationParameters
import os
import numpy as np
import farms_pylog as pylog
import matplotlib.pyplot as plt
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows_modified

import matplotlib.pyplot as plt
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows

<<<<<<< HEAD


=======
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859
def exercise2(**kwargs):

    pylog.info("Ex 2")
    pylog.info("Implement exercise 2")
    log_path = './logs/exercise2/'
    os.makedirs(log_path, exist_ok=True)

    all_pars = SimulationParameters(
<<<<<<< HEAD
        n_iterations=4001,
=======
        n_iterations=10001,
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859
        controller="sine",
        square = True,
        log_path=log_path,
        compute_metrics=3,
        return_network=True,
        **kwargs
    )

    pylog.info("Running the simulation")
<<<<<<< HEAD
    controller = run_single(
        all_pars
    )
=======
    controller = run_single(all_pars)
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859

    pylog.info("Plotting the result")

    left_idx = controller.muscle_l
    right_idx = controller.muscle_r

<<<<<<< HEAD
    # example plot using plot_left_right
    plt.figure("Left & Right muscle activity")

=======
    # Plot left and right muscle activity
    plt.figure("Left & Right muscle activity")
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859
    plot_left_right(
        controller.times,
        controller.state,
        left_idx,
        right_idx,
        cm="green",
        offset=0.1)

<<<<<<< HEAD
    # example plot using plot_trajectory
    plt.figure("trajectory")
    plot_trajectory(controller)

    
=======
    # Plot trajectory
    plt.figure("trajectory")
    plot_trajectory(controller)

    # Plot joint positions
    plt.figure("joint positions")
    plot_time_histories_multiple_windows_modified(
        controller.times,
        controller.joints_positions,
        offset=-0.4,
        colors="green",
        ylabel="joint positions",
        lw=1
    )

    # Plot link y-velocities
    plt.figure("link y-velocities")
    plot_time_histories(
        controller.times,
        controller.links_velocities[:, :, 1],
        offset=-0.,
        colors="green",
        ylabel="link y-velocities",
        lw=1
    )

>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859

if __name__ == '__main__':
    exercise2(headless=False)
    plt.show()

