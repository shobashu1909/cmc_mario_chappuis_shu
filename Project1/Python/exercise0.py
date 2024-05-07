
from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
<<<<<<< HEAD
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows
=======
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows_modified
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859



def exercise0(**kwargs):

    pylog.info("Ex 0")
    pylog.info("Implement exercise 0")
    log_path = './logs/exercise0/'
    os.makedirs(log_path, exist_ok=True)

    all_pars = SimulationParameters(
        n_iterations=10001,
        controller="sine",
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

<<<<<<< HEAD
    # example plot using plot_left_right
=======
    # Plot muscle activity
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859
    plt.figure("Left & Right muscle activity")
    plot_left_right(
        controller.times,
        controller.state,
        left_idx,
        right_idx,
        cm="green",
        offset=0.1)
<<<<<<< HEAD
    # plt.savefig('Left & Right muscle activity.png')


    # example plot using plot_trajectory
    plt.figure("Animal head trajectory")
    plot_trajectory(controller)

    plt.figure("joint positions")
    plot_time_histories_multiple_windows(
=======

    # Plot trajectory
    plt.figure("Animal head trajectory")
    plot_trajectory(controller)

    # Plot joint positions
    plt.figure("joint positions")
    plot_time_histories_multiple_windows_modified(
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859
        controller.times,
        controller.joints_positions,
        offset=-0.4,
        colors="green",
        ylabel="joint positions",
        lw=1
    )
<<<<<<< HEAD
    # plt.savefig('joint positions.png')


=======
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859


if __name__ == '__main__':
    exercise0(headless=False)
    plt.show()

