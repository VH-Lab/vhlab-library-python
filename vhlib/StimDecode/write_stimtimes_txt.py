import os
import numpy as np

def write_stimtimes_txt(dirname, stimids, stimtimes, frametimes=None, filename=None):
    """
    Writes the stimtimes.txt file

    :param dirname: Directory path
    :param stimids: list of stim ids
    :param stimtimes: list of stim times
    :param frametimes: list of frame times (list of arrays/lists)
    :param filename: optional filename
    """

    if filename is None:
        if frametimes is None:
            filename = 'stimontimes.txt'
        else:
            filename = 'stimtimes.txt'

    filepath = os.path.join(dirname, filename)

    if os.path.isfile(filepath):
        raise IOError(f"Could not write {filename}; file already exists in {dirname}.")

    with open(filepath, 'w') as fid:
        for i in range(len(stimids)):
            # fprintf(fid,'%d ', stimids(i));
            # fprintf(fid,'%.5f', stimtimes(i));
            fid.write(f"{int(stimids[i])} {stimtimes[i]:.5f}")

            if frametimes is not None:
                # for j=1:length(frametimes{i}),
                #   fprintf(fid,' %.5f', frametimes{i}(j));
                # end;
                fts = frametimes[i]
                if isinstance(fts, (list, np.ndarray)):
                    for ft in fts:
                        fid.write(f" {ft:.5f}")

            # fprintf(fid,'\r\n');
            fid.write("\n")

        fid.write("\n") # Blank line at end
