

"""
File of metrics computations
"""

import numpy as np
from scipy.signal import butter, filtfilt, find_peaks, fftconvolve
import sys


def sum_torques(joints_data, sim_fraction=1.0):
    """Compute sum of torques"""
    nsteps = joints_data.shape[0]
    nsteps_considered = round(nsteps * sim_fraction)
    return np.sum(np.abs(joints_data[-nsteps_considered:, :]))

def cost_of_transport(network, sim_fraction=0.3):
    """
    Compute the cost of transport = torque / speed
    """
    mass = 0.00005022324522733332 #[kg]
    (fspeed,lspeed) = compute_speed_cycle(network, sim_fraction=sim_fraction)
    torque = sum_torques(network.joints_active_torques, sim_fraction=sim_fraction)
    speed = np.sqrt(np.mean(fspeed)**2 + np.mean(lspeed)**2)

    # compute the Distance Traveled with the speed
    distance  = speed * network.times[-1]

    return torque / (distance*mass)

def compute_speed_cycle(
    network,
    sim_fraction: float = 1.0,
):
    """
    Compute forward and lateral speeds using the xy joint positions
    sampled across cycles using the frequency computed using the
    treshold crossing method
    """

    n_steps = network.links_positions.shape[0]
    n_steps_considered = round(n_steps * sim_fraction)
    links_pos_xy = network.links_positions[-n_steps_considered:, :, :2]

    # compute freq based on the state
    times = network.times[-n_steps_considered:]
    state = network.state[-n_steps_considered:]
    muscle_diff = state[:, network.muscle_l]-state[:, network.muscle_r]

    frequency, _ = compute_frequency_treshold_crossings(
        times, muscle_diff.T, theta=0.0)

    if frequency > 0:
        sampling_rate = int(1/(frequency*network.pars.timestep))
        sampling_idxs = np.arange(0, n_steps_considered, sampling_rate)
        sampled_pos = links_pos_xy[sampling_idxs, 0, :]  # head pos

        vel = frequency*(sampled_pos[1:]-sampled_pos[:-1])  # head velocity

        nsamples = len(sampling_idxs)
        v_fwd = np.zeros(nsamples-1)
        v_lat = np.zeros(nsamples-1)
        for idx in range(nsamples-2):
            #
            p_head_fwd0 = links_pos_xy[sampling_idxs[idx],
                                       0, :]-links_pos_xy[sampling_idxs[idx], 1, :]
            move_direction0 = p_head_fwd0/np.linalg.norm(p_head_fwd0)
            angles = []
            theta = np.arctan2(move_direction0[1], move_direction0[0])

            for idx2 in range(sampling_idxs[idx]+1, sampling_idxs[idx+1]):
                # to avoid the bias from the arctan switching sign at theta=pi
                # we sum across small dthetas in each iteration
                p_head_fwd = links_pos_xy[idx2, 0, :]-links_pos_xy[idx2, 1, :]
                move_direction = p_head_fwd/np.linalg.norm(p_head_fwd)

                cos_dtheta = np.dot(move_direction0, move_direction)
                sin_dtheta = np.cross(move_direction0, move_direction)
                dtheta = np.arctan2(sin_dtheta, cos_dtheta)

                theta = theta + dtheta
                angles.append(theta)
                move_direction0 = move_direction

            mean_angle = np.mean(angles)
            ht_direction = np.array([np.cos(mean_angle), np.sin(mean_angle)])
            ht_direction = ht_direction/np.linalg.norm(ht_direction)

            vec_left = np.cross(
                [0, 0, 1],
                [ht_direction[0], ht_direction[1], 0]
            )[:2]
            v_fwd[idx+1] = np.dot(vel[idx+1], ht_direction)
            v_lat[idx+1] = np.dot(vel[idx+1], vec_left)

        return v_fwd[1:], v_lat[1:]
    else:
        return 0.0, 0.0


