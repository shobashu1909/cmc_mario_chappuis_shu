
"""Simulation parameters"""


class SimulationParameters:
    """Simulation parameters"""

    def __init__(self, **kwargs):
        """
        parameters of the FiringRateController() class
        ----------
        **kwargs: optional parameters that overrides the previous parameters
        """
        super(SimulationParameters, self).__init__()

        # firing rate controllers parameters
        self.I = 2
        self.Idiff = 0.
        self.b = 3
        self.w = 2
        self.tau = 0.001
        self.taua = 0.1
        self.alpha = 0

        # simulation parameters
        self.timestep = 0.001  # integration timestep
        # number of iterations (stopping time = timestep*n_iterations)
        self.n_iterations = 1001
        # "single" for single unit, "coupled" for two coupled units
        self.equation_type = "single"
        self.show_progress = True  # show progress in the simulation run
        self.show_metrics = True  # show the metrics of the controller

        # other params
        self.gain = "sigmoid"  # "sigmoid", "sqrt_max" or "max"
        self.lam = 10  # sigmoid's lambda
        self.theta = 0.5  # sigmoid's theta

        # NOTE: This overrides the previous declarations
        self.__dict__.update(kwargs)

