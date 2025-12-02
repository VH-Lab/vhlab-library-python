import os

def remove_associate(ds, type_):
    """
    Remove an associate from all experiment variables in a dirstruct

    :param ds: vlt.file.dirstruct object
    :param type_: string or list of strings of associate types to remove
    """

    from vhlib.md import findassociate, disassociate
    try:
        from vlt.file.load2celllist import load2celllist
    except ImportError:
         raise NotImplementedError("vlt.file.load2celllist missing")

    if isinstance(type_, str):
        types = [type_]
    else:
        types = type_

    if hasattr(ds, 'getexperimentfile'):
        exp_file, _ = ds.getexperimentfile()
    else:
         raise NotImplementedError("ds.getexperimentfile method missing")

    vars_list, varnames = load2celllist(exp_file, '*', '-mat')

    changes_made = False

    for i in range(len(vars_list)):
        var = vars_list[i]

        for t in types:
            a, ii = findassociate(var, t, '', '')
            if a:
                vars_list[i] = disassociate(var, ii)
                changes_made = True

    if changes_made:
        if hasattr(ds, 'saveexpvar'):
            ds.saveexpvar(vars_list, varnames)
        else:
             raise NotImplementedError("ds.saveexpvar method missing")
