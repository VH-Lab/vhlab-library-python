import os
import numpy as np
try:
    from vlt.file.dirstruct import _load_mat_file
except ImportError:
    def _load_mat_file(filepath): raise NotImplementedError("vlt.file.dirstruct._load_mat_file missing")

from .read_stimtimes_txt import read_stimtimes_txt
from .write_stimtimes_txt import write_stimtimes_txt # To be implemented

def repairoverflow_stimtimes_txt(dirname, skiplineafteroverflow=0, stimtimes_file='stimtimes.txt', stims_mat_file='stims.mat', goodframes=10):
    """
    Repair stimtimes.txt file where numstims > 255

    :param dirname: Directory path
    :param skiplineafteroverflow: 1 if an extra line needs to be removed after overflow error
    :param stimtimes_file: Filename for stimtimes (default 'stimtimes.txt')
    :param stims_mat_file: Filename for stims.mat (default 'stims.mat')
    :param goodframes: Number of frames in a proper stimulus (default 10)
    """

    fout = 'stimtimes_repaired.txt'

    fin_path = os.path.join(dirname, stimtimes_file)
    stims_mat_path = os.path.join(dirname, stims_mat_file)

    # Load stims.mat
    try:
        stims_data = _load_mat_file(stims_mat_path)
    except Exception as e:
        raise IOError(f"Could not load {stims_mat_path}: {e}")

    # [stimids,stimtimes,frametimes] = read_stimtimes_txt(dirname,stimtimes_file);
    stimids, stimtimes, frametimes = read_stimtimes_txt(dirname, stimtimes_file)

    stimtimes_entry = 0 # 0-based index
    i = 0 # 0-based

    stimids_new = []
    stimtimes_new = []
    frametimes_new = []

    # do = getDisplayOrder(saveScript);
    # Asssuming saveScript is in stims_data
    if 'saveScript' in stims_data:
        saveScript = stims_data['saveScript']
        # getDisplayOrder likely a method of saveScript object or function?
        # In MATLAB saveScript is an object (stimscript).
        # We need to simulate getDisplayOrder.
        # If saveScript is loaded as dict/struct, maybe we can find display order.
        # Or if it's missing, we can't proceed.

        # Check if vhlab-library-python or toolbox has stimscript implementation?
        # Assuming getDisplayOrder is not available, we might need to assume stims_data has it pre-calculated or fail.
        # But MATLAB code calls a method/function.

        # Let's assume we can get it from saveScript if it's a dict.
        # If not, raise Error.

        # Mocking getDisplayOrder for now or check if it's a list in saveScript
        # In Python port of objects, maybe we have it.
        # But we are porting StimulusDecoding.

        # Let's assume 'getDisplayOrder' function is available or we can extract it.
        # For now, I'll raise NotImplementedError if I can't find it.
        pass
    else:
        raise ValueError("saveScript not found in stims.mat")

    # Trying to find getDisplayOrder
    # It might be in vhlib.stimulus or something?
    # I'll define a dummy one if not found or try to find it in the data structure.

    # Assuming `do` is a list of stimulus IDs.
    # If saveScript is a dict, maybe it has a field 'displayOrder'?
    if hasattr(saveScript, 'getDisplayOrder'):
        do = saveScript.getDisplayOrder()
    elif isinstance(saveScript, dict) and 'displayOrder' in saveScript:
        do = saveScript['displayOrder']
    else:
        # Fallback?
        raise NotImplementedError("getDisplayOrder functionality missing")

    print(f"Total stims to display: {len(do)}.")

    while i < len(do):
        print(f"displayorder: {i+1} stimtimes line#: {stimtimes_entry+1} "
              f"stimshouldbe: {do[i]} stimis: {stimids[stimtimes_entry]} "
              f"stimtime: {stimtimes[stimtimes_entry]}")

        recordthisentry = 1
        if len(frametimes[stimtimes_entry]) < goodframes:
            print('hmmm, a mismatch we did not expect')
            recordthisentry = 0

        if recordthisentry:
            stimids_new.append(do[i])
            stimtimes_new.append(stimtimes[stimtimes_entry])
            frametimes_new.append(frametimes[stimtimes_entry][:goodframes])

        stimtimes_entry += 1

        if skiplineafteroverflow and recordthisentry and (do[i] >= 255):
            stimtimes_entry += 1

        if recordthisentry:
            i += 1

    write_stimtimes_txt(dirname, stimids_new, stimtimes_new, frametimes_new, fout)
