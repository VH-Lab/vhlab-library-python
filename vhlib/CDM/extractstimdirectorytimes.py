import os

def extractstimdirectorytimes(ds, cell, **kwargs):
    """
    Loop through all known TEST directories and extract the time of presentation

    :param ds: vlt.file.dirstruct object
    :param cell: cell object
    :param kwargs:
        ErrorIfEmptyTestData (bool, default True)
        WarnOnEarlyMorning (bool, default True)
        EarlyMorningCutOffTime (float, default 5)
        ErrorIfEmpty (bool, default True)
    :return: tuple (cell, assoc_list)
    """

    error_if_empty_test_data = kwargs.get('ErrorIfEmptyTestData', True)

    from vhlib.md import findassociate, associate

    def getstimdirectorytime(*args, **kwargs):
         raise NotImplementedError("getstimdirectorytime is missing")

    assoc_new = []

    A, _ = findassociate(cell, '', '', '')

    try:
        pn = ds.getpathname()
    except AttributeError:
        if isinstance(ds, str):
            pn = ds
        else:
             raise ValueError("ds must have getpathname method or be a string path")

    if A:
        if not isinstance(A, list): A = [A]
        for item in A:
            atype = item.get('type', '')
            if atype.upper().endswith(' TEST'):
                idx = atype.upper().rfind(' TEST')
                if idx != -1:
                    newtype = atype[:idx] + ' time'

                    data = item.get('data')
                    if not data:
                        if error_if_empty_test_data:
                            raise ValueError(f"Test directory associate label '{atype}' is present but is empty.")
                        else:
                            print(f"Warning: Test directory label {atype} is present but empty and will be ignored.")
                    else:
                        time_val = getstimdirectorytime(os.path.join(pn, data), **kwargs)

                        a_struct = {
                            'type': newtype,
                            'owner': 'extractstimdirectorytimes',
                            'data': time_val,
                            'desc': 'Time of day of the recording'
                        }
                        assoc_new.append(a_struct)
                        cell = associate(cell, a_struct)

    return cell, assoc_new
