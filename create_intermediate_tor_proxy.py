# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 22:15:33 2021

@author: Yicong
"""
import io
import os
import stem.process
import re
import urllib.request
import requests
import json
from datetime import datetime

SOCKS_PORT = 9050
CONTROL_PORT = 9051
TOR_PATH = os.path.normpath(os.getcwd()+"\\tor\\tor.exe")
GEOIPFILE_PATH = os.path.normpath(os.getcwd()+"\\data\\tor\\geoip")
try:
    urllib.request.urlretrieve('https://raw.githubusercontent.com/torproject/tor/main/src/config/geoip', GEOIPFILE_PATH)
except:
    print ('[INFO] Unable to update geoip file. Using local copy.')
    
tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort' : str(SOCKS_PORT),
    'ControlPort' : str(CONTROL_PORT),
    'EntryNodes' : '{FR}',
    'ExitNodes' : '{JP}',
    'StrictNodes' : '1',
    'CookieAuthentication' : '1',
    'MaxCircuitDirtiness' : '60',
    'GeoIPFile' : GEOIPFILE_PATH,
    
  },
  init_msg_handler = lambda line: print(line) if re.search('Bootstrapped', line) else False,
  tor_cmd = TOR_PATH
)

PROXIES = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}
response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
result = json.loads(response.content)
print('TOR IP [%s]: %s %s'%(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), result["query"], result["country"]))


