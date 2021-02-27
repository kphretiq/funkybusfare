# funkybusfare
You'd better get off the curb.

Grab bus position data from Cincinnati, OH USA Metro Bus API endpoint at ```developer.go-metro.com```.
Flatten `protobuf` objects out, then dump to a `json` file or `sql` database.

Everything tested in >= Python 3.6 only.

# Setup
1. clone this repo
1. run ```pip install -r requirements.txt```
1. run either ```./vehicle-positions``` or ```./vehicle-positions-db```
    1. Create a `records` directory for your compressed `.json` files to land in.
1. notice either gzipped json file or database growing
1. kill process. json file should be properly formed, database should be closed correctly.
