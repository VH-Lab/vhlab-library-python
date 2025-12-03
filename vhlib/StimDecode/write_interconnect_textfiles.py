import os
import numpy as np
from .write_stimtimes_txt import write_stimtimes_txt

def write_interconnect_textfiles(dirname, out):
    """
    Write interconnect text file info for a given directory

    :param dirname: Directory path
    :param out: Dictionary with fields StimTrigger, FrameTriggerRaw, etc.
    """

    # if ~isfield(out,'FrameTrigger'),
    #   out.FrameTrigger = frametimesraw2frametimes(out.FrameTriggerRaw,out.StimTrigger);
    # end;

    if 'FrameTrigger' not in out:
        # frametimesraw2frametimes is missing function?
        # I should probably implement logic or assume it is available.
        # But MATLAB code calls it. It might be in StimulusDecoding folder?
        # I listed files and didn't see it. Maybe in AnalysisTools/MeasuredData/general?

        # Simple implementation: divide FrameTriggerRaw by StimTrigger intervals
        if 'FrameTriggerRaw' in out and 'StimTrigger' in out:
            ft_raw = np.array(out['FrameTriggerRaw'])
            st = np.array(out['StimTrigger'])
            out['FrameTrigger'] = []

            for i in range(len(st)):
                if i < len(st) - 1:
                    mask = (ft_raw >= st[i]) & (ft_raw < st[i+1])
                    out['FrameTrigger'].append(ft_raw[mask])
                else:
                    # Last stimulus until end?
                    mask = (ft_raw >= st[i])
                    out['FrameTrigger'].append(ft_raw[mask])
        else:
            out['FrameTrigger'] = None

    fnames = ['stimtimes.txt', 'stimontimes.txt', 'verticalblanking.txt', 'twophotontimes.txt', 'Intan_decoding_finished.txt']
    for fname in fnames:
        fpath = os.path.join(dirname, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)

    # write_stimtimes_txt(dirname,out.StimCode,out.StimTrigger,out.FrameTrigger);
    # write_stimtimes_txt(dirname,out.StimCode,out.StimTrigger);

    if 'StimCode' in out and 'StimTrigger' in out:
        write_stimtimes_txt(dirname, out['StimCode'], out['StimTrigger'], out.get('FrameTrigger'), filename='stimtimes.txt')
        write_stimtimes_txt(dirname, out['StimCode'], out['StimTrigger'], filename='stimontimes.txt')

    if 'TwoPhotonFrameTrigger' in out:
        np.savetxt(os.path.join(dirname, 'twophotontimes.txt'), out['TwoPhotonFrameTrigger'], fmt='%.5f', delimiter='\n')

    if 'StimulusMonitorVerticalRefresh' in out:
        np.savetxt(os.path.join(dirname, 'verticalblanking.txt'), out['StimulusMonitorVerticalRefresh'], fmt='%.5f', delimiter='\n')

    # Write empty file
    with open(os.path.join(dirname, 'Intan_decoding_finished.txt'), 'w') as f:
        pass
