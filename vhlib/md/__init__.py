from .measureddata import MeasuredData
from .general import spiketriggeredaverage

def findassociate(md, type_str, owner, description):
    """
    Finds associates of MEASUREDDATA object MD.
    Wrapper for md.findassociate(type, owner, description).
    """
    if hasattr(md, 'findassociate'):
        return md.findassociate(type_str, owner, description)
    else:
        raise ValueError("Object does not have findassociate method")

def associate(md, type_or_struct, owner=None, data=None, description=None):
    """
    Associates data with MEASUREDDATA object.
    Wrapper for md.associate(...).
    """
    if hasattr(md, 'associate'):
        return md.associate(type_or_struct, owner, data, description)
    else:
        raise ValueError("Object does not have associate method")

def disassociate(md, indices):
    """
    Removes associates from MEASUREDDATA object.
    Wrapper for md.disassociate(indices).
    """
    if hasattr(md, 'disassociate'):
        return md.disassociate(indices)
    else:
        raise ValueError("Object does not have disassociate method")

def associate_all(cells, assoclist):
    """
    Associates a list of associates to a list of cells.
    """
    if not isinstance(cells, list):
        cells_list = [cells]
    else:
        cells_list = cells

    for i in range(len(cells_list)):
        for assoc_item in assoclist:
             cells_list[i] = associate(cells_list[i], assoc_item)

    if not isinstance(cells, list):
        return cells_list[0]
    return cells_list
