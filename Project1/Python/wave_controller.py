"""Network controller"""

import numpy as np
import farms_pylog as pylog


class WaveController:

    """Test controller"""

    def __init__(self, pars):
        self.pars = pars
        self.timestep = pars.timestep
        self.times = np.linspace(
            0,
            pars.n_iterations *
            pars.timestep,
            pars.n_iterations)
        self.n_joints = pars.n_joints

        # state array for recording all the variables
        self.state = np.zeros((pars.n_iterations, 2*self.n_joints))

        pylog.warning(
            "Implement below the step function following the instructions here and in the report")

        # indexes of the left muscle activations (optional)
        self.muscle_l = 2*np.arange(15)
        # indexes of the right muscle activations (optional)
        self.muscle_r = self.muscle_l+1
    
    def calculate_MLi(self, t, A, f, epsilon, n_joints, i):
        return 0.5 + A/2 * np.sin((2*np.pi * (f*t - epsilon*i/n_joints)))

    def calculate_MRi(self, t, A, f, epsilon, n_joints, i):
        return 0.5 - A/2 * np.sin((2*np.pi * (f*t - epsilon*i/n_joints)))

    def step(self, iteration, time, timestep, pos=None):
        """
        Step function. This function passes the activation functions of the muscle model
        Inputs:
        - iteration - iteration index
        - time - time vector
        - timestep - integration timestep
        - pos (not used) - joint angle positions

        Implement here the control step function,
        it should return an array of 2*n_joint=30 elements,
        even indexes (0,2,4,...) = left muscle activations
        odd indexes (1,3,5,...) = right muscle activations

        In addition to returning the activation functions, store
        them in self.state for later use offline
        """

        A = self.pars.amplitude
        f = self.pars.frequency
        epsilon = self.pars.wave_frequency
        n_joints = self.n_joints
        activation_functions = np.zeros(n_joints*2)

        for i in range(n_joints*2):
            if i%2 == 0:
                activation_functions[i] = self.calculate_MLi(time, A, f, epsilon, n_joints, i)
            else:
                activation_functions[i] = self.calculate_MRi(time, A, f, epsilon, n_joints, i)
        
        self.state[iteration] = activation_functions

        return activation_functions

