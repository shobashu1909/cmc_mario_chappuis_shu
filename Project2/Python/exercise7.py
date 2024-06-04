

from simulation_parameters import SimulationParameters
from util.run_closed_loop import run_multiple
import numpy as np
import farms_pylog as pylog
import os
import matplotlib.pyplot as plt

from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows, plot_2d, plot_1d, plot_1d_merge
from util.rw import load_object


def exercise7():

    pylog.info("Ex 7")
    pylog.info("Implement exercise 7")
    os.makedirs('./logs/exercise7', exist_ok=True)

    # added by shu
    log_path = './logs/exercise7/'
    nsim = 10

    nsim_gss = 4
    nsim_I = 10

    pars_list = [
        SimulationParameters(
            simulation_i = i*nsim_I + j,
            n_iterations = 10001,
            log_path = log_path,
            video_record = False,
            compute_metrics = 3,
            g_ss = g_ss,
            I = I,
            headless = True,
            print_metrics = False,
            return_network = True
        )
        for i,g_ss in enumerate(np.linspace(0, 15, nsim_gss))
        for j, I in enumerate(np.linspace(0, 30, nsim_I))
    ]
    # Run the simulations
    pylog.info("Running the simulation")
    # controllers = run_multiple(pars_list, num_process=16)

    # Prepare to plot metrics
    frequency = np.zeros((nsim_gss, nsim_I))
    wavefrequency = np.zeros((nsim_gss, nsim_I))
    fspeed = np.zeros((nsim_gss, nsim_I))

    # Organize data for plotting
    for i in range(nsim_gss):
        for j in range(nsim_I):
            idx = i * nsim_I + j
            controller = load_object(log_path+"controller"+str(idx))
            # print("idx:", idx, "g_ss:", controller.pars.g_ss, "I:", controller.pars.I)

            frequency[i, j] = np.mean(controller.metrics["frequency"])
            wavefrequency[i, j] = np.mean(controller.metrics["wavefrequency"])
            fspeed[i, j] = np.mean(controller.metrics["fspeed_cycle"])

    # Create subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 18), sharex=True)

    for i in range(nsim_gss):
        g_ss_value = np.linspace(0, 15, nsim_gss)[i]
        I_values = np.linspace(0, 30, nsim_I)

        # Plot frequency for each g_ss
        axs[0].plot(I_values, frequency[i, :], label=f'g_ss={g_ss_value}')
        axs[1].plot(I_values, wavefrequency[i, :], label=f'g_ss={g_ss_value}')
        axs[2].plot(I_values, fspeed[i, :], label=f'g_ss={g_ss_value}')

    # axs[0].set_title('Frequency vs I')
    # axs[1].set_title('Wave Frequency vs I')
    # axs[2].set_title('F Speed vs I')
    axs[2].set_xlabel('I')
    axs[0].set_ylabel('Frequency')
    axs[1].set_ylabel('Wave Frequency')
    axs[2].set_ylabel('F Speed')

    for ax in axs:
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.savefig("ex_7_metrics.png")
    plt.show()
    
    # Create subplots in a 3x1 grid
    
    # first plot
    # plot the result with the first value of g_ss
    # on x axis : I
    # on y axis : frequency

    # plot the result with the second value of g_ss
    # on x axis : I
    # on y axis : frequency

    # plot the result with the third value of g_ss
    # on x axis : I
    # on y axis : frequency

    #...

    # plot the result with the nsim value of g_ss
    # on x axis : I
    # on y axis : frequency

    # second plot
    # plot the result with the first value of g_ss
    # on x axis : I
    # on y axis : wavefrequency

    # plot the result with the second value of g_ss
    # on x axis : I
    # on y axis : frequency

    # plot the result with the third value of g_ss
    # on x axis : I
    # on y axis : wavefrequency

    #...

    # plot the result with the nsim value of g_ss
    # on x axis : I
    # on y axis : wavefrequency

    # third plot
    # plot the result with the first value of g_ss
    # on x axis : I
    # on y axis : fspeed

    # plot the result with the second value of g_ss
    # on x axis : I
    # on y axis : fspeed

    # plot the result with the third value of g_ss
    # on x axis : I
    # on y axis : fspeed

    #...

    # plot the result with the nsim value of g_ss
    # on x axis : I
    # on y axis : fspeed


def main(ind=0, w_stretch=0):
    log_path = './logs/exercise7/w_stretch'+str(ind)+'/'
    os.makedirs(log_path, exist_ok=True)


if __name__ == '__main__':
    exercise7()

