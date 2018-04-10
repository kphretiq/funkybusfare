# funkybusfare
You'd better get off the curb.

Sketch for listening daemons. They simply grab data from ```developer.go-metro.com```, flatten it out and then dump to a json file.

Everything tested in python3 only.

# TODO
1. dump to postgres or other useful database
1. use daemonize to listen
1. find out from metro what the acceptable cycle for hitting the api is
