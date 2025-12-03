import os
import numpy as np
from vlt.file.custom_struct_io import loadStructArray

def read_plexon_events_txt(filename):
    """
    Read a text file with exported Plexon event data.

    Reads event data that has been exported from Plexon to a text file. It is assumed
    that the first row is a 'header' row that has tab delimited field names.
    Subsequent rows contain tab-delimited data values for these fields.

    :param filename: The file name to be opened and read (full path).
    :return: dictionary with field names equal to the those in the header row of the
             file. The values for the field names are the data points in those fields.
    """

    # We can use loadStructArray which reads tab delimited file into list of dicts.
    # But read_plexon_events_txt returns a struct of arrays (columns),
    # whereas loadStructArray returns array of structs (rows).
    # So we need to convert.

    try:
        data_list = loadStructArray(filename)
    except Exception as e:
        raise IOError(f"Error reading plexon event file: {e}")

    if not data_list:
        return {}

    keys = data_list[0].keys()
    events = {k: [] for k in keys}

    for item in data_list:
        for k in keys:
            # Convert to float if possible, as in MATLAB sscanf('%f')
            val = item.get(k)
            try:
                val_float = float(val)
                events[k].append(val_float)
            except (ValueError, TypeError):
                # If can't convert, keep as string or handle?
                # MATLAB code uses sscanf(..., '%f'). If it fails or is empty, it appends nothing?
                # But here we are iterating rows.
                # If it's a number, it appends.
                # Assuming all data is numeric based on MATLAB code usage.
                events[k].append(float('nan'))

    # Convert lists to numpy arrays
    for k in events:
        events[k] = np.array(events[k])

    return events
