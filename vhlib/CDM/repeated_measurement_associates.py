def repeated_measurement_associates(cell, associatename, nmax):
    """
    Find all instances of a repeated measurement associate

    :param cell: cell object
    :param associatename: string with '%d' placeholder (e.g., 'SP F0 TFOP%d TF Response curve')
    :param nmax: max number to check
    :return: list of matching numbers
    """

    from vhlib.md import findassociate

    n = []

    for i in range(nmax + 1):
        name = associatename % i
        matches, _ = findassociate(cell, name, '', '')
        if matches:
            n.append(i)

    return n
