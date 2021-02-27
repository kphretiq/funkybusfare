"""
Write locations to mongodb
"""
import datetime
from pymongo import InsertOne
from FunkyBusFare import get_positions, timestamp

class VehiclePositionsMongo:
    """
    Write rows to mongodb.
    """
    def __init__(self, url, collection, sleep=5):
        self.url = url
        self.collection = collection
        self.sleep = sleep

    def write(self):
        """
        Write rows to database.
        """
        rows = get_positions(self.url, sleep=self.sleep)
        data = []
        try:
            while True:
                for _ in range(100):
                    row = next(rows)
                    row["timestamp"] = timestamp(row["timestamp"])
                    data.append(InsertOne(row))
                self.collection.bulk_write(data)
                data = []
        finally:
                # clean up any stragglers
                self.collection.bulk_write(data)

