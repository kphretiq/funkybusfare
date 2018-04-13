import os
import time
import uuid
import requests
from google.protobuf import json_format
from google.transit import gtfs_realtime_pb2
from FunkyBusFare.protobuf_to_dict import protobuf_to_dict
from FunkyBusFare.flattery import flatten
from FunkyBusFare.fauxstream import JSONListGZ

class StreamWriter(object):
    """
    constantly monitor metro api endpoint, writing data as a series of 
    compressed json files
    """

    def __init__(self, url, outpath, bytecount=10000000):
        self.url = url
        self.outpath = outpath
        self.bytecount = bytecount

    def get(self):
        """
        generator reading metro api endpoint
        """
        while True:
            response = requests.get(self.url)
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            for entity in feed.entity:
                foo = protobuf_to_dict(entity)
                yield flatten(foo)
            time.sleep(5)

    def write(self):
        """
        write metro data to json file
        """
        row = self.get()
        while True:
            uniq = str(uuid.uuid4())
            name = os.path.splitext(os.path.split(self.url)[1])[0]
            outfile = "%s-%s.json.gz"%(name, uniq)
            filepath = os.path.join(self.outpath, outfile)
            with JSONListGZ(filepath) as fh:
                while True:
                    fh.write(next(row))
                    if fh.bytecount >= self.bytecount:
                        break
