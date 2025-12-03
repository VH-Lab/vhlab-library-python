import os
import numpy as np

def getstimdirectorytime(dirname, **kwargs):
    """
    Get the time that a recording was made

    :param dirname: Directory name
    :param kwargs:
        WarnOnEarlyMorning (bool, default True)
        EarlyMorningCutOffTime (float, default 5)
        ErrorIfEmpty (bool, default True)
    :return: time in seconds since midnight on the first day of the experiment
    """

    error_if_empty = kwargs.get('ErrorIfEmpty', True)
    early_morning_cutoff_time = kwargs.get('EarlyMorningCutOffTime', 5)
    warn_on_early_morning = kwargs.get('WarnOnEarlyMorning', True)

    time_val = np.nan

    fname1 = os.path.join(dirname, 'stims.mat')
    fname2 = os.path.join(dirname, 'spike2data.smr')
    fname3 = os.path.join(dirname, 'filetime.txt')

    # MATLAB: if exist(fname1)==2&exist(fname2)==2&exist(fname3)==2
    # It checks if all three exist?
    # Actually, filetime.txt seems to be the one read.
    # The logic seems to imply that if all exist, we read fname3.
    # What if only fname3 exists?
    # MATLAB code:
    # if exist(fname1)==2&exist(fname2)==2&exist(fname3)==2
    # This condition is quite strict. All 3 files must exist.

    if os.path.isfile(fname1) and os.path.isfile(fname2) and os.path.isfile(fname3):
        try:
            with open(fname3, 'r') as f:
                content = f.read().strip()
                time_val = float(content)
        except ValueError:
            if error_if_empty:
                raise ValueError(f"Could not read time from {fname3}")

        is_early_morning = False
        if early_morning_cutoff_time is not None and not np.isnan(early_morning_cutoff_time):
            if time_val < early_morning_cutoff_time * 60 * 60:
                is_early_morning = True
                time_val += 24 * 60 * 60

        if is_early_morning and warn_on_early_morning:
            print(f"Warning: For directory {dirname}, the function GETSTIMDIRECTORYTIME is assuming that recordings between midnight and {early_morning_cutoff_time} were done the next day.")

    else:
        if error_if_empty:
            raise FileNotFoundError(f"No time information found for directory {dirname} (requires stims.mat, spike2data.smr, and filetime.txt).")

    return time_val
