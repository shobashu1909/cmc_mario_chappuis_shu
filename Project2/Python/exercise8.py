
from util.run_closed_loop import run_multiple
from simulation_parameters import SimulationParameters
import os
import numpy as np
import farms_pylog as pylog
import matplotlib.pyplot as plt

from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows, plot_2d, plot_1d, plot_1d_merge
from util.rw import load_object

def exercise8():

    pylog.info("Ex 8")
    pylog.info("Implement exercise 8")
    log_path = './logs/exercise8/'
    os.makedirs(log_path, exist_ok=True)

    nsim = 5

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    
    pars_list = [
        SimulationParameters(
            simulation_i = i * nsim + j,
            n_iterations = 10001,
            log_path = log_path,
            video_record = False,
            method = "noise",
            compute_metrics = 3,
            noise_sigma = sigma,
            w_stretch = w_stretch,
            headless = True,
            print_metrics = False,
            return_network = True
        )
        for i, sigma in enumerate(np.linspace(0, 10, nsim))
        for j, w_stretch in enumerate(np.linspace(0, 30, nsim))
    ]

    # Run the simulations 
    pylog.info("Running the simulation")
    # controllers = run_multiple(pars_list, num_process=16)

    # initialize the metrics to plot
    fspeeds_PCA = np.zeros([nsim*nsim, 3])
    lspeeds_PCA = np.zeros([nsim*nsim, 3])

    # Plot the results
    # _________________________________________________________________
    # fspeeds_PCA
    for i in range(nsim*nsim):
        # load the controller
        controller = load_object(log_path+"controller"+str(i))
        fspeeds_PCA[i] = [
            controller.pars.noise_sigma,
            controller.pars.w_stretch,
            np.mean(controller.metrics["fspeed_PCA"])
        ]
    
    plt.figure('Forward Speed PCA[m/s] ', figsize=[10, 10])
    plot_2d(
        fspeeds_PCA,
        ['sigma', 'w_stretch', 'Forward Speed PCA[m/s]'],
        cmap='nipy_spectral'
    )
    plt.savefig('ex_8_fspeed_PCA.png')

    # _________________________________________________________________
    # lspeeds_PCA
    for i in range(nsim*nsim):
        # load the controller
        controller = load_object(log_path+"controller"+str(i))
        lspeeds_PCA[i] = [
            controller.pars.noise_sigma,
            controller.pars.w_stretch,
            np.mean(controller.metrics["lspeed_PCA"])
        ]
    
    plt.figure('L Speed PCA[m/s]', figsize=[10, 10])
    plot_2d(
        lspeeds_PCA,
        ['sigma', 'w_stretch', 'Lateral Speed PCA[m/s]'],
        cmap='nipy_spectral'
    )
    plt.savefig('ex_8_lspeed_PCA.png')



if __name__ == '__main__':
    exercise8()
    plt.show()
