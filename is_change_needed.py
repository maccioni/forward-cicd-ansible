#!/usr/bin/env python

import json
import os
import requests
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "url",
    help="The URL of the deviceSource endpoint")
parser.add_argument(
    "username",
    help="Forward Networks instance username")
parser.add_argument(
    "password",
    help="Forward Networks instance username")
parser.add_argument(
    "--verify",
    help="Whether to verify the certificate on the instance "
         "(e.g. True or False)",
    action="store_true")

args = parser.parse_args()

# The patch APIs returns device names.
# This function translates device name into device ip 
def get_device_ip(device_name):
    device_list = requests.get(args.url, auth=(args.username, args.password), verify=args.verify).json()
    for device in device_list:
        if device["name"] == device_name:
            return device["host"]

# Open the paths.json that contains the Path API json output
try:
  f = open("paths.json", "r")
  if f.mode == 'r':
      file_str = f.read()
except:
  print("An exception occurred while opening the API json file")

# convert the file from string to Python object format
paths_json = json.loads(file_str)
f.close()

# Extract the first path and the related outcomes
best_path = paths_json['info']['paths'][0]
path_security_outcome   = best_path['securityOutcome']
path_forwarding_outcome = best_path['forwardingOutcome']

# Take action based on the forwarding and security outcomes
# Possible values:
# forwardingOutcome: DELIVERED, DELIVERED_TO_INCORRECT_LOCATION, BLACKHOLE, DROPPED, INADMISSIBLE, UNREACHABLE, LOOP
# securityOutcome: PERMITTED, DENIED

if path_forwarding_outcome != "DELIVERED":
    print("The is no valid routing path between source and destination")
    print("Please contact your network administrator")
    exit(1)

elif path_forwarding_outcome == "DELIVERED" and path_security_outcome == "PERMITTED":
    print("The security policy is already configured. No changes needed")

elif path_forwarding_outcome == "DELIVERED" and path_security_outcome == "DENIED":
    print("The forwarding is OK but the security rules need to be changed on these devices: ")
    f_ip = open("firewall_ip","w+")
    f_name = open("firewall_name","w+")
    for hop in best_path['hops']:
        for behavior in hop['behaviors']:
            if behavior == "ACL_DENY":
                #Save device name into file
                print(hop['deviceName'])
                f_name.write(hop['deviceName'])
                #Translate device name into device ip and store it into a files
                firewall_ip = get_device_ip(hop['deviceName'])
                print(firewall_ip)
                f_ip.write(firewall_ip)
    f_ip.close()
    f_name.close()

else:
    print("Something went wrong!!")
    print("Path Security Outcome: "   + path_security_outcome)
    print("Path Forwarding Outcome: " + path_forwarding_outcome)
    exit(1)
