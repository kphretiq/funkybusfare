import collections
"""
Flattens nested dictionaries.
"""

def flatten(obj):
    """
    Flatten a dictionary 
    Accepts: dictionary
    Returns: dictionary
    >>> mydict = {"foo": {"bar": "bat", "baz": "quux"}, "quuz": [1, 2],}
    >>> flatdict = flatten(mydict)
    >>> keys = sorted(flatdict.keys())
    >>> for k in keys:
    ...     print(k, flatdict[k])
    bar bat
    baz quux
    quuz [1, 2]
    """

    if not isinstance(obj, dict):
        raise TypeError("Object must be a dictionary.")

    return dict(flatter(obj))

def flatter(obj):
    """
    recursively flatten a nested dictionary into a list of tuples
    Accepts: dictionary
    Returns: list of tuples
    >>> mydict = {"foo": {"bar": "bat", "baz": "quux"}, "quuz": [1, 2],}
    >>> sorted(flatter(mydict))
    [('bar', 'bat'), ('baz', 'quux'), ('quuz', [1, 2])]
    """

    # if someone decides they want a list of tuples ...
    if not isinstance(obj, dict):
        raise TypeError("Object must be a dictionary.")

    row = []
    for k, v in obj.items():
        if isinstance(v, collections.MutableMapping):
            row.extend(flatter(v))
        else:
            row.append((k, v))
    return row

if __name__ == "__main__":
    import doctest
    doctest.testmod()