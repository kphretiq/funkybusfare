"""
Write lists of json objects to a file without a lot of fuss.
use GZ version for compression
"""

import json
import gzip


class JSONList:
    """
    "Stream" json-serializable objects to a file as a json list-of-objects.
    """

    openbracket = "[\n"
    closebracket = "\n]"

    def __init__(self, path):
        """
        Create a file handle.
        Create a blank "comma" object
        Accepts path(str) output path
        """
        self.filehandle = open(path, "w")
        self.comma = comma()
        self.bytecount = 0

    def __enter__(self):
        """
        Upon entry signal, write our opening bracket and a newline.
        return self
        """
        self.filehandle.write(self.openbracket)
        return self

    def __exit__(self, _type, value, traceback):
        """
        Upon exit singnal, write a newline and our closing bracket, then
        close file handle
        """
        self.filehandle.write(self.closebracket)
        self.filehandle.close()

    def write(self, obj):
        """
        Write a json-serialized object with a comma appearing at the end of any
        preceeding objects.
        Assure comma value is correctly set.
        """
        val = "".join([next(self.comma), json.dumps(obj)])
        self.bytecount += len(val)
        self.filehandle.write(val)


class JSONListGZ(JSONList):
    """
    "Stream" json-serializable objects to a gzipped file as a json
    list-of-objects.
    """

    openbracket = "[\n".encode()
    closebracket = "\n]".encode()

    def __init__(self, path):
        """
        Create a file handle.
        Create a blank "comma" object
        Accepts path(str) output path
        """
        super().__init__(path)
        self.filehandle = gzip.open(path, "w")
        self.comma = comma()
        self.bytecount = 0

    def write(self, obj):
        """
        Write a json-serialized object with a comma appearing at the end of any
        preceeding objects.
        Assure comma value is correctly set.
        """
        val = "".join([next(self.comma), json.dumps(obj)]).encode()
        self.bytecount += len(val)
        self.filehandle.write(val)


def comma():
    """
    Generator that yields a blank first, then a comma with newline thereafter
    for nice formatting.
    Accepts: None
    Yields: ""
    YIelds: "\n,"
    """
    yield ""
    while True:
        yield ",\n"


def test():
    """
    A little test generator for fauxstream.
    Creates a temporary file in /tmp
    Displays contents of temporary file
    Cleans up temporary file
    >>> import tempfile
    >>> import os
    >>> import json
    >>> from FunkyBusFare import flattery
    >>> from FunkyBusFare.fauxstream import JSONList
    >>> from FunkyBusFare.fauxstream import test
    >>> TMP = os.path.join(tempfile.gettempdir(), "fauxstream.json")
    >>> rows = test() # generates deeply nested dictionaries
    >>> with JSONList(TMP) as filehandle: # "with" tests __enter__ and __exit__
    ...     while True:
    ...         try:
    ...             filehandle.write(flattery.flatten(next(rows)))
    ...         except StopIteration:
    ...             break
    >>> # test converts to tuples so order doesn't surprise us
    >>> with open(TMP, "r") as filehandle:
    ...     for d in json.loads(filehandle.read()):
    ...         print([(k, d[k]) for k in sorted(d.keys())])
    [('_id', 0), ('foo', [0, 1]), ('quux', 0)]
    [('_id', 1), ('foo', [1, 2]), ('quux', 1)]
    [('_id', 2), ('foo', [2, 3]), ('quux', 2)]
    >>> # won't totally clean up darwin, since it creates randomized temp dirs.
    >>> os.remove(TMP)
    """
    # generate deeply nested dictionaries for test.
    for i in range(3):
        yield {
            "_id": i,
            "numbers": {"foo": [i, i + 1], "bar": {"bat": {"baz": {"quux": i}}}},
        }


if __name__ == """__main__""":
    import doctest

    doctest.testmod()
