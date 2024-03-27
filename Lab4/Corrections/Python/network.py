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

        self.n_iterations   = pars.n_iterations
        self.timestep       = pars.timestep
        self.times          = np.linspace(0, self.n_iterations*self.timestep, self.n_iterations)

        self.pars = pars # model parameter simulation_parameters.SimulationParameters() class

        if self.pars.equation_type == "single":

            n_eq         = 2 # total number of ODE equations
            self.ode_rhs = self.rhs_single

            self.all_v   = [0]
            self.all_a   = [1]

        elif self.pars.equation_type == "coupled":

            n_eq         = 4
            self.ode_rhs = self.rhs_coupled

            self.left_v  = [0]
            self.left_a  = [1]
            self.right_v = [2]
            self.right_a = [3]
            self.all_v   = np.concatenate([self.left_v,self.right_v])
            self.all_a   = np.concatenate([self.left_a,self.right_a])
            self.inputs  = np.zeros(n_eq) # input drives

        else:
            raise("Choose correct equation type: single or coupled!!")


        # initialize the state of the ODE solver
        self.state  = np.zeros([self.n_iterations, n_eq])
        self.dstate = np.zeros([n_eq])

        # random initial values
        self.state[0] = np.random.rand(n_eq)

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

        # rate equations
        self.dstate[self.all_v] = ( -state[self.all_v] + self.S(
                self.pars.alpha*state[self.all_v]+self.pars.I-self.pars.b*state[self.all_a]
            )
        ) / self.pars.tau
        # adaptation equations
        self.dstate[self.all_a] = ( -state[self.all_a] + state[self.all_v] ) / self.pars.taua
        return self.dstate




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
        # self-excitation+inputs+adaptation terms
        self.inputs[self.all_v] = self.pars.alpha*state[self.all_v]-self.pars.b*state[self.all_a]+self.pars.I

        # coupling equations
        self.inputs[self.left_v]  += - self.pars.w*state[self.right_v]
        self.inputs[self.right_v] += - self.pars.w*state[self.left_v]

        # rate equations
        self.dstate[self.all_v] = ( -state[self.all_v] + self.S( self.inputs[self.all_v] ) ) / self.pars.tau

        # adaptation equations
        self.dstate[self.all_a] = ( -state[self.all_a] + state[self.all_v] ) / self.pars.taua

        return self.dstate


    def S_sqrt(self, x):
        return np.sqrt(np.maximum(x,0))

    def S_max(self, x):
        return np.maximum(x,0)

    def S_sigmoid(self, x):
        return 1/(1+np.exp(-self.pars.lam*(x-self.pars.theta)))