def compute_speed_PCA(links_positions, links_vel, sim_fraction=1.0):
    '''
    Computes the axial and lateral speed based on the PCA of the links positions
    '''

    n_steps = links_positions.shape[0]
    n_steps_considered = round(n_steps * sim_fraction)

    links_pos_xy = links_positions[-n_steps_considered:, :, :2]
    joints_vel_xy = links_vel[-n_steps_considered:, :, :2]
    time_idx = links_pos_xy.shape[0]

    speed_forward = []
    speed_lateral = []

    for idx in range(time_idx):
        x = links_pos_xy[idx, :, 0]
        y = links_pos_xy[idx, :, 1]

        pheadtail = links_pos_xy[idx][0]-links_pos_xy[idx][-1]  # head - tail
        vcom_xy = np.mean(joints_vel_xy[idx], axis=0)

        covmat = np.cov([x, y])
        eig_values, eig_vecs = np.linalg.eig(covmat)
        largest_index = np.argmax(eig_values)
        largest_eig_vec = eig_vecs[:, largest_index]

        ht_direction = np.sign(np.dot(pheadtail, largest_eig_vec))
        largest_eig_vec = ht_direction * largest_eig_vec

        v_com_forward_proj = np.dot(vcom_xy, largest_eig_vec)

        left_pointing_vec = np.cross(
            [0, 0, 1],
            [largest_eig_vec[0], largest_eig_vec[1], 0]
        )[:2]

        v_com_lateral_proj = np.dot(vcom_xy, left_pointing_vec)

        speed_forward.append(v_com_forward_proj)
        speed_lateral.append(v_com_lateral_proj)

    return np.mean(speed_forward), np.mean(speed_lateral)


# ------= SIGNAL PROCESSING TOOLS ------=
def filter_signals(
    signals: np.ndarray,
    signal_dt: float,
    fcut_hp: float = None,
    fcut_lp: float = None,
    filt_order: int = 5,
):
    ''' Butterwort, zero-phase filtering '''

    # Nyquist frequency
    fnyq = 0.5 / signal_dt

    # Filters
    if fcut_hp is not None:
        num, den = butter(filt_order, fcut_hp/fnyq,  btype='highpass')
        signals = filtfilt(num, den, signals)

    if fcut_lp is not None:
        num, den = butter(filt_order, fcut_lp/fnyq, btype='lowpass')
        signals = filtfilt(num, den, signals)

    return signals


def remove_signals_offset(signals: np.ndarray):
    ''' Removed offset from the signals '''
    return (signals.T - np.mean(signals, axis=1)).T


def compute_frequency_treshold_crossings(
    times: np.ndarray,
    signals: np.ndarray,
    theta=0.1
):
    """
    Compute the frequency of a signal oscillating around a predefined treshold
    """

    onset_idxs = (signals[:, 1:] >= theta) * (signals[:, :-1] < theta)
    last_spikes = np.zeros(onset_idxs.shape[0])
    prec_spikes = np.zeros(onset_idxs.shape[0])
    for idx, onsets in enumerate(onset_idxs):
        onsets = onset_idxs[idx]
        all_spikes = times[:-1][onsets]
        # check if 1) all neurons have fired and 2) the last spike happened
        # after tstop/2 (or no oscillations at st)
        if len(all_spikes) > 1 and all_spikes[-1] > times[-1]/2:
            last_spikes[idx] = all_spikes[-1]
            prec_spikes[idx] = all_spikes[-2]
    periods = last_spikes - prec_spikes

    if all(periods):  # make sure that all neurons are oscillating
        period = np.mean(periods)
        phase_diffs = np.zeros(onset_idxs.shape[0]-1)
        for i in range(len(last_spikes)-1):
            dphi = last_spikes[i+1]-last_spikes[i]
            if dphi < -period/2:
                phase_diffs[i] = period+dphi
            elif dphi > period/2:
                phase_diffs[i] = dphi-period
            else:
                phase_diffs[i] = dphi
        frequency = 1/period
    else:
        frequency = 0.0
        phase_diffs = np.zeros(onset_idxs.shape[0])

    return frequency, phase_diffs


