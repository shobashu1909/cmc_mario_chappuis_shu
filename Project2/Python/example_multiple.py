
from util.run_closed_loop import run_multiple
from simulation_parameters import SimulationParameters
import os
import numpy as np
import farms_pylog as pylog
import matplotlib.pyplot as plt


def exercise_multiple():

    log_path = './logs/example_multiple/'
    os.makedirs(log_path, exist_ok=True)

    nsim = 5

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    pars_list = [
        SimulationParameters(
            simulation_i=i,
            n_iterations=3001,
            log_path=log_path,
            video_record=False,
            compute_metrics=2,
            g_ss = g_ss,
            headless=True,
            print_metrics=True
        )
        for i, g_ss in enumerate(np.linspace(0, 15, nsim))
    ]

    run_multiple(pars_list, num_process=8)
    

if __name__ == '__main__':
    exercise_multiple()
    print(np.linspace(0, 15, 5))
