# fuel-save-restore

Fuel loses all the information about node names (and hostnames) if environment is reset or deleted.

This script can save and restore some information (node names and hostnames and network settings).
It uses node's MAC address in fuel-admin network as unique node ID.

You can save your settings to YAML file and then use this file as source of information to restore.

One more use case: update all the hostnames in accordance with the names. 
(You don't need to update hostnames manually anymore)

See fuel-save-restore.py --help for options


