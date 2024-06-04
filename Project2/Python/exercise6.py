from simulation_parameters import SimulationParameters
from util.run_closed_loop import run_multiple, run_single
import numpy as np
import farms_pylog as pylog
import os
import matplotlib.pyplot as plt
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows_modified, plot_1d_merge
from metrics import compute_controller


def exercise6(**kwargs):
    pylog.info("Ex 6")
    log_path = './logs/exercise6/'
    os.makedirs(log_path, exist_ok=True)

    multiple_sim = True #change to True to test many values of g_ss

    all_pars_single = SimulationParameters(
        n_iterations=5001,
        log_path=log_path,
        compute_metrics=3,
        return_network=True,
        g_ss = 0,
        stretch_feedback = True,
        **kwargs
    )

            
    pylog.info("Running the simulation")

    if not multiple_sim: #one simulation
        controller = run_single(all_pars_single)

        pylog.info("Plotting the result")

        left_idx = controller.muscle_l
        right_idx = controller.muscle_r

        # plot muscle activity
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

         # plot joint positions
        plt.figure("joint positions_single")
        plot_time_histories_multiple_windows_modified(
            controller.times,
            controller.joints_positions,
            offset=-0.4,
            colors="green",
            ylabel="joint positions",
            lw=1
        )


    nsim = 10

    pars_list = [
        SimulationParameters(
            simulation_i=i,
            n_iterations=5001,
            log_path=log_path,
            video_record=False,
            compute_metrics=3,
            return_network = True,
            g_ss = g_ss,
            strecth_feedback = True,
            headless=True,
            print_metrics=True
        )
        for i, g_ss in enumerate(np.linspace(0, 15, nsim))
    ]
    if multiple_sim: #run multiple simulations
        controllers = run_multiple(pars_list, num_process=16)

        # initialize the metrics to plot
        frequency = np.zeros([nsim, 2])
        wavefrequency = np.zeros([nsim, 2])
        fspeed = np.zeros([nsim, 2])

        for i in range(nsim):
            controller = controllers[i]
            frequency[i] = [
                controller.pars.g_ss,
                np.mean(controller.metrics["frequency"])
            ]
            wavefrequency[i] = [
                controller.pars.g_ss,
                np.mean(controller.metrics["wavefrequency"])
            ]
            fspeed[i] = [
                controller.pars.g_ss,
                np.mean(controller.metrics["fspeed_cycle"])
            ]

            # Create subplots in a 3x1 grid
            fig, axs = plt.subplots(3, 1, figsize=[12, 6], sharex=True)

            # Plot each metric on a subplot
            plot_1d_merge(axs[0], frequency, ["g_ss", "frequency"], cmap='blue')
            plot_1d_merge(axs[1], wavefrequency, ["g_ss", "wavefrequency"], cmap='red')
            plot_1d_merge(axs[2], fspeed, ["g_ss", "fspeed"], cmap='green')

            # Adjust layout and save the figure
            plt.tight_layout()
            plt.savefig("ex_6_g_ss_vs_metrics.png")
            plt.show()

if __name__ == '__main__':
    exercise6(headless = False)
    plt.show()

