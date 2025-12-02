def cellname2nameref(cellname):
    """
    Converts a VHLab cellname to a CKSDIRSTRUCT name/ref

    :param cellname: The cell name string
    :return: A tuple (nameref, index, datestr) where nameref is a dictionary {'name': name, 'ref': ref}
    """

    parts = cellname.split('_')
    # cellname example: cell_ctx_0003_001_2003_05_27
    # parts: ['cell', 'ctx', '0003', '001', '2003', '05', '27']

    if len(parts) < 7:
         raise ValueError(f"Invalid cellname format: {cellname}")

    nameref = {
        'name': parts[1],
        'ref': int(parts[2])
    }

    index = int(parts[3])

    datestr = f"{parts[4]}_{parts[5]}_{parts[6]}"

    return nameref, index, datestr

def cellname2date(cellname):
    """
    Converts a VHLAB cellname to a date string

    :param cellname: The cell name string
    :return: Date string (e.g., '2003-05-27')
    """
    # In MATLAB: [dummy,dummy,datestr] = cellname2nameref(cellname);
    # datestr was returned as '2003_05_27' from cellname2nameref in my python impl above.
    # But the MATLAB example says '2003-05-27'.
    # Let's check the MATLAB code again.
    # datestr = cellname(m(end-2)+1:end);
    # cellname: cell_ctx_0003_001_2003_05_27
    # m would find all underscores.
    # m(end-2) corresponds to the underscore before the year.
    # So datestr in MATLAB returns '2003_05_27'.
    # However, the example says '2003-05-27'.
    # If I look at nameref2cellname, it constructs it with underscores.
    # Let's stick to returning what corresponds to the string in the cellname.
    # If the example says dashes, maybe the example is illustrative or I should convert.
    # But `cellname2nameref` returns `datestr` as the tail of the string.
    # I will return with underscores for consistency with the code logic, or replace if needed.

    _, _, datestr_underscores = cellname2nameref(cellname)
    return datestr_underscores.replace('_', '-')
