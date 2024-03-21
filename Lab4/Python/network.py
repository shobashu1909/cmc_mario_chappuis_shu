"""Network controller"""

import numpy as np
import farms_pylog as pylog


class FiringRateController:
    """zebrafish controller"""

    def __init__(
            self,
            pars
    ):
        super().__init__()

        self.n_iterations = pars.n_iterations
        self.timestep = pars.timestep
        self.times = np.linspace(
            0,
            self.n_iterations *
            self.timestep,
            self.n_iterations)

        self.pars = pars  # model parameter simulation_parameters.SimulationParameters() class

        if self.pars.equation_type == "single":

            n_eq = 2  # total number of ODE equations
            pylog.warning(
                'Implement in self.rhs_single the equations for the single unit')
            self.ode_rhs = self.rhs_single

        elif self.pars.equation_type == "coupled":

            n_eq = 4
            pylog.warning(
                'Implement in self.rhs_coupled the equations for the coupled units')
            self.ode_rhs = self.rhs_coupled

        else:
            raise ("Choose correct equation type: single or coupled!!")

        # initialize the state of the ODE solver
        self.state = np.zeros([self.n_iterations, n_eq])
        self.dstate = np.zeros([n_eq])

        # random initial values
        self.state[0] = np.random.rand(n_eq)

        pylog.warning(
            'Implement in self.S_sqrt, self.S_max and S_sigmoid the gain functions for the max-sqrt, max and sigmoid activation functions')
        # set the gain function
        if self.pars.gain == "sqrt_max":
            self.S = self.S_sqrt
        elif self.pars.gain == "max":
            self.S = self.S_max
        elif self.pars.gain == "sigmoid":
            self.S = self.S_sigmoid

    def rhs_single(self,  _time, state):
        """ Single unit
        Implement here the right-hand-side ODE equations network of two coupled firing rate units
        Parameters
        ----------
        _time: <float>
            Time
        state: <np.array>
            ODE states at time _time
        Returns
        -------
        dstate: <np.array>
            Returns derivative of state
        """

        return np.zeros(2)

    def rhs_coupled(self,  _time, state):
        """ Coupled units
        Implement here the right-hand-side ODE equations network of two coupled firing rate units
        Parameters
        ----------
        _time: <float>
            Time
        state: <np.array>
            ODE states at time _time
        Returns
        -------
        dstate: <np.array>
            Returns derivative of state
        """

        return np.zeros(4)

    def S_sqrt(self, x):
        return np.zeros(len(x))

    def S_max(self, x):
        return np.zeros(len(x))

    def S_sigmoid(self, x):
        return np.zeros(len(x))

