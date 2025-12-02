import os

def read_unitquality(ds):
    """
    Read the unitquality.txt file and prepare a list of cells to include

    :param ds: vlt.file.dirstruct object
    :return: list of cell info dictionaries
    """

    try:
        from vlt.file.custom_struct_io import loadStructArray
    except ImportError:
         raise NotImplementedError("vlt.file.custom_struct_io.loadStructArray missing")

    unit_shift = 400

    try:
        pathn = ds.getpathname()
    except AttributeError:
        if isinstance(ds, str):
            pathn = ds
        else:
             raise ValueError("ds must have getpathname method or be a string path")

    uq_file = os.path.join(pathn, 'unitquality.txt')
    if not os.path.exists(uq_file):
        raise FileNotFoundError(f"File not found: {uq_file}")

    uq = loadStructArray(uq_file)

    channelshift = 0
    channelshift_file = os.path.join(pathn, 'unitquality_channelshift.txt')
    if os.path.isfile(channelshift_file):
        with open(channelshift_file, 'r') as f:
            try:
                content = f.read().split()
                if content:
                    channelshift = float(content[0])
            except ValueError:
                pass

    uq2 = []

    for item in uq:
        base_uq = item.copy()

        qc = item.get('qualitycode', '').lower()
        if qc in ['multiunit', 'mu']:
            base_uq['qualitycode'] = 'Multi-unit'
        elif qc in ['excellent', 'e']:
             base_uq['qualitycode'] = 'Excellent'
        elif qc in ['good', 'g']:
             base_uq['qualitycode'] = 'Good'
        elif qc in ['nu', 'notuseable']:
             base_uq['qualitycode'] = 'Not useable'

        gtd = item.get('goodtestdirs', '')
        base_uq['goodtestdirs'] = [x.strip() for x in gtd.split(',') if x.strip()]

        unit_str = item.get('unit', '')
        unit_list_str = [x.strip() for x in unit_str.split(',') if x.strip()]

        for u_str in unit_list_str:
            if len(u_str) == 1 and u_str.isalpha():
                if 'a' <= u_str <= 'z':
                    unit = unit_shift + 1 + ord(u_str) - ord('a')
                elif 'A' <= u_str <= 'Z':
                    unit = unit_shift + 1 + ord(u_str) - ord('A')
                else:
                    unit = int(u_str)
            else:
                try:
                    unit = int(u_str)
                except ValueError:
                    unit = 0

            entry = base_uq.copy()
            entry['unit'] = unit
            uq2.append(entry)

    cellinfo = []

    for item in uq2:
        celli = {}
        celli['name'] = 'extra'
        try:
            ch = float(item['channel'])
        except ValueError:
            ch = 0

        celli['ref'] = ch + channelshift
        celli['index'] = item['unit']
        celli['goodtestdirs'] = item['goodtestdirs']
        celli['quality'] = item['qualitycode']
        celli['comment'] = item.get('comment', '')

        cellinfo.append(celli)

    return cellinfo
