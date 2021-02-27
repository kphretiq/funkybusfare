"""
Pull data from metro api endpoint.
"""

import os
import time
import datetime
import uuid
import requests
from pytz import timezone
from google.protobuf import json_format
from google.transit import gtfs_realtime_pb2
from FunkyBusFare.protobuf_to_dict import protobuf_to_dict
from FunkyBusFare.flattery import flatten
from FunkyBusFare.fauxstream import JSONListGZ

EASTERN = timezone("US/Eastern")

def get_positions(url, sleep=5):
    """
    Generator reading metro api endpoint
    """
    while True:
        response = requests.get(url)
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        for entity in feed.entity: # pylint: disable=no-member
            entity_dict = protobuf_to_dict(entity)
            yield flatten(entity_dict)
        time.sleep(sleep)


def timestamp(stamp):
    """
    Localize timestamp to EST. Obviously brittle.
    """
    return EASTERN.localize(datetime.datetime.fromtimestamp(stamp))
