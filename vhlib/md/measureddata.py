class MeasuredData:
    """
    Part of the NeuralAnalysis package

    Creates a new MEASUREDDATA object, sampled over the intervals described in
    the Nx2 matrix INTERVALS (i.e., there is assumed to be a clock).
    """

    def __init__(self, intervals, desc_long='', desc_brief=''):
        """
        MD = MEASUREDDATA(INTERVALS, DESC_LONG, DESC_BRIEF)

        :param intervals: Nx2 list or array of intervals
        :param desc_long: Long description string
        :param desc_brief: Brief description string
        """
        if hasattr(intervals, 'shape'):
             if len(intervals.shape) == 2 and intervals.shape[1] == 2:
                 pass
             elif len(intervals) == 0:
                 pass
             else:
                  raise ValueError(f"intervals are not Nx2: {intervals.shape}")
        elif isinstance(intervals, list):
             if len(intervals) > 0:
                 if len(intervals[0]) != 2:
                     raise ValueError("intervals are not Nx2")

        self.intervals = intervals
        self.description_long = desc_long
        self.description_brief = desc_brief
        self.associates = []

    def associate(self, type_or_struct, owner=None, data=None, description=None):
        """
        Associates some data with the MEASUREDDATA object and returns the object (self).
        """
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

        matches, indices = self.findassociate(atype, aowner, adesc)

        if matches:
            for idx in indices:
                self.associates[idx] = new_assoc
        else:
            self.associates.append(new_assoc)

        return self

    def findassociate(self, type_str, owner, description):
        """
        Finds associates matching criteria.
        Returns list of matching associates and their indices.
        """
        if type_str and not isinstance(type_str, str): raise ValueError('type must be string.')
        if owner and not isinstance(owner, str): raise ValueError('owner must be string.')
        if description and not isinstance(description, str): raise ValueError('description must be string.')

        matches = []
        indices = []

        for i, a in enumerate(self.associates):
            match_type = (not type_str) or (type_str == a.get('type'))
            match_desc = (not description) or (description == a.get('desc'))
            match_owner = (not owner) or (owner == a.get('owner'))

            if match_type and match_desc and match_owner:
                matches.append(a)
                indices.append(i)

        return matches, indices

    def numassociates(self):
        return len(self.associates)

    def getassociate(self, indices):
        """
        Returns associates at given indices (scalar or list)
        """
        if isinstance(indices, int):
            return self.associates[indices]
        else:
            return [self.associates[i] for i in indices]

    def disassociate(self, indices):
        """
        Removes associates at given indices.
        """
        if isinstance(indices, int):
            indices = [indices]

        for i in sorted(indices, reverse=True):
            if 0 <= i < len(self.associates):
                del self.associates[i]

        return self

    def associates2struct(self):
        """
        Convert associates to structure (dictionary in Python)
        Field names are associate types (spaces replaced by underscores).
        """
        s = {}
        for a in self.associates:
            key = a['type'].replace(' ', '_')
            s[key] = a['data']
        return s

    def update(self, *args):
         pass
