import os

try:
    from vlt.file.dirstruct import _load_mat_file
except ImportError:  # pragma: no cover - vlt is a hard requirement of this package
    _load_mat_file = None


def getstimscript(dirname):
    """
    Return a stimscript from a directory

    [THESTIMSCRIPT, MTI] = GETSTIMSCRIPT(DIRNAME)

    Looks for the existence of a 'stims.mat' file in the directory DIRNAME.
    If it exists, it loads the STIMSCRIPT (variable 'saveScript') and the
    measured timing information (variable 'MTI2').

    :param dirname: Directory path
    :return: tuple (thestimscript, mti)

    `thestimscript` is returned exactly as the .mat loader produces it. The
    NewStim `stimscript` class has no Python port, so a stims.mat written by
    MATLAB yields a scipy MATLAB-object/struct wrapper rather than a
    stimscript; reading stimulus parameters off it needs a NewStim port.
    `mti` is the 'MTI2' timing record, a struct array in MATLAB. The loader
    squeezes it, so a one-stimulus MTI2 arrives as a single struct rather than
    as a length-1 array.

    See also: read_stimtimes_txt, vhlabcorrectmti
    """
    if not os.path.isdir(dirname):
        raise FileNotFoundError(f"Directory {dirname} does not exist.")

    stims_path = os.path.join(dirname, 'stims.mat')
    if not os.path.isfile(stims_path):
        raise FileNotFoundError(f"No stims in directory {dirname}.")

    if _load_mat_file is None:  # pragma: no cover
        raise ImportError('vlt.file.dirstruct._load_mat_file is needed to read '
                          f'{stims_path}; install vhlab-toolbox-python.')

    g = _load_mat_file(stims_path)

    missing = [name for name in ('saveScript', 'MTI2') if name not in g]
    if missing:
        raise KeyError(f"{stims_path} has no variable(s) {', '.join(missing)}.")

    return g['saveScript'], g['MTI2']
