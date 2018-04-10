#!/usr/bin/env python

from FunkyBusFare.streamreader import StreamReader

if __name__ == "__main__": 
    TRIP_UPDATES = "http://developer.go-metro.com/TMGTFSRealTimeWebService/TripUpdate/TripUpdates.pb"
    streamreader = StreamReader(TRIP_UPDATES, "./")
    streamreader.write()
