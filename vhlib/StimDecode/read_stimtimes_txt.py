import os
import numpy as np

def read_stimtimes_txt(dirname, filename='stimtimes.txt'):
    """
    Interpret the stimtimes.txt file written by VH lab Spike2

    :param dirname: Directory path
    :param filename: Filename (default 'stimtimes.txt')
    :return: tuple (stimids, stimtimes, frametimes)
    """

    filepath = os.path.join(dirname, filename)

    if not os.path.isfile(filepath):
        raise IOError(f"Could not open file {filename} in directory {dirname}.")

    stimids = []
    stimtimes = []
    frametimes = []

    with open(filepath, 'r') as fid:
        for line in fid:
            line = line.strip()
            if line:
                try:
                    # sscanf(stimline,'%f')
                    # Expecting space separated numbers?
                    stimdata = [float(x) for x in line.split()]
                    if stimdata:
                        stimids.append(stimdata[0])
                        stimtimes.append(stimdata[1])
                        frametimes.append(np.array(stimdata[2:]))
                except Exception:
                    raise IOError(f"error in {filepath}.")

    return np.array(stimids), np.array(stimtimes), frametimes
