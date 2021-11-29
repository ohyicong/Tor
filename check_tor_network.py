# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:35:16 2021

@author: Yicong
"""
from stem.control import Controller
from stem import CircStatus
import requests
import json
from datetime import datetime

with Controller.from_port(port = 9051) as controller:
    controller.authenticate()
    for circ in sorted(controller.get_circuits()):
        print(circ.status)
        if circ.status == CircStatus.BUILT:
            print("Circuit %s (%s)" % (circ.id, circ.purpose))
            for i, entry in enumerate(circ.path):
                div = '+' if (i == len(circ.path) - 1) else '|'
                fingerprint, nickname = entry
                desc = controller.get_network_status(fingerprint, None)
                address = desc.address if desc else 'unknown'
                print(" %s- %s (%s, %s)" % (div, fingerprint, nickname, address))

PROXIES = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}
response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
result = json.loads(response.content)
print('TOR IP [%s]: %s %s'%(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), result["query"], result["country"]))

