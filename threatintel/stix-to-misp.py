#!/usr/bin/env python3

##########################
#     WRAPPER SCRIPT     #
#     DEALS WITH STIX    #
#     TO MISP            #
##########################


import argparse
import pyaml
import sys
import json
import base64
import os

from stix.core import STIXPackage
from threatintel.servers import misp

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("-c", "--config", help="Path to config file. Default is misp.login.")
parser.add_argument("file", help="The STIX file to push")

args = parser.parse_args()

# Set the config file
if args.config:
    configfile = args.config
else:
    configfile = os.path.expanduser("~/.misptostix/misp.login")

try:
    with open(configfile, "r") as f:
        CONFIG = pyaml.yaml.load(f)
except FileNotFoundError:
    print("Could not find config file {}".format(configfile))
    sys.exit(1)

# This is just a file conversion
# Relatively quick and easy
MISP = misp.MISP(CONFIG["MISP"]["URL"], CONFIG["MISP"]["KEY"])

# We'll use my nice little misp module
# Load the package
try:
    pkg = STIXPackage().from_xml(open(args.file, "r")) 
except:
    try:
        pkg = STIXPackage.from_json(open(args.file, "r"))
    except:
        print("Could not load package!")
        sys.exit(1)

MISP.push(pkg)
