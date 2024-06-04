

from simulation_parameters import SimulationParameters
from util.run_open_loop import run_multiple
import numpy as np
import farms_pylog as pylog
import os

# added by shu
from util.rw import load_object
import matplotlib.pyplot as plt
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows, plot_2d, plot_1d, plot_1d_merge




def exercise4():

    pylog.info("Ex 4")
    pylog.info("Implement exercise 4")
    log_path = './logs/exercise4/'
    os.makedirs(log_path, exist_ok=True)

    nsim = 30

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    
    pars_list = [
        SimulationParameters(
            simulation_i = i ,
            # frequency = 1.0,
            frequency = 3.4479310689620735,
            # ipls = 0.19689468749999772, 
            wavefrequency = 0.6788793103448205, 
            # ptcc = 1.9272312875880733,
            amp = 1.838618356662702,
            n_iterations = 10001,
            log_path = log_path,
            video_record = False,
            compute_metrics = 2,
            I = I,
            headless = True,
            print_metrics = True,
            return_network = True
        )
        # vary I from 0 to 30
        for i, I in enumerate(np.linspace(0, 30, nsim))
    ]

    # Run the simulations
    pylog.info("Running the simulation")
    # controllers = run_multiple(pars_list, num_process=16)

    # # initialize the metrics to plot
    # ptcc = np.zeros([nsim, 2])

    # # Plot the results
    # # _________________________________________________________________
    # # use the ptcc metric to measure the stability of the oscillations
    # for i in range(nsim):
    #     # load the controller
    #     controller = load_object(log_path+"controller"+str(i))
    #     ptcc[i] = [
    #         controller.pars.I,
    #         controller.metrics["ptcc"]
    #     ]
    
    # # plot the I vs ptcc graph
    # plt.figure('ptcc', figsize=[12, 6])
    # plot_1d(
    #     ptcc,
    #     ["I", "ptcc"],
    #     cmap='nipy_spectral'
    # )
    # plt.savefig("ex_4_I_vs_ptcc.png")
    
    # plt.show()

    # # How does the frequency and wavefrequency change within the range of I that support the oscialltions
    # # _________________________________________________________________
    # # initialize the metrics to plot
    # frequency = np.zeros([nsim, 2])
    # wavefrequency = np.zeros([nsim, 2])
    # ipls = np.zeros([nsim, 2])

    # for i in range(nsim):
    #     # load the controller
    #     controller = load_object(log_path+"controller"+str(i))
    #     frequency[i] = [
    #         controller.pars.I,
    #         controller.metrics["frequency"]
    #     ]
    #     wavefrequency[i] = [
    #         controller.pars.I,
    #         controller.metrics["wavefrequency"]
    #     ]
    #     ipls[i] = [
    #         controller.pars.I,
    #         controller.metrics["ipls"]
    #     ]
    
    # plt.figure('frequency', figsize=[12, 6])
    # plot_1d(
    #     frequency,
    #     ["I", "frequency"],
    #     cmap='nipy_spectral'
    # )
    # plt.savefig("ex_4_I_vs_frequency.png")
    # plt.show()

    # plt.figure('wavefrequency', figsize=[12, 6])
    # plot_1d(
    #     wavefrequency,
    #     ["I", "wavefrequency"],
    #     cmap='nipy_spectral'
    # )
    # plt.savefig("ex_4_I_vs_ipls.png")
    # plt.show()

    # plt.figure('ipls', figsize=[12, 6])
    # plot_1d(
    #     wavefrequency,
    #     ["I", "ipls"],
    #     cmap='nipy_spectral'
    # )
    # plt.savefig("ex_4_I_vs_ipls.png")
    # plt.show()

    # Initialize metrics arrays
    ptcc = np.zeros([nsim, 2])
    frequency = np.zeros([nsim, 2])
    wavefrequency = np.zeros([nsim, 2])
    ipls = np.zeros([nsim, 2])

    # Load data and calculate metrics
    for i in range(nsim):
        controller = load_object(log_path + "controller" + str(i))
        ptcc[i] = [controller.pars.I, controller.metrics["ptcc"]]
        frequency[i] = [controller.pars.I, controller.metrics["frequency"]]
        wavefrequency[i] = [controller.pars.I, controller.metrics["wavefrequency"]]
        ipls[i] = [controller.pars.I, controller.metrics["ipls"]]

    # Create subplots in a 4x1 grid
    fig, axs = plt.subplots(4, 1, figsize=[6, 12], sharex=True)

    # Plot each metric on a subplot
    plot_1d_merge(axs[0], ptcc, ["I", "ptcc"], cmap='blue')
    plot_1d_merge(axs[1], frequency, ["I", "frequency"], cmap='green')
    plot_1d_merge(axs[2], wavefrequency, ["I", "wavefrequency"], cmap='red')
    plot_1d_merge(axs[3], ipls, ["I", "ipls"], cmap='purple')

    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig("ex_4_metrics_overview.png")
    plt.show()



    # _________________________________________________________________



if __name__ == '__main__':
    exercise4()

