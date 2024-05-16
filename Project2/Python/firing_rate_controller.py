"""Network controller"""

import numpy as np
from scipy.interpolate import CubicSpline
import scipy.stats as ss
import farms_pylog as pylog


class FiringRateController:
    """zebrafish controller"""

    def __init__(
            self,
            pars
    ):
        super().__init__()

        self.n_iterations = pars.n_iterations
        self.n_neurons = pars.n_neurons
        self.n_muscle_cells = pars.n_muscle_cells
        self.timestep = pars.timestep
        self.times = np.linspace(
            0,
            self.n_iterations *
            self.timestep,
            self.n_iterations)
        self.pars = pars

        self.n_eq = self.n_neurons*4 + self.n_muscle_cells*2 + self.n_neurons * \
            2  # number of equations: number of CPG eq+muscle cells eq+sensors eq
        self.muscle_l = 4*self.n_neurons + 2 * \
            np.arange(0, self.n_muscle_cells)  # muscle cells left indexes
        self.muscle_r = self.muscle_l+1  # muscle cells right indexes
        self.all_muscles = 4*self.n_neurons + \
            np.arange(0, 2*self.n_muscle_cells)  # all muscle cells indexes
        # vector of indexes for the CPG activity variables - modify this
        # according to your implementation
        self.all_v = range(self.n_neurons*2)

        self.r_L_ind = 2*np.arange(0, self.n_neurons)
        self.r_R_ind = self.r_L_ind + 1
        self.a_L_ind = 2*np.arange(self.n_neurons, self.n_neurons*2)
        self.a_R_ind = self.a_L_ind + 1
        self.m_L_ind = self.muscle_l
        self.m_R_ind = self.muscle_r

        pylog.warning(
            "Implement here the vectorization indexed for the equation variables")

        self.state = np.zeros([self.n_iterations, self.n_eq])  # equation state
        self.dstate = np.zeros([self.n_eq])  # derivative state
        self.state[0] = np.random.rand(self.n_eq)  # set random initial state

        self.poses = np.array([
            0.007000000216066837,
            0.00800000037997961,
            0.008999999612569809,
            0.009999999776482582,
            0.010999999940395355,
            0.012000000104308128,
            0.013000000268220901,
            0.014000000432133675,
            0.014999999664723873,
            0.01600000075995922,
        ])  # active joint distances along the body (pos=0 is the tip of the head)
        self.poses_ext = np.linspace(
            self.poses[0], self.poses[-1], self.n_neurons)  # position of the sensors

        # initialize ode solver
        self.f = self.ode_rhs

        # stepper function selection
        if self.pars.method == "euler":
            self.step = self.step_euler
        elif self.pars.method == "noise":
            self.step = self.step_euler_maruyama
            # vector of noise for the CPG voltage equations (2*n_neurons)
            self.noise_vec = np.zeros(self.n_neurons*2)

        # zero vector activations to make first and last joints passive
        # pre-computed zero activity for the first 4 joints
        self.zeros8 = np.zeros(8)
        # pre-computed zero activity for the tail joint
        self.zeros2 = np.zeros(2)

        # parameters
        self.tau = self.pars.tau
        self.tau_a = self.pars.taua
        self.gamma = self.pars.gamma
        self.I = self.pars.I
        self.Idiff = self.pars.Idiff
        self.b = self.pars.b
        self.g_in = self.pars.g_in
        # g_ss = self.pars.g_ss
        self.taua_m = self.pars.taua_m
        self.taud_m = self.pars.taud_m
        self.g_mc = self.pars.g_mc
        self.W_in = self.connectivity_matrix(self.n_neurons, 1, 2)
        # W_ss = self.connectivity_matrix(self.n_neurons, 10, 0)
        self.W_mc = self.connectivity_matrix_CPGtoMuscle(self.n_neurons, self.n_muscle_cells, self.pars.n_mc)

    def get_ou_noise_process_dw(self, timestep, x_prev, sigma):
        """
        Implement here the integration of the Ornstein-Uhlenbeck processes
        dx_t = -0.5*x_t*dt+sigma*dW_t
        Parameters
        ----------
        timestep: <float>
            Timestep
        x_prev: <np.array>
            Previous time step OU process
        sigma: <float>
            noise level
        Returns
        -------
        x_t{n+1}: <np.array>
            The solution x_t{n+1} of the Euler Maruyama scheme
            x_new = x_prev-0.1*x_prev*dt+sigma*sqrt(dt)*Wiener
        """

        dx_process = np.zeros_like(x_prev)

    def step_euler(self, iteration, time, timestep, pos=None):
        """Euler step"""
        self.state[iteration+1, :] = self.state[iteration, :] + \
            timestep*self.f(time, self.state[iteration], pos=pos)
        return np.concatenate([
            self.zeros8,  # the first 4 passive joints
            self.motor_output(iteration),  # the active joints
            self.zeros2  # the last (tail) passive joint
        ])

    def step_euler_maruyama(self, iteration, time, timestep, pos=None):
        """Euler Maruyama step"""
        self.state[iteration+1, :] = self.state[iteration, :] + \
            timestep*self.f(time, self.state[iteration], pos=pos)
        self.noise_vec = self.get_ou_noise_process_dw(
            timestep, self.noise_vec, self.pars.noise_sigma)
        self.state[iteration+1, self.all_v] += self.noise_vec
        self.state[iteration+1,
                   self.all_muscles] = np.maximum(self.state[iteration+1,
                                                             self.all_muscles],
                                                  0)  # prevent from negative muscle activations
        return np.concatenate([
            self.zeros8,  # the first 4 passive joints
            self.motor_output(iteration),  # the active joints
            self.zeros2  # the last (tail) passive joint
        ])

    def motor_output(self, iteration):
        """
        Here you have to final muscle activations for the 10 active joints.
        It should return an array of 2*n_muscle_cells=20 elements,
        even indexes (0,2,4,...) = left muscle activations
        odd indexes (1,3,5,...) = right muscle activations
        """
        #_______________________________________________________________________________________
        # To complete
        muscles = np.zeros(2*self.n_muscle_cells)
        i_L = np.arange(0, 19, 2)
        i_R = np.arange(1, 20, 2)
        muscles[i_L] = self.pars.act_strength*self.state[iteration][self.m_L_ind]
        muscles[i_R] = self.pars.act_strength*self.state[iteration][self.m_R_ind]
        #_______________________________________________________________________________________
        
        return muscles # np.zeros(2 * self.n_muscle_cells)  # here you have to final active muscle equations for the 10 joints
    

    def F_sqrt(self, x):
        return np.sqrt(np.maximum(x,0))


    def connectivity_matrix(self, n_neurons, n_asc, n_desc):
        """
        Implement here the connectivity matrix
        Parameters
        ----------
        n_neurons: <int>
            Number of neurons
        n_asc: <int>
            Number of ascending connections
        n_desc: <int>
            Number of descending connections
        Returns
        -------
        W: <np.array>
            Connectivity matrix "CPG to CPG" or "stetch to CPG"
        """
        #_______________________________________________________________________________________
        # To complete
        W = np.zeros((n_neurons, n_neurons))
        
        for i in range(n_neurons):
            for j in range(n_neurons):
                if i<=j and j-i<=n_desc:
                    W[i,j] = 1/(j-i+1)
                elif i>j and i-j<=n_asc:
                    W[i,j] = 1/(i-j+1)
                else: # otherwise
                    W[i,j] = 0
        #_______________________________________________________________________________________
        return W
    
    def connectivity_matrix_CPGtoMuscle(self, n_neurons, n_muscle_cells, n_mc):
        """
        Implement here the connectivity matrix
        Parameters
        ----------
        n_neurons: <int>
            Number of neurons
        n_muscle_cells: <int>
            Number of muscle cells
        Returns
        -------
        W_mc: <np.array>
            Connectivity matrix CPG to muscle
        """
        #_______________________________________________________________________________________
        W_mc = np.zeros((n_muscle_cells, n_neurons))
        
        for i in range(n_muscle_cells):
            for j in range(n_neurons):
                if n_mc*i <= j <= n_mc*(i+1)-1:
                    W_mc[i,j] = 1
                else:
                    W_mc[i,j] = 0
        #_______________________________________________________________________________________
        return W_mc

    #_______________________________________________________________________________________
    
    def ode_rhs(self,  _time, state, pos=None):
        """Network_ODE
        You should implement here the right hand side of the system of equations
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

        self.r_L = state[self.r_L_ind]
        self.r_R = state[self.r_R_ind]
        self.a_L = state[self.a_L_ind]
        self.a_R = state[self.a_R_ind]
        self.m_L = state[self.m_L_ind]
        self.m_R = state[self.m_R_ind]

        # ODEs
        drdt_L = 1/self.tau * (-self.r_L + self.F_sqrt(self.I + self.Idiff - self.b*self.a_L - self.g_in*self.W_in.T.dot(self.r_R)))
        drdt_R = 1/self.tau * (-self.r_R + self.F_sqrt(self.I - self.Idiff - self.b*self.a_R - self.g_in*self.W_in.T.dot(self.r_L)))

        dadt_L = 1/self.tau_a * (-self.a_L + self.gamma*self.r_L)
        dadt_R =  1/self.tau_a * (-self.a_R + self.gamma*self.r_R)

        dmdt_L = self.g_mc * self.W_mc.dot(self.r_L) * (1 - self.m_L)/self.taua_m - self.m_L/self.taud_m
        dmdt_R = self.g_mc * self.W_mc.dot(self.r_R) * (1 - self.m_R)/self.taua_m - self.m_R/self.taud_m

        
        self.dstate[self.r_L_ind] = drdt_L
        self.dstate[self.r_R_ind] = drdt_R
        self.dstate[self.a_L_ind] = dadt_L
        self.dstate[self.a_R_ind] = dadt_R
        self.dstate[self.m_L_ind] = dmdt_L
        self.dstate[self.m_R_ind] = dmdt_R

        #_______________________________________________________________________________________

        return self.dstate
