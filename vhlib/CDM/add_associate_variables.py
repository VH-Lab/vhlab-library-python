import os

def add_associate_variables(ds, cells=None):
    """
    Add associates from the file 'associate_variables.txt' to all cells in an experiment

    :param ds: vlt.file.dirstruct object
    :param cells: list of cell objects (optional). If provided, modifications are returned.
                  If not provided, it would load cells, modify and save back.
    :return: list of modified cells
    """

    from vhlib.md import associate_all, findassociate, disassociate
    try:
        from vlt.file.custom_struct_io import loadStructArray
    except ImportError:
         raise NotImplementedError("vlt.file.custom_struct_io.loadStructArray missing")

    try:
        from vlt.data import load2celllist
    except ImportError:
         def load2celllist(*args): raise NotImplementedError("vlt.data.load2celllist missing")

    try:
        pathname = ds.getpathname()
    except AttributeError:
        if isinstance(ds, str):
            pathname = ds
        else:
             raise ValueError("ds must have getpathname method or be a string path")

    filename = os.path.join(pathname, 'associate_variables.txt')

    if not os.path.isfile(filename):
         raise FileNotFoundError(f"Could not find the file 'associate_variables.txt' in the directory {pathname}.")

    assoclist = loadStructArray(filename)

    saving_needed = False
    cellnames = []

    if cells is None:
        if hasattr(ds, 'getexperimentfile'):
            exp_file, _ = ds.getexperimentfile()
        else:
             raise NotImplementedError("ds.getexperimentfile method missing")

        cells, cellnames = load2celllist(exp_file, 'cell*', '-mat')
        saving_needed = True

    for i in range(len(cells)):
        for assoc_item in assoclist:
             atype = assoc_item.get('type')
             a, inds = findassociate(cells[i], atype, '', '')
             if a:
                 cells[i] = disassociate(cells[i], inds)

    cells = associate_all(cells, assoclist)

    if saving_needed:
        print("writing variables back to disk")
        if hasattr(ds, 'saveexpvar'):
            ds.saveexpvar(cells, cellnames, 0)
        else:
            raise NotImplementedError("ds.saveexpvar method missing")
        return cells

    return cells
