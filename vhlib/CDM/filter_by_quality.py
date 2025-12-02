from .nameref2cellname import nameref2cellname

def filter_by_quality(ds, cells, cellnames, cellinfo):
    """
    Filter out all but specified cell recordings

    :param ds: vlt.dirstruct object
    :param cells: list of cell objects
    :param cellnames: list of cell name strings
    :param cellinfo: list of cell info dictionaries (from read_unitquality)
    :return: tuple (filtered_cells, filtered_cellnames, indices)
    """

    from vhlib.md import findassociate, disassociate, associate

    I = []

    for i in range(len(cellinfo)):
        cell_name = nameref2cellname(ds, cellinfo[i]['name'], cellinfo[i]['ref'], cellinfo[i]['index'])

        try:
            j = cellnames.index(cell_name)
        except ValueError:
             raise ValueError(f"No cell {cell_name} encountered in input cellnames.")

        I.append(j)

        inds_to_ax = []
        A, _ = findassociate(cells[j], '', '', '')

        if A:
            if not isinstance(A, list): A = [A]
            for idx, a in enumerate(A):
                atype = a.get('type', '')
                if atype.endswith(' test'):
                    data = a.get('data')
                    good_dirs = cellinfo[i].get('goodtestdirs', [])

                    if data not in good_dirs:
                        inds_to_ax.append(idx)

        if inds_to_ax:
             cells[j] = disassociate(cells[j], inds_to_ax)

        cells[j] = associate(cells[j], 'Plexon Quality', '', cellinfo[i].get('quality', ''), 'Quality label as determined by the user of the Offline Spike Sorter by Plexon')

    I = sorted(I)
    cells = [cells[i] for i in I]
    cellnames = [cellnames[i] for i in I]

    return cells, cellnames, I
