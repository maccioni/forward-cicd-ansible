#!/usr/bin/env python

import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "name",
    help="The firewall name ")

args = parser.parse_args()

#
# This script adds the new security rule and new service object to the fw config
# by replacing the top most line (identify by the keyword) with the configs
# snipets created by the jinja2 templates
#

# Variables to add the new security rule on top position
rule_key = 'rules {'
rule_file_name = "configs/" + args.name + "_rule.txt"
add_rule = open(rule_file_name).read()

# Variables used to add the new security object
address_key = 'address {'
address_file_name = "configs/" + args.name + "_address.txt"
add_address = open(address_file_name).read()

# The initial configuration before the change is save in the local directory
# while the new modified configuration is saved in the configs directory
initial_config_file_name = "./tmp/" + args.name + "_config.txt"
modified_config_file_name = "./configs/" + args.name + "_config.txt"
with open(initial_config_file_name) as data:
    with open(modified_config_file_name, 'w') as new_data:
        for line in data:
            # look for the line with rule keyword and replace with new rule
            if rule_key in line:
                line = line.replace(rule_key, add_rule)
            # look for the line with the address keyword and replace with new rule
            elif address_key in line:
                line = line.replace(address_key, add_address)
            # Save the line (original or modified)
            new_data.write(line)
