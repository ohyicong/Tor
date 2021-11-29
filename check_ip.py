# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 11:48:06 2021

@author: Yicong
"""
import requests
import json
from datetime import datetime
PROXIES = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}
response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
result = json.loads(response.content)
print('TOR IP [%s]: %s %s'%(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), result["query"], result["country"]))
