# funkybusfare
You'd better get off the curb.

Sketch for listening daemons. They simply grab data from ```developer.go-metro.com```, flatten it out and then dump to a json file.

Everything tested in python3 only.

# Setup
1. clone this repo
1. if you are not runing python 3, make a nice virtualenv and source it
1. run either ```./trip_updates.py``` or ```vehicle_positions.py```
1. notice json files growing in directory
1. kill process and note that json file is still properly formed.

# TODO
1. dump to postgres or other useful database
1. use daemonize to listen
1. find out from metro what the acceptable cycle for hitting the api is
1. normalize timestamps to utc
