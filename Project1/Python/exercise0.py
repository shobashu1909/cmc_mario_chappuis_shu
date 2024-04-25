
from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows



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

    # example plot using plot_left_right
    plt.figure("Left & Right muscle activity")
    plot_left_right(
        controller.times,
        controller.state,
        left_idx,
        right_idx,
        cm="green",
        offset=0.1)
    # plt.savefig('Left & Right muscle activity.png')


    # example plot using plot_trajectory
    plt.figure("Animal head trajectory")
    plot_trajectory(controller)

    plt.figure("joint positions")
    plot_time_histories_multiple_windows(
        controller.times,
        controller.joints_positions,
        offset=-0.4,
        colors="green",
        ylabel="joint positions",
        lw=1
    )
    # plt.savefig('joint positions.png')




if __name__ == '__main__':
    exercise0(headless=False)
    plt.show()

