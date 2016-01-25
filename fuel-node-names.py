#!/usr/bin/env python


import os
import re
import json
import argparse

def do (cmd):
    error_code = os.system(cmd)
    if (error_code):
        print "Can't do command:", cmd
        exit(1)


def get_fuel_nodelist (env):
    nodelist={}
    if env:
       cmd = "fuel node --env={0}".format(env)
    else: 
       cmd = "fuel node"
    result = os.popen(cmd)
    output = result.read()
    for line in output.split('\n'):
       m = re.search ("^(\d+)\s+.*(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})\s", line)
       if m:
          nodelist[m.group(2)] = m.group(1) 
    return nodelist


def get_fuel_nodenames (env):
    nodename={}
    if env:
       cmd = "fuel node --env={0}".format(env)
    else: 
       cmd = "fuel node"

    result = os.popen(cmd)
    output = result.read()
    for line in output.split('\n'):
       m = re.search ("^\d+\s+\|.*?\|\s+(.*?)\s+\|.*(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})\s", line)
       if m:
          nodename[m.group(2)]=m.group(1)   
    return nodename

def get_filename(env=False):
   file = 'fuel-node-names'
   if env:
       file += '-env-{0}'.format(env)
   file += '.json'
   return file 

def get_fuel_token():
    result = os.popen("fuel token")
    token = result.read()
    return token 

def dump_data(file, data):
    with open(file,'w') as outfile:
       json.dump(data, outfile)
       print "Data are stored to the file: {0}".format(file)
       return True

def load_data(file):
    with open(file) as infile:
        data = json.load(infile)
        return data

#parsing CLI arguments       
parser = argparse.ArgumentParser()
parser.add_argument('-e', '--env', action="store", default=False, dest="env", help="Specify the environment id")
parser.add_argument('-f', '--file', action="store", default=False, dest="file", help="File to save/restore node names")
parser.add_argument('-s', '--save node names', action="store_true", dest="save", help="Save node names for the environment")
parser.add_argument('-r', '--restore', action="store_true", default=False, dest="restore", help="Restore node names  for the environment")
parser.add_argument('-o', '--omit-hostnames', action="store_true", default=False, dest="omit_hostnames", help="Do NOT update hostnames (use with --restore)")

args = parser.parse_args()

if args.env:
   env = int(args.env)   
else:
   env = None

if args.file:
   file = args.file
else:
   file = get_filename(env)

if args.restore:
    current_nodes = get_fuel_nodelist(env)
    nodenames = load_data(file) 
    token = get_fuel_token()

    for mac in current_nodes:
        node_id = current_nodes[mac]
        if nodenames.has_key(mac):
            node_name = nodenames[mac] 
            json = '{"name":' + '"{0}"'.format(node_name) + '}'
            cmd = "curl -si -H 'X-Auth-Token:{0}'  -H 'Content-Type: application/json' -X PUT -d '{1}' http://localhost:8000/api/nodes/{2}".format(token, json, node_id)
            print cmd
            do(cmd)
            if not args.omit_hostnames: 
                json = '{"hostname":' + '"{0}"'.format(node_name) + '}'
                cmd = "curl -si -H 'X-Auth-Token:{0}'  -H 'Content-Type: application/json' -X PUT -d '{1}' http://localhost:8000/api/nodes/{2}".format(token, json, node_id)
                print cmd
                do(cmd)

     
if args.save:
    nodename = get_fuel_nodenames(env)
    dump_data(file,nodename) 




