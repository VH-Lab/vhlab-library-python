import os
from .cellname2nameref import cellname2nameref

def add_testdir_info(ds, cells=None, cellnames=None):
    """
    Add test directory info as associates to cells

    :param ds: vlt.file.dirstruct object
    :param cells: list of cell objects
    :param cellnames: list of cell names (optional, but needed for filtering by recording)
    :return: tuple (assoc, cells)
    """

    from vhlib.md import associate_all, associate
    try:
        from vlt.file.custom_struct_io import loadStructArray
    except ImportError:
         raise NotImplementedError("vlt.file.custom_struct_io.loadStructArray missing")

    try:
        pathname = ds.getpathname()
    except AttributeError:
         if isinstance(ds, str):
            pathname = ds
         else:
            raise ValueError("ds must have getpathname method or be a string path")

    testdirinfo_file = os.path.join(pathname, 'testdirinfo.txt')
    testdirinfo = loadStructArray(testdirinfo_file)

    assoc = []

    for info in testdirinfo:
        types_str = info.get('types', '')
        types = [x.strip() for x in types_str.split(',') if x.strip()]

        td = info.get('testdir', '')

        for t in types:
            a = {
                'type': f"{t} test",
                'owner': 'add_testdir_info',
                'data': td,
                'desc': 'Test directory info'
            }
            assoc.append(a)

    if cells is not None:
        if cellnames is None:
             cells = associate_all(cells, assoc)
        else:
             for i in range(len(cells)):
                nameref, _, _ = cellname2nameref(cellnames[i])

                if hasattr(ds, 'gettests'):
                    t = ds.gettests(nameref['name'], nameref['ref'])
                else:
                    raise NotImplementedError("ds.gettests method is missing")

                for a in assoc:
                    if a['data'] in t:
                        cells[i] = associate(cells[i], a)

    return assoc, cells
