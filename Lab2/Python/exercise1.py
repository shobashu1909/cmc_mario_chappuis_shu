""" Lab 4 """

import matplotlib.pyplot as plt
import numpy as np
from nptyping import NDArray

import farms_pylog as pylog
from cmcpack import DEFAULT, integrate, parse_args
from cmcpack.plot import bioplot, save_figure
from pendulum_system import PendulumSystem
from system_animation import SystemAnimation
from system_parameters import PendulumParameters

DEFAULT['label'] = [r'$\theta$ [rad]', r'$d\theta/dt$ [rad/s]']

# pylint: disable=invalid-name


def pendulum_integration(state: NDArray[(2,), float], time: float, *args):
    """ Function for system integration with no perturbations.
    """
    pylog.warning(
        'Pendulum equation with spring and damper must be implemented'
    )
    pendulum = args[0]
    return pendulum.pendulum_system(
        state[0], state[1], time, torque=0.0,
    )[:, 0]


def pendulum_unperturbed(
        state: NDArray[(2,), float],
        time: float,
        *args,
) -> NDArray[(2,), float]:
    """ Function for system integration with perturbations.
    Setup your time based system pertubations within this function.
    The pertubation can either be applied to the states or as an
    external torque.
    """
    pendulum = args[0]
    return pendulum.pendulum_system(
        state[0], state[1], time, torque=0,
    )[:, 0]


def pendulum_perturbation(
        state: NDArray[(2,), float],
        time: float,
        *args,
) -> NDArray[(2,), float]:
    """ Function for system integration with perturbations.
    Setup your time based system pertubations within this function.
    The pertubation can either be applied to the states or as an
    external torque.
    """
    pendulum = args[0]
    pert_type = 'speed' if len(args) == 1 else args[1]
    torque = 0.0
    if 5 < time < 5.1:
        # pylog.info('Applying state perturbation to pendulum_system')
        if pert_type == 'speed':
            state[1] = 2.
        elif pert_type == 'angle':
            state[0] = -1.
        elif pert_type == 'torque':
            torque = 4.
    return pendulum.pendulum_system(
        state[0], state[1], time, torque=torque,
    )[:, 0]


def exercise1():
    """ Exercise 1  """
    pylog.info('Executing Lab 4 : Exercise 1')
    pendulum = PendulumSystem()
    pendulum.parameters = PendulumParameters()

    pylog.info(
        'Find more information about'
        ' Pendulum Parameters in SystemParameters.py'
    )
    pylog.info('Executing Lab 4 : Exercise 1')

    # Initialize a new pendulum system with default parameters
    pendulum = PendulumSystem()
    pendulum.parameters = PendulumParameters()

    pylog.info(
        'Find more information about'
        ' Pendulum Parameters in SystemParameters.py'
    )

    # To change a parameter you could so by,
    # >>> pendulum.parameters.L = 1.5
    # The above line changes the length of the pendulum

    # You can instantiate multiple pendulum models with different parameters
    # For example,

    # >>> pendulum_1 = PendulumSystem()
    # >>> pendulum_1.parameters = PendulumParameters()
    # >>> pendulum_1.parameters.L = 0.5
    # >>> parameters_2 = PendulumParameters()
    # >>> parameters_2.L = 0.5
    # >>> pendulum_2 = PendulumSystem(paramters=parameters_2)

    # Above examples shows how to create two istances of the pendulum
    # and changing the different parameters using two different approaches

    pylog.warning('Loading default pendulum pendulum.parameters')
    pylog.info(pendulum.parameters.show_parameters())

    # Simulation Parameters
    t_start = 0.0
    t_stop = 10.0
    dt = 0.01
    pylog.warning('Using large time step dt=%s', dt)
    time = np.arange(t_start, t_stop, dt)
    x0 = [0.5, 0.0]

    res = integrate(pendulum_integration, x0, time, args=(pendulum,))
    pylog.info('Instructions for applying pertubations')
    # Use pendulum_perturbation method to apply pertubations
    # Define the pertubations inside the function pendulum_perturbation
    # res = integrate(pendulum_perturbation, x0, time, args=(pendulum,))
    res.plot_state('State')
    res.plot_phase('Phase')

    # To animate the model, use the SystemAnimation class
    # Pass the res(states) and systems you wish to animate
    simulation = SystemAnimation(
        res,
        pendulum,
        handler='Simple Pendulum (without using spring and damper)'
    )
    # If you want to disable the parameters in the animation plot
    # simulation2 = SystemAnimation(
    #     res,
    #     pendulum,
    #     handler='Simple pendulum 2',
    #     show_parameters=False,
    # )
    # To start the animation, use either simulation.animate() or plt.show()
    # simulation.animate()

    if DEFAULT['save_figures'] is False:
        plt.show()


if __name__ == '__main__':
    parse_args()
    exercise1()

