#!/usr/bin/env python
"""
Read a huge csv file in chunks.
"""
from subprocess import Popen, PIPE


class MultiRead:
    """
    Read a huge csv file in chunks. Provides generator "chunks", which is
    for consumption by multiprocessing.Pool

    >>> import os
    >>> import csv
    >>> import tempfile
    >>> from FunkyBusFare.multiread import MultiRead
    >>> fieldnames = ["foo", "bar"]
    >>> vals = [{"foo": i, "bar": i} for i in range(100)]
    >>> tmp_path = os.path.join(tempfile.gettempdir(), "test.csv")
    >>> with open(tmp_path, "w") as fh:
    ...     writer = csv.DictWriter(fh, fieldnames=fieldnames)
    ...     writer.writeheader()
    ...     writer.writerows(vals)
    >>> mr = MultiRead(tmp_path, limit=10)
    >>> # number of rows in csv file
    >>> print(mr.size)
    101
    >>> # header extracted from file
    >>> print(mr.header)
    ['foo', 'bar']
    >>> os.remove(tmp_path)
    >>> vals = next(mr.chunks)
    >>> for k in sorted(vals.keys()):
    ...     print(k, vals[k])
    end 10
    header ['foo', 'bar']
    path /tmp/test.csv
    start 1
    step 0
    """

    def __init__(self, path, limit=1000000, size=None, header=None):
        self.path = path
        self.limit = limit
        self._size = size
        self._header = header
        self.chunks = self._chunks()

    @property
    def header(self):
        """
        CSV file fieldnames.
        """
        if not self._header:
            with open(self.path, "r") as _fh:
                self._header = [i.strip() for i in _fh.readline().split(",")]
        return self._header

    @property
    def size(self):
        """
        use wc to get a row count of the csv we are dealing with
        """
        if not self._size:
            cmd = ["/usr/bin/wc", "-l", self.path]
            out, err = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
            out, err = out.strip().split()[0], err.strip()
            if err:
                raise Exception(err)
            self._size = int(out)
        return self._size

    def _chunks(self):
        """
        Generator yielding step, path, start, end and header values for
        consumption by multiprocessing.Pool
        """
        start = 1  # start on 1, since expect first row to be header
        end = self.limit
        steps = int((self.size / self.limit + 1) + 1)

        # create list of chunks to work on in parallel
        yield {
            "step": 0,
            "path": self.path,
            "start": start,
            "end": end,
            "header": self.header,
        }

        for step in range(1, int(steps)):
            start, end = start + self.limit, end + self.limit
            if start > self.size:
                break

            yield {
                "step": step,
                "path": self.path,
                "start": start,
                "end": end,
                "header": self.header,
            }


if __name__ == "__main__":
    import doctest

    doctest.testmod()
