

"""
File of metrics computations
"""

import numpy as np
from scipy.signal import butter, filtfilt, find_peaks, fftconvolve

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
    if all(periods):
        return 1/np.mean(periods)
    else:
        return 0.0


def compute_frequency_fft(
    times: np.ndarray,
    signals: np.ndarray,
):
    ''' Computes the average frequency based on the FFT '''

    dt_sig = times[1]-times[0]
    n_step = len(times)

    # Filter high-frequency noise
    smooth_signals = signals.copy()
    smooth_signals = remove_signals_offset(smooth_signals)
    # smooth_signals = filter_signals(smooth_signals, dt_sig, fcut_lp=50)

    # Compute FFT
    signals_fft = np.fft.fft(smooth_signals, axis=1)
    freqs = np.fft.fftfreq(n_step, d=dt_sig)

    signals_fft_mod = np.abs(signals_fft)
    ind_max_signals = np.argmax(signals_fft_mod[:, :n_step//2], axis=1)
    freq_max_signals = freqs[ind_max_signals-1]

    return freq_max_signals, ind_max_signals


def compute_ipls_corr(
    times: np.ndarray,
    signals: np.ndarray,
    inds_couples: list
) -> np.ndarray:
    '''
    Computes the IPL evolution based on the cross correlation of signals.
    Returns the IPLs between adjacent signals
    '''
    n_couples = len(inds_couples)
    dt_sig = times[1] - times[0]
    ipls = np.zeros(n_couples)

    signals_f = (np.mean(signals, axis=1) - signals.T).T

    for ind_couple, (ind1, ind2) in enumerate(inds_couples):
        sig1 = signals_f[ind1]
        sig2 = signals_f[ind2]

        xcorr = np.correlate(sig1, sig2, mode="full")
        n_lag = np.argmax(xcorr) - len(xcorr) // 2

        t_lag = n_lag * dt_sig

        ipls[ind_couple] = t_lag

    return ipls


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


def compute_metrics(
        network
):
    metrics = {}

    n_iterations = network.pars.n_iterations
    sim_fraction = 0.8
    nsteps_considered = round(n_iterations * sim_fraction)

    # consider only a number of steps
    times = network.times[-nsteps_considered:]
    signals = network.state[-nsteps_considered:, :]

    v1 = signals[:, 0]
    half_width = (np.max(v1)-np.min(v1))/2
    frequency = compute_frequency_treshold_crossings(
        times, signals[:, [0]].transpose(), theta=np.min(signals)+0.25*half_width
    )
    metrics["frequency"] = frequency  # frequency of the state[:,0]

    metrics["amp"] = np.max(v1)-np.min(v1)  # amplitude of the state[:,0]

    if signals.shape[1] > 2:
        # ipls (in % of the cycle duration) study of the synchronization
        # between two coupled units
        metrics["sync"] = compute_ipls_corr(
            times, signals[:, :].transpose(), inds_couples=[[0, 2]]
        )[0] * metrics["frequency"]
        if metrics["sync"] < 0:
            metrics["sync"] = -metrics["sync"]

    # # unused metrics
    # freqs_max, _ = compute_frequency_fft(
    #     times, signals.transpose()
    # )
    # metrics["frequency2"] = np.mean(freqs_max)

    # ptcc = compute_ptcc(
    #         times,
    #         signals.transpose(),
    #         )
    # metrics["ptcc"] = np.min( ptcc )

    return metrics

