#!/usr/bin/env python

import subprocess
import json
import sys


def nmap(args, kwargs):
    """
    nmap $ARGS $ADDRESS -oX nmap_out.xml
    """
