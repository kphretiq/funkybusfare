"""
Write metro api data to compressed json files.
"""
import os
import uuid
from FunkyBusFare.fauxstream import JSONListGZ
from FunkyBusFare import get_positions

class StreamWriter:
    """
    constantly monitor metro api endpoint, writing data as a series of
    compressed json files
    """

    def __init__(self, url, outpath, bytecount=10000000):
        self.url = url
        self.outpath = outpath
        self.bytecount = bytecount

    def write(self):
        """
        write metro data to json file
        """

        row = get_positions(self.url)

        while True:
            uniq = str(uuid.uuid4())
            name = os.path.splitext(os.path.split(self.url)[1])[0]
            outfile = "%s-%s.json.gz"%(name, uniq)
            filepath = os.path.join(self.outpath, outfile)
            with JSONListGZ(filepath) as _fh:
                while True:
                    _fh.write(next(row))
                    if _fh.bytecount >= self.bytecount:
                        break
