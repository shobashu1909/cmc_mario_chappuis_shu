
from util.run_closed_loop import run_multiple
from simulation_parameters import SimulationParameters
import os
import numpy as np
import farms_pylog as pylog

import matplotlib.pyplot as plt
from plot_results import plot_exercise_multiple

<<<<<<< HEAD

=======
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859

def exercise_multiple():

    log_path = './logs/example_multiple/'
    os.makedirs(log_path, exist_ok=True)

    nsim = 2

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    pars_list = [
        SimulationParameters(
            simulation_i=i*nsim+j,
            n_iterations=10001,
<<<<<<< HEAD
            controller="sine",
=======
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859
            log_path=log_path,
            video_record=False,
            compute_metrics=2,
            amplitude=amp,
            wave_frequency=wavefrequency,
            headless=True,
            print_metrics=False
        )
        for i, amp in enumerate(np.linspace(0.05, 0.3, nsim))
        for j, wavefrequency in enumerate(np.linspace(0., 0.1, nsim))
    ]

    # run_multiple(pars_list, num_process=16)

<<<<<<< HEAD
    # add by shu
    # plot result 
    plot_exercise_multiple(nsim**2, log_path)
=======
    pylog.info("Plotting the result")
    #plot_exercise_multiple(nsim**2, log_path)
>>>>>>> 9719d05d174e77c5af79c175692796a80cf19859

if __name__ == '__main__':
    exercise_multiple()
    plt.show()

