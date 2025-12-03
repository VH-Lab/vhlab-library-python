from .measureddata import MeasuredData
from .general import spiketriggeredaverage

def findassociate(md, type_str, owner, description):
    """
    Finds associates of MEASUREDDATA object MD or dictionary (struct).
    Wrapper for md.findassociate(type, owner, description) or dict processing.
    """
    if hasattr(md, 'findassociate'):
        return md.findassociate(type_str, owner, description)
    elif isinstance(md, dict):
        # Handle dictionary input
        associates = md.get('associates', [])
        if not isinstance(associates, list):
            # Maybe it is a numpy array or single item?
            # In MATLAB struct arrays are often loaded as object arrays or dicts.
            # If loadStructArray returns list of dicts, fine.
            # But load2celllist loads MAT files which might have 'associates' as struct array.
            # We assume it is iterable.
            try:
                iter(associates)
                if isinstance(associates, dict): # Dict is iterable but we want list of associates
                    associates = [associates]
            except TypeError:
                associates = [associates] if associates is not None else []

        matches = []
        indices = []

        for i, a in enumerate(associates):
            # a should be a dict or object
            if isinstance(a, dict):
                match_type = (not type_str) or (type_str == a.get('type'))
                match_desc = (not description) or (description == a.get('desc'))
                match_owner = (not owner) or (owner == a.get('owner'))

                if match_type and match_desc and match_owner:
                    matches.append(a)
                    indices.append(i)

        return matches, indices
    else:
        raise ValueError("Object does not have findassociate method and is not a dict")

def associate(md, type_or_struct, owner=None, data=None, description=None):
    """
    Associates data with MEASUREDDATA object or dictionary.
    Wrapper for md.associate(...) or dict processing.
    """
    if hasattr(md, 'associate'):
        return md.associate(type_or_struct, owner, data, description)
    elif isinstance(md, dict):
        if isinstance(type_or_struct, dict):
            assoc = type_or_struct
            atype = assoc.get('type')
            aowner = assoc.get('owner')
            adata = assoc.get('data')
            adesc = assoc.get('desc')
        else:
            atype = type_or_struct
            aowner = owner
            adata = data
            adesc = description

        if not isinstance(atype, str): raise ValueError('type must be string.')
        if not isinstance(aowner, str): raise ValueError('owner must be string.')
        if not isinstance(adesc, str): raise ValueError('description must be string.')

        new_assoc = {
            'type': atype,
            'owner': aowner,
            'data': adata,
            'desc': adesc
        }

        # Check existing
        matches, indices = findassociate(md, atype, aowner, adesc)

        associates = md.get('associates', [])
        if not isinstance(associates, list):
             # Try to make it a list if possible, or create new list
             if associates is None:
                 associates = []
             elif hasattr(associates, 'tolist'): # numpy array
                 associates = associates.tolist()
             else:
                 associates = [associates] # Single item?

        if matches:
            for idx in indices:
                associates[idx] = new_assoc
        else:
            associates.append(new_assoc)

        md['associates'] = associates
        return md
    else:
        raise ValueError("Object does not have associate method and is not a dict")

def disassociate(md, indices):
    """
    Removes associates from MEASUREDDATA object or dictionary.
    Wrapper for md.disassociate(indices) or dict processing.
    """
    if hasattr(md, 'disassociate'):
        return md.disassociate(indices)
    elif isinstance(md, dict):
        associates = md.get('associates', [])
        if isinstance(indices, int):
            indices = [indices]

        # Ensure associates is list
        if not isinstance(associates, list):
             if associates is None: return md
             if hasattr(associates, 'tolist'): associates = associates.tolist()
             else: associates = [associates]

        for i in sorted(indices, reverse=True):
            if 0 <= i < len(associates):
                del associates[i]

        md['associates'] = associates
        return md
    else:
        raise ValueError("Object does not have disassociate method and is not a dict")

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
