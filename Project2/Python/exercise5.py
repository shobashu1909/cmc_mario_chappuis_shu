

from simulation_parameters import SimulationParameters
from util.run_closed_loop import run_multiple, run_single 
import numpy as np
import farms_pylog as pylog
import os
import matplotlib.pyplot as plt

from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows, plot_2d, plot_1d, plot_1d_merge
from util.rw import load_object


def exercise5(**kwargs):

    pylog.info("Ex 5")
    pylog.info("Implement exercise 5")
    log_path = './logs/exercise5/'
    os.makedirs(log_path, exist_ok=True)

    #===========================================================================
    # # run an individual simulations with default parameters
    # # visualize the swimming behvior and test its performance
    # all_pars = SimulationParameters(
    #     n_iterations=5001,
    #     log_path=log_path,
    #     compute_metrics=3,
    #     return_network=True,
    #     **kwargs
    # )

    # pylog.info("Running the simulation")
    # controller = run_single(
    #     all_pars
    # )

    # pylog.info("Plotting the result")

    # # plot the center of mass trajectory ?
    # plt.figure("trajectory_single")
    # plot_trajectory(controller)
    
    # plt.savefig("trajectory_single_1.png")


    # # plot the left and right muscle activities
    # left_idx = controller.muscle_l
    # right_idx = controller.muscle_r

    # plt.figure('muscle_activities_single')
    # plot_left_right(
    #     controller.times,
    #     controller.state,
    #     left_idx,
    #     right_idx,
    #     cm="green",
    #     offset=0.1
    # )

    # plt.savefig("muscle_activities_single_1.png")

    # # plot CPG activities
    # plt.figure('CPG_activities_single')
    # plot_left_right(
    #     controller.times,
    #     controller.state,
    #     controller.r_L_ind,
    #     controller.r_R_ind,
    #     cm='green',
    #     offset=0.1    
    # )

    # plt.savefig("CPG_activities_single_I_4.png")
    #===========================================================================

    #===========================================================================
    pylog.info("Test the ability of turning by applying a differential drive Idiff in [0;4]")

    nsim = 10

    pars_list = [
        SimulationParameters(
            simulation_i = i,
            n_iterations = 10001,
            frequency = 3.4479310689620735,
            # ipls = 0.19689468749999772, 
            wavefrequency = 0.6788793103448205, 
            # ptcc = 1.9272312875880733,
            amp = 1.838618356662702,
            log_path = log_path,
            video_record = False,
            compute_metrics = 3,
            Idiff = Idiff,
            headless = True,
            print_metrics = True,
            return_network = True
        )
        for i, Idiff in enumerate(np.linspace(0, 4, nsim))
    ]
    # Run the simulations
    pylog.info("Running the simulation")
    # controllers = run_multiple(pars_list, num_process=16)

    # # # plot CPG activities
    # # for i in range(nsim):
    # #     controller = load_object(log_path+"controller"+str(i))
    # #     plot_left_right(
    # #         controller.times,
    # #         controller.state,
    # #         controller.r_L_ind,
    # #         controller.r_R_ind,
    # #         cm='green',
    # #         offset=0.1    
    # #     )

    # #     # save figures
    # #     plt.savefig("CPG_activities_single_"+str(i)+".png")
    # # plt.figure('CPG_activities_single', figsize=[15, 15])
    # for i in range(nsim):
    #     controller = load_object(log_path+"controller"+str(i))
    #     plot_left_right(
    #         controller.times,
    #         controller.state,
    #         controller.r_L_ind,
    #         controller.r_R_ind,
    #         cm='green',
    #         offset=0.1    
    #     )
    #     # save figures
    #     plt.savefig("ex_5_CPG_activities_single_"+str(i)+"_nsim10.png")
    
    # plt.figure('Trajectory', figsize=[15, 15])
    # # plot the center of mass trajectory
    # for i in range(nsim):
    #     controller = load_object(log_path+"controller"+str(i))
    #     sim_fraction = 1
    #     head_positions = np.array(controller.links_positions)[:, 0, :]
    #     n_steps = head_positions.shape[0]
    #     n_steps_considered = round(n_steps * sim_fraction)

    #     head_positions = head_positions[-n_steps_considered:, :2]

    #     """Plot head positions"""
    #     plt.plot(head_positions[:-1, 0],head_positions[:-1, 1], label="Idiff = "+str(round(controller.pars.Idiff,2)), )
    #     # label each plot
        
    # plt.xlabel('x [m]')
    # plt.ylabel('y [m]')
    # plt.axis('equal')
    # plt.grid(True)
    # plt.legend()

    # # plot_trajectory(controller)

    # # save figure
    # plt.savefig("ex_5_trajectory_nsim10.png")
    
    # # # plot the left and right muscle activities
    # # for i in range(nsim):
    # #     controller = load_object(log_path+"controller"+str(i))
    # #     left_idx = controller.muscle_l
    # #     right_idx = controller.muscle_r

    # #     plot_left_right(
    # #         controller.times,
    # #         controller.state,
    # #         left_idx,
    # #         right_idx,
    # #         cm="green",
    # #         offset=0.1
    # #     )

    #     # # save figures
    #     # plt.savefig("muscle_activities_single_"+str(i)+".png")


    # # # plot the turning performance
    # # curvature
    curvature = np.zeros([nsim, 2])

    for i in range(nsim):
        controller = load_object(log_path+"controller"+str(i))
        curvature[i] = [
            controller.pars.Idiff,
            np.mean(controller.metrics["curvature"])
        ]
    
    # plt.figure('curvature', figsize=[12, 3])
    # plot_1d(
    #     curvature,
    #     ["Idiff", "curvature"],
    #     cmap='nipy_spectral'
    # )
    # plt.savefig("ex_5_Idiff_vs_curvature_nsim10.png")

    # # lateral speed
    lateral_speed = np.zeros([nsim, 2])

    for i in range(nsim):
        controller = load_object(log_path+"controller"+str(i))
        lateral_speed[i] = [
            controller.pars.Idiff,
            np.mean(controller.metrics["lspeed_cycle"])
        ]
    
    # plt.figure('lateral_speed', figsize=[12, 3])
    # plot_1d(
    #     lateral_speed,
    #     ["Idiff", "lateral_speed"],
    #     cmap='nipy_spectral'
    # )
    # plt.savefig("ex5_Idiff_vs_lspeed_nsim10.png")

    # check that the turning radius match the curvature expected from the trajectory
    # plot the center of mass activities for fixed Idiff=0 and Idiff > 0

    # Create subplots in a 2x1 grid
    fig, axs = plt.subplots(2, 1, figsize=[12, 6], sharex=True)

    # Plot each metric on a subplot
    plot_1d_merge(axs[0], curvature, ["Idiff", "curvature"], cmap='blue')
    plot_1d_merge(axs[1], lateral_speed, ["Idiff", "lateral_speed"], cmap='red')

    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig("ex_5_Idiff_vs_metrics_nsim10.png")
    plt.show()

    #===========================================================================






if __name__ == '__main__':
    # for visualization
    exercise5(headless=True)
    plt.show()