def compute_ptcc(
    times: np.ndarray,
    signals: np.ndarray,
    discard_time: float = 0,
    filtering: bool = True,
) -> np.ndarray:
    '''
    Computes the peak-to-through correlatio coefficient
    based on the difference between the the maximum and the minimum of the
    auto-correlogram of smoothened pools' oscillations
    '''

    sig_dt = times[1] - times[0]

    smooth_signals = signals.copy()
    if filtering:
        smooth_signals = filter_signals(smooth_signals, sig_dt, fcut_lp=10)

    # Remove offset and initial transient
    smooth_signals = remove_signals_offset(smooth_signals)

    istart = round(float(discard_time)/float(sig_dt))
    chopped_signals = smooth_signals[:, istart:]

    ptccs = []
    for ind, sig in enumerate(chopped_signals):

        # Auto-correlogram
        power = np.correlate(sig, sig)
        autocorr = fftconvolve(sig, sig[::-1], 'full')

        if power > 0:
            autocorr = autocorr / power
        else:
            autocorr = np.zeros(autocorr.shape)

        siglen = len(autocorr)//2   # Computed in [-n//2,+n//2-1]

        sig_maxs = find_peaks(+autocorr[siglen:])
        sig_mins = find_peaks(-autocorr[siglen:])

        if sig_maxs[0].size == 0 or sig_mins[0].size == 0:
            ptccs.append(0)
        else:
            first_max_ind = sig_maxs[0][0] + siglen
            first_min_ind = sig_mins[0][0] + siglen

            ptccs.append(autocorr[first_max_ind] - autocorr[first_min_ind])

    return np.array(ptccs)


def compute_controller(
        network
):
    """
    Compute all the metrics of the firing rate controller
    """
    metrics = {}

    n_iterations = network.pars.n_iterations
    sim_fraction = 0.3
    nsteps_considered = round(n_iterations * sim_fraction)

    # consider sim_fraction number of steps, for the difference between left
    # and right muscle cells
    times = network.times[-nsteps_considered:]
    signals = network.state[-nsteps_considered:,
                            network.muscle_r]-network.state[-nsteps_considered:,
                                                            network.muscle_l]

    frequency, iplss = compute_frequency_treshold_crossings(
        times, signals.transpose(), theta=0.001
    )
    # adding one element to consider the full body length
    iplss = np.append(iplss, iplss[-1])
    metrics["frequency"] = frequency
    metrics["ipls"] = np.sum(iplss)
    metrics["wavefrequency"] = metrics["ipls"]*metrics["frequency"]

    ptcc = compute_ptcc(
        times,
        signals.transpose(),
    )
    metrics["ptcc"] = np.min(ptcc)

    # ------ amplitude of the limbs at steady-state ------
    metrics["amp"] = np.max(signals)-np.min(signals)

    return metrics


def compute_mechanical(
    network
):
    """
    compute all mechanical metrics
    """

    metrics = {}
    sim_fraction = 0.3

    # ------ COMPUTE FORWARD AND LATERAL SPEEDS ------
    links_positions = network.links_positions
    link_velocities = network.links_velocities
    joints_active_torques = network.joints_active_torques

    # method 1
    (fspeed, lspeed) = compute_speed_PCA(
        links_positions,
        link_velocities,
        sim_fraction=sim_fraction
    )
    metrics["fspeed_PCA"] = fspeed
    metrics["lspeed_PCA"] = lspeed

    # method 2
    (fspeed, lspeed) = compute_speed_cycle(
        network,
        sim_fraction=sim_fraction
    )
    metrics["fspeed_cycle"] = np.mean(fspeed)
    metrics["lspeed_cycle"] = np.mean(lspeed)

    # ------ Mechanical metrics ------
    torque = sum_torques(joints_active_torques, sim_fraction=sim_fraction)

    metrics["torque"] = torque

    if network.mujoco_error:
        metrics = dict.fromkeys(metrics, np.nan)

    # ------ Cost of transport ------
    
    cost = cost_of_transport(network, sim_fraction=sim_fraction)
    metrics["cost_of_transport"] = cost

    return metrics


def compute_all(network):
    """
    compute and joint all controller and mechanical metrics
    """

    if sys.version_info[1] <= 8:  # for python3.8 or lower
        metrics = {
            **compute_controller(network),
            **compute_mechanical(network)}
    else:
        metrics = compute_controller(network) | compute_mechanical(network)
    return metrics

