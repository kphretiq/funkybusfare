#!/usr/bin/env python

from FunkyBusFare.streamreader import StreamReader

if __name__ == "__main__": 
    VEHPOS = "http://developer.go-metro.com/TMGTFSRealTimeWebService/vehicle/VehiclePositions.pb"
    streamreader = StreamReader(VEHPOS, "./")
    streamreader.write()
