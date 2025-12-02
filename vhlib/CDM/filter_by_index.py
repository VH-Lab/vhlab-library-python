from .cellname2nameref import cellname2nameref

def filter_by_index(cells, cellnames, minindex, maxindex):
    """
    Filter out cells by the cluster index number

    :param cells: list of cell objects
    :param cellnames: list of cell name strings
    :param minindex: minimum index value (inclusive)
    :param maxindex: maximum index value (inclusive)
    :return: tuple (filtered_cells, filtered_cellnames, included_indices)
    """

    incl = []

    for i, name in enumerate(cellnames):
        _, index, _ = cellname2nameref(name)
        if minindex <= index <= maxindex:
            incl.append(i)

    filtered_cells = [cells[i] for i in incl]
    filtered_cellnames = [cellnames[i] for i in incl]

    return filtered_cells, filtered_cellnames, incl
