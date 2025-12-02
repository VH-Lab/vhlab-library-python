def spiketriggeredaverage(spiketimes, signal, signal_t, window):
    """
    Computes spike-triggered average of a signal.

    :param spiketimes: list or array of spike times
    :param signal: array of signal values
    :param signal_t: array of time points for signal
    :param window: tuple (pre, post) window around spike in seconds (e.g., [-0.1, 0.1])
    :return: tuple (sta, t_sta, num_spikes)
    """
    import numpy as np

    # Simple implementation using numpy
    # Identify sample rate from signal_t
    if len(signal_t) < 2:
        return None, None, 0

    dt = signal_t[1] - signal_t[0]

    # Indices window
    n_pre = int(abs(window[0]) / dt)
    n_post = int(abs(window[1]) / dt)

    sta = np.zeros(n_pre + n_post + 1)
    count = 0

    signal_arr = np.array(signal)

    # Map spike times to indices
    # This assumes linear time signal_t start at 0 or whatever
    # idx = (t - t0) / dt
    t0 = signal_t[0]

    for st in spiketimes:
        if st < signal_t[0] or st > signal_t[-1]:
            continue

        idx = int((st - t0) / dt)

        start_idx = idx - n_pre
        end_idx = idx + n_post + 1

        if start_idx >= 0 and end_idx <= len(signal_arr):
            sta += signal_arr[start_idx:end_idx]
            count += 1

    if count > 0:
        sta /= count

    t_sta = np.arange(-n_pre, n_post + 1) * dt

    return sta, t_sta, count
