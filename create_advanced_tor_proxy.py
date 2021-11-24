# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 22:26:58 2021

@author: Yicong
"""
import io
import os
import stem.process
from stem.control import Controller
from stem import Signal
import re
import requests
import json
from datetime import datetime
import time

SOCKS_PORT = 9050
CONTROL_PORT = 9051
TOR_PATH = os.path.normpath(os.getcwd()+"\\tor\\tor.exe")
tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort' : str(SOCKS_PORT),
    'ControlPort' : str(CONTROL_PORT),
    'CookieAuthentication' : '1' ,
    'EntryNodes' : '6B7ABD237CF25E5F787F365AF5FC4C86F0213A9F',
    'StrictNodes' : '1'
  },
  init_msg_handler = lambda line: print(line) if re.search('Bootstrapped', line) else False,
  tor_cmd = TOR_PATH
)


