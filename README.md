# fuel-node-names

Fuel deletes all node names (and hostnames) if environment is reset or deleted.

This script can save and restore names and hostnames.
It uses node's MAC address in fuel-admin network as unique node ID.

You can save node names to JSON file and then use this file as source of information to restore all the node names.

One more use case: update all the hostnames in accordance with the names.

See fuel-node-names.py --help for options

