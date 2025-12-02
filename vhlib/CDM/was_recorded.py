def was_recorded(cell, testdir):
    """
    Looks to see if a cell was recorded in a given directory

    :param cell: A dictionary or object representing a cell, expected to have associates.
                 Should be something that vlt.data.findassociate can query.
    :param testdir: String representing the test directory (e.g., 't00001') or a test type.
    :return: 1 if recorded (or assumed recorded), 0 if not.
    """

    from vhlib.md import findassociate

    b = 1 # assume it is unless we have evidence otherwise
    testdirname = ''

    A, _ = findassociate(cell, 'vhlv_loadcelldata', '', '')

    if not A:
        return b

    # check T
    istestdir = 0
    if len(testdir) == 6:
        if testdir.lower().startswith('t') and testdir[1:].isdigit():
            istestdir = 1

    if istestdir:
        testdirname = testdir
    else:
        asc, _ = findassociate(cell, testdir + ' test', '', '')
        if asc:
            if isinstance(asc, list):
                if len(asc) > 0:
                    testdirname = asc[0].get('data', '')
            else:
                 testdirname = asc.get('data', '')

    if testdirname:
        if isinstance(A, list):
             A_assoc = A[0]
        else:
             A_assoc = A

        data = A_assoc.get('data', [])

        if not isinstance(data, list):
            data = [data]

        a_ind = 0
        for j, item in enumerate(data):
            if isinstance(item, dict) and 'clusterinfo' in item:
                if 'number' in item['clusterinfo']:
                    a_ind = j

        if a_ind < len(data):
            selected_item = data[a_ind]
            if isinstance(selected_item, dict) and 'clusterinfo' in selected_item:
                clusterinfo = selected_item['clusterinfo']
                if 'EpochStart' in clusterinfo:
                    strs = [clusterinfo['EpochStart'], clusterinfo.get('EpochStop', '')]

                    if testdirname not in strs:
                         strs.append(testdirname)
                         sorted_strs = sorted(strs)

                         if sorted_strs[1] != testdirname:
                             b = 0

    return b
