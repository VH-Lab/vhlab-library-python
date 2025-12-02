from .cellname2nameref import cellname2nameref

def filter_by_reference(cells, cellnames, minreference, maxreference):
    """
    Filter out cells by the cluster reference number

    :param cells: list of cell objects
    :param cellnames: list of cell name strings
    :param minreference: minimum reference value (inclusive)
    :param maxreference: maximum reference value (inclusive)
    :return: tuple (filtered_cells, filtered_cellnames, included_indices)
    """

    incl = []

    for i, name in enumerate(cellnames):
        nameref, _, _ = cellname2nameref(name)
        ref = nameref.get('ref')
        if minreference <= ref <= maxreference:
            incl.append(i)

    filtered_cells = [cells[i] for i in incl]
    filtered_cellnames = [cellnames[i] for i in incl]

    return filtered_cells, filtered_cellnames, incl
