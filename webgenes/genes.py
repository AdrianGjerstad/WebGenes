#!/usr/bin/env python3

#
# genes.py
#
# Copyright (c) Adrian Gjerstad. Project Licensed Under GNU GPLv3
# You can get yourself a copy of the license at:
#
#   https://github.com/AdrianGjerstad/WebGenes/blob/master/LICENSE
#

########################################
# IMPORTS                              #
########################################

# A-Z STDLIB
from http.server import HTTPServer, BaseHTTPRequestHandler

# A-Z WEBGENESLIB
from webgenes_path import wg_PATH

########################################
# WEBGENES REQUEST HANDLER             #
########################################

class wg_WebGenesRequestHandler(BaseHTTPRequestHandler):
  pass

########################################
# WEBGENES SERVER                      #
########################################

class wg_WebGenesServer(HTTPServer):
  pass

########################################
# SERVER SPAWNER                       #
########################################

def wg_ServerSpawner():
  pass

