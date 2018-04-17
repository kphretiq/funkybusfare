from FunkyBusFare.streamwriter import StreamWriter
from FunkyBusFare.database import initialize, VehiclePositions
import sys
import datetime
from pytz import timezone
eastern = timezone("US/Eastern")

# this should wait. It's going to take some thinking.
class VehiclePositionsETL(StreamWriter):

    def __init__(self, url, database_connection):
        self.url = url
        self.session = initialize(database_connection)
        self.cnt = 0

    def timestamp(self, ts):
        return eastern.localize(datetime.datetime.fromtimestamp(ts))

    def write(self):
        row = self.get()
        try:
            while True:
                vals = next(row)
                self.session.add(VehiclePositions(
                        timestamp = self.timestamp(vals["timestamp"]),
                        vehicle_id = vals["id"],
                        label = vals["label"],
                        trip_id = vals["trip_id"],
                        longitude = vals["longitude"],
                        latitude = vals["latitude"],
                    ))
                self.cnt += 1
                if self.cnt >= 100:
                    self.session.commit()
                    self.cnt = 0
        finally:
            self.session.commit()
