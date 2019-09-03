#!/usr/bin/env python

import json
import sys

# Open the checks.json that contains the Checks API json output
try:
  f = open("checks.json", "r")
  if f.mode == 'r':
      file_str = f.read()
except:
  print("An exception occurred while opening the API json file")

# convert the file from string to Python object format
checks_json = json.loads(file_str)

status = "PASS"
for check in checks_json:
    if check['status'] == "FAIL":
        # if it's the first failing check, change status and print error message
        if status == "PASS":
            status = "FAIL"
            print("These Checks failed:")
        print(check['id'])

if status == "PASS":
    print("All the Forward Check are OK!")
elif status == "FAIL":
    sys.exit(1)
else:
    print("Unknown status: " + status)
    sys.exit(1)
