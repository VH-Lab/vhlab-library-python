import numpy as np

def vhinterconnect_decode(time, input_sig, polarity=None):
    """
    Decode the 16 bit vhlab stimulus interconnect signals

    :param time: array of times (seconds)
    :param input_sig: array of UINT16 inputs
    :param polarity: optional polarity array (9 elements)
    :return: dictionary with fields StimTrigger, FrameTriggerRaw, etc.
    """

    # default_polarity = [ -1 1 -1 1 1 1 1 1 1];
    default_polarity = np.array([-1, 1, -1, 1, 1, 1, 1, 1, 1])

    if polarity is not None:
        if len(polarity) != 9:
            raise ValueError("polarity must have 9 elements")

        # goodinds = find(isnan(polarity));
        # default_polarity(goodinds) = polarity(goodinds);
        # In Python: where polarity is not nan, replace default.
        mask = ~np.isnan(polarity)
        default_polarity[mask] = polarity[mask]

    polarity = default_polarity

    th = [
        {'name': 'StimTrigger', 'bit': 1, 'samples': 0, 'polarity': polarity[0]},
        {'name': 'StimTriggerSamples', 'bit': 1, 'samples': 1, 'polarity': polarity[0]},
        {'name': 'StimTriggerOff', 'bit': 1, 'samples': 0, 'polarity': polarity[1]}, # Note: polarity(2) used for StimTriggerOff?
        {'name': 'FrameTriggerRaw', 'bit': 2, 'samples': 0, 'polarity': polarity[2]},
        {'name': 'StimulusMonitorVerticalRefresh', 'bit': 3, 'samples': 0, 'polarity': polarity[3]},
        {'name': 'TwoPhotonFrameTrigger', 'bit': 5, 'samples': 0, 'polarity': polarity[4]},
        # What about bits 4?
        # MATLAB code:
        # th(4) = struct(..., 'bit',2, ... polarity(3)) -> index 2 in 0-based is 3rd element.
        # th(5) = struct(..., 'bit',3, ... polarity(4))
        # th(6) = struct(..., 'bit',5, ... polarity(5))
    ]

    # Wait, the MATLAB code indexing for polarity:
    # th(1): polarity(1) -> 1st element
    # th(2): polarity(1) -> 1st element
    # th(3): polarity(2) -> 2nd element
    # th(4): polarity(3) -> 3rd element
    # th(5): polarity(4) -> 4th element
    # th(6): polarity(5) -> 5th element

    # Python 0-based indexing:
    # polarity[0]
    # polarity[0]
    # polarity[1]
    # polarity[2]
    # polarity[3]
    # polarity[4]

    out = {}

    input_sig = np.array(input_sig, dtype=np.uint16)
    time = np.array(time)

    for item in th:
        # bitget(input, th(i).bit)
        # bit is 1-based in MATLAB. 1 means bit 0 in Python.
        bit_idx = item['bit'] - 1
        bitinfo = (input_sig >> bit_idx) & 1

        if item['polarity'] < 0:
            bitinfo = 1 - bitinfo

        # samples = threshold_crossings(bitinfo,1);
        # threshold_crossings of 1 means transition from 0 to 1?
        # Assuming vlt or vhlib has threshold_crossings.
        # It's a toolbox function?
        # I should assume it exists or implement simple one.
        # Ideally import from vlt.signal?

        # Let's check if threshold_crossings is in vlt.
        # If not, I'll implement locally.
        # Simple diff > 0.5

        diff_sig = np.diff(bitinfo.astype(float))
        samples = np.where(diff_sig > 0.5)[0] + 1 # +1 because diff reduces length and we want the index after crossing?
        # MATLAB threshold_crossings: "returns the indicies of the first sample after a threshold crossing"

        if item['samples'] == 0:
            out[item['name']] = time[samples]
        else:
            out[item['name']] = samples

    # out.StimCode = bitshift(bitand(input(out.StimTriggerSamples), intmax('uint16') - 255),-8);
    # intmax('uint16') is 65535. 65535 - 255 = 65280 (0xFF00)
    # So it masks upper 8 bits.

    if 'StimTriggerSamples' in out:
        samples = out['StimTriggerSamples']
        if len(samples) > 0:
            vals = input_sig[samples]
            out['StimCode'] = (vals & 0xFF00) >> 8
        else:
            out['StimCode'] = np.array([])

    return out
