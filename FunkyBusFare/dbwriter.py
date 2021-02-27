"""
Experimental, and obviously flawed database writer.
"""
import datetime
from pytz import timezone
from FunkyBusFare.models import initialize, VehiclePositions
from FunkyBusFare import get_positions

EASTERN = timezone("US/Eastern")

class VehiclePositionsETL:
    """
    Write row to sql database. Obvious drawback: if company upgrades
    tracking to provide more vehicle position data, we lose it due to
    schema limitations.
    """
    def __init__(self, url, database_connection):
        self.url = url
        self.session = initialize(database_connection)
        self.cnt = 0

    def write(self):
        """
        Write rows to database.
        """
        row = get_positions(self.url)
        try:
            while True:
                vals = next(row)
                self.session.add(
                    VehiclePositions(
                        timestamp=timestamp(vals["timestamp"]),
                        vehicle_id=vals["id"],
                        label=vals["label"],
                        trip_id=vals["trip_id"],
                        longitude=vals["longitude"],
                        latitude=vals["latitude"],
                    )
                )
                self.cnt += 1
                if self.cnt >= 100:
                    self.session.commit()
                    self.cnt = 0
        finally:
            self.session.commit()

def timestamp(stamp):
    """
    Localize timestamp to EST. Obviously brittle.
    """
    return EASTERN.localize(datetime.datetime.fromtimestamp(stamp))
