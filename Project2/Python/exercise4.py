

from simulation_parameters import SimulationParameters
from util.run_open_loop import run_multiple
import numpy as np
import farms_pylog as pylog
import os


def exercise4():

    pylog.info("Ex 4")
    pylog.info("Implement exercise 4")
    log_path = './logs/exercise4/'
    os.makedirs(log_path, exist_ok=True)

    nsim = 5

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    
    pars_list = [
        SimulationParameters(
            simulation_i = i * nsim + j,
            frequency = 1.0,
            n_iterations = 10001,
            log_path = log_path,
            video_record = False,
            compute_metrics = 2,
            I = I,
            headless = True,
            print_metrics = True,
            return_network = True
        )
        for i, I in enumerate(np.linspace(0, 30, nsim))
    ]


if __name__ == '__main__':
    exercise4()

