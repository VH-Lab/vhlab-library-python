import os

def nameref2cellname(ds, name, ref, index):
    """
    Produces string of cell name given name/ref

    :param ds: vlt.file.dirstruct object or similar that has getpathname() method
    :param name: reference name string
    :param ref: reference number
    :param index: cell index
    :return: cell name string
    """

    try:
        pathname = ds.getpathname()
    except AttributeError:
        if isinstance(ds, str):
            pathname = ds
        else:
             raise ValueError("ds must have getpathname method or be a string path")

    dirname, datestr = os.path.split(pathname)

    if not datestr: # Trailing slash might result in empty tail
         dirname, datestr = os.path.split(dirname)

    parts = datestr.split('-')
    if len(parts) != 3:
         raise ValueError("Can't extract date string for naming cell...too many/few dashes.")

    datestr_formatted = f"{parts[0]}_{parts[1]}_{parts[2]}"

    cellname = f"cell_{name}_{int(ref):03d}_{int(index):03d}_{datestr_formatted}"

    return cellname
