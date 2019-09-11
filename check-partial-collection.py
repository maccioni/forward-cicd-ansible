#!/usr/bin/env python

import json
import sys

#https://app.forwardnetworks.com/api/networks/35619/collector/status
#    "busyStatus": "IDLE",
# Open the checks.json that contains the Checks API json output
try:
  f = open("collection.json", "r")
  if f.mode == 'r':
      file_str = f.read()
except:
  print("An exception occurred while opening the API json file")

# convert the file from string to Python object format
collection_json = json.loads(file_str)

counter = 0
while counter < 10:
  if collection_json['busyStatus'] == "COLLECTING":
      print("Collection in progress. Sleeping for 10 seconds")
      i += 1
  elif collection_json['busyStatus'] == "IDLE":
      print("Partial Collection is over!")
      break
  else:
      print("Unexpected Collection status: " + collection_json['busyStatus'])
  counter += 1

if counter = 10:
    print("Partial Collection is taking too long...Aborting...")
    exit(1)

if status == "PASS":
    print("All the Forward Check are OK!")
elif status == "FAIL":
    print("Exiting from post-chsange verification with errors!")
    sys.exit(1)
else:
    print("Unknown status: " + status)
    sys.exit(2)
