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

        #_______________________________________________________________________________________

        
        return muscles # np.zeros(2 * self.n_muscle_cells)  # here you have to final active muscle equations for the 10 joints
    
    #_______________________________________________________________________________________
    # Add by Clara
    def F(x):
        return np.sqrt(max(x, 0))
    #_______________________________________________________________________________________
    # Add by Shu
    def F_sqrt(self, x):
        return np.sqrt(np.maximum(x,0))

    def F_max(self, x):
        return np.maximum(x,0)

    def F_sigmoid(self, x):
        return 1/(1+np.exp(-self.pars.lam*(x-self.pars.theta)))
    
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
    
    def connectivity_matrix_CPGtoMuscle(self, n_neurons, n_muscle_cells):
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
        # To complete
        W_mc = np.zeros((n_muscle_cells, n_neurons))
        
        for i in range(n_muscle_cells):
            for j in range(n_neurons):
                if n_muscle_cells*i <= j <= n_muscle_cells*(i+1)-1:
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
        #_______________________________________________________________________________________
        # Add by Clara
        tau = self.pars.tau
        tau_a = self.pars.taua
        gamma = self.pars.gamma
        I = self.pars.I
        b = self.pars.b
        g_in = self.pars.g_in
        g_ss = self.pars.g_ss

        # W_in = self.pars.W_in # is it the inhibitory strength?
        W_in = self.connectivity_matrix(self.n_neurons, 1, 2)
        W_ss = self.connectivity_matrix(self.n_neurons, 10,0)
        # W_mc = self.connectivity_matrix_CPGtoMuscle(self.n_neurons, self.n_muscle_cells)

        # r_L, a_L, r_R, a_R = np.split(state, 4)
        
        # vector of left neuron activities
        r_L = state[0:self.n_neurons]
        a_L = state[self.n_neurons:2*self.n_neurons]

        # vector of right neuron activities
        r_R = state[2*self.n_neurons:3*self.n_neurons]
        a_R = state[3*self.n_neurons:4*self.n_neurons]

        print(state.shape)

        drdt_L = 1/tau * (-r_L + self.F_sqrt(I - b*a_L - g_in*W_in.dot(r_R)))
        drdt_R = 1/tau * (-r_R + self.F_sqrt(I - b*a_R - g_in*W_in.dot(r_L)))
        
        # idea shu
        # drdt_R = 1/tau * (-r_R + self.F_sqrt(I - b*a_R - g_in*W_in.dot(r_L)-g_ss*W_ss.dot(s_L)))

        dadt_L = 1/tau_a * (-a_L + gamma*r_L)
        dadt_R =  1/tau_a * (-a_R + gamma*r_R)

        self.dstate = np.concatenate((drdt_L, dadt_L, drdt_R, dadt_R))
        #_______________________________________________________________________________________

        return self.dstate

