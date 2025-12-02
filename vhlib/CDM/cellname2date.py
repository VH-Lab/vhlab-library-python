from .cellname2nameref import cellname2nameref as c2n

def cellname2date(cellname):
    """
    Converts a VHLAB cellname to a date string

    :param cellname: The cell name string
    :return: Date string (e.g., '2003-05-27')
    """
    _, _, datestr_underscores = c2n(cellname)
    return datestr_underscores.replace('_', '-')
