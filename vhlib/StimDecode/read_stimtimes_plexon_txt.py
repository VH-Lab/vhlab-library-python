import os
import numpy as np
from .read_plexon_events_txt import read_plexon_events_txt
try:
    from vlt.file.dirstruct import _load_mat_file
except ImportError:
    def _load_mat_file(filepath): raise NotImplementedError("vlt.file.dirstruct._load_mat_file missing")

def read_stimtimes_plexon_txt(dirname):
    """
    Interpret the stimtimes.txt file written by VH lab Spike2

    Reads the stimulus ids, stimulus times, and frame times for each stimulus
    from the 'stimtimes_plexon.txt' file located in the directory DIRNAME (full path
    needed).

    :param dirname: Directory name.
    :return: tuple (stimids, stimtimes, frametimes)
             stimids: vector containing the stim id of each stimulus presentation.
             stimtimes: vector with the time of stimulus onset.
             frametimes: list of vectors of the frame times.
    """

    fname = 'stimtimes_plexon.txt'
    fname_alt = 'stimtimes_plexon.mat'

    gotit = 0
    events = None

    if os.path.exists(os.path.join(dirname, fname_alt)):
        try:
            # Load specific variables
            # events = load([dirname filesep fname_alt],'FrameTrigger','StimulusTrigger','Strobed','-mat');
            # _load_mat_file loads all variables.
            events = _load_mat_file(os.path.join(dirname, fname_alt))
            # events.stimid = events.Strobed(:,2);
            # Check if Strobed exists and is 2D array
            if 'Strobed' in events:
                strobed = events['Strobed']
                # strobed might be numpy array.
                if len(strobed.shape) > 1 and strobed.shape[1] >= 2:
                    events['stimid'] = strobed[:, 1]
                else:
                    events['stimid'] = np.array([]) # Or handle error
            gotit = 1
        except Exception:
            pass

    if not gotit:
        events = read_plexon_events_txt(os.path.join(dirname, fname))

    if 'StimulusTrigger' in events:
        stimtimes = events['StimulusTrigger']
        # If scalar, make array
        if np.isscalar(stimtimes):
            stimtimes = np.array([stimtimes])
    else:
        stimtimes = np.array([])

    if 'FrameTrigger' in events:
        frame_triggers = events['FrameTrigger']
        if np.isscalar(frame_triggers):
            frame_triggers = np.array([frame_triggers])
    else:
        frame_triggers = np.array([])

    frametimes = []

    # MATLAB:
    # for i=1:length(stimtimes),
    #   if i<length(stimtimes),
    #       matches = (events.FrameTrigger>=stimtimes(i)&events.FrameTrigger<stimtimes(i+1));
    #       frametimes{i} = events.FrameTrigger(matches);
    #       events.FrameTrigger= events.FrameTrigger(~matches); % drop the frametimes we just assigned
    #   else,
    #       frametimes{i} = events.FrameTrigger; % assign remaining frametimes to this stimulus
    #   end;
    # end;

    # We can assume frame_triggers is sorted? MATLAB code assumes it effectively by consuming it.

    current_ft = frame_triggers

    for i in range(len(stimtimes)):
        if i < len(stimtimes) - 1:
            t_start = stimtimes[i]
            t_end = stimtimes[i+1]

            mask = (current_ft >= t_start) & (current_ft < t_end)
            frametimes.append(current_ft[mask])
            current_ft = current_ft[~mask]
        else:
            frametimes.append(current_ft)

    if events and 'stimid' in events:
        stimids = events['stimid']
    else:
        stimids = np.full(len(stimtimes), np.nan)

    return stimids, stimtimes, frametimes
