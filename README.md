# funkybusfare
You'd better get off the curb.

Sketch for listening daemons. They simply grab data from ```developer.go-metro.com```, flatten it out and then dump to a json file or database.

Everything tested in python3 only.

# Setup
1. clone this repo
1. if you are not runing python 3, make a nice virtualenv and source it
1. run ```pip install -r requirements.txt```
1. run either ```./vehicle-positions``` or ```./vehicle-positions-db```
1. notice either gzipped json file or database growing
1. kill process. json file should be properly formed, database should be closed correctly.
