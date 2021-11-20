#!/usr/bin/python
import logging
import random
import string
import os
import re
import sys
import time
import socket
import subprocess
import urllib.request
import socks
import sys
from .tor_utility import check_path, is_port_in_use
if os.name == "nt":
    from . import inet_pton
else:
    print ('[ERROR] Only supports windows OS.')
    sys.exit(0)

def clean(value):
    if sys.version_info[:2] >= (3, 0):
        return value.decode('utf-8')
    else:
        return value
    
class Proxy:

    def __init__(self, 
                 connection_port = "9050", 
                 control_port = "9051", 
                 refesh_rate = "300", 
                 exit_nodes = "", 
                 exclude_exit_nodes = "", 
                 exclude_nodes = ""):
        if (connection_port==control_port):
            print ('[ERROR] Cannot assign same port number to connection_port & control_port ')
            sys.exit(1)
        if (is_port_in_use(connection_port)):
            print ('[ERROR] Connection_port %s is used, pelase select another port.'%(connection_port))
            sys.exit(1)
        if (is_port_in_use(control_port)):
            print ('[ERROR] Control_port %s is used, please select another port.'%(control_port))
            sys.exit(1)
            
        self._proxy_type = socks.SOCKS5
        self._addr = '127.0.0.1'
        self._control_port = str(control_port)
        self._connection_port = str(connection_port)
        self._password = ''.join(random.choice(string.ascii_lowercase) for i in range(12))
        self._refresh_rate = str(refesh_rate)
        self._exit_nodes = exit_nodes
        self._exclude_exit_nodes = exclude_exit_nodes
        self.exclude_nodes = exclude_nodes
        self.cmd = None
        
    @property
    def start(self):

        search_torrc = os.getcwd()+'\\tor_proxy\\tor_configs\\win\\*torrc'
        search_torexe = os.getcwd()+'\\tor_proxy\\tor_configs\\win\\*tor.exe'
        search_geoip = os.getcwd()+'\\tor_proxy\\tor_configs\\win\\*geoip'
        search_geoip6 = os.getcwd()+'\\tor_proxy\\tor_configs\\win\\*geoip6'

        torexe = check_path(search_torexe)
        torrc = check_path(search_torrc)
        geoip = check_path(search_geoip)
        geoip6 = check_path(search_geoip6)
        
        try:
            urllib.request.urlretrieve('https://raw.githubusercontent.com/torproject/tor/main/src/config/geoip', geoip)
        except:
            print ('[INFO] Unable to update geoip file. Using local copy.')
        try:
            urllib.request.urlretrieve('https://raw.githubusercontent.com/torproject/tor/main/src/config/geoip6', geoip6)
        except:
            print ('[INFO] Unable to update geoip6 file. Using local copy.')  
        
        cmd = subprocess.Popen([torexe, '--hash-password', self._password], stdout=subprocess.PIPE)
        out, err = cmd.communicate()
        out = out.decode("utf-8") 
        password = re.search('16:.*\r\n', out).group(0)[:-2]
        
        settings = {
            "ControlPort":self._control_port,
            "GeoIPFile":geoip,
            "GeoIPv6File":geoip6,
            "DataDirectory":geoip.replace('\geoip',''),
            "HashedControlPassword":password,
            "HiddenServiceStatistics":"0",
            "Log notice":"stdout",
            "SocksPort":self._connection_port,
            "ExitNodes":self._exit_nodes,
            "ExcludeExitNodes":self._exclude_exit_nodes,
            "ExcludeNodes":self.exclude_nodes,
            "MaxCircuitDirtiness":self._refresh_rate,
            "StrictNodes":"0",
        }
        
        fd = open(torrc, "w")
        for key in settings:
            if(len(settings[key])>0):
                fd.write("%s %s\n"%(key,settings[key]))
        fd.close()
        
        self.cmd = subprocess.Popen([torexe, '-f', torrc], stdout=subprocess.PIPE)
        
        req, umsg = 1, "User requested new identity.."
        while True:
            try:
                line = self.cmd.stdout.readline()
                if line != '':
                    line = clean(line)
                    
                    if '0.3.2.10' in line:
                        t, v = (line.strip().split('running')[0].split('[notice]')[1]).split()
                        print ('[INFO] %s %s'%(t, v))
                    if 'Bootstrapped' in line:
                        per, msg = ((line.strip())[42:]).split(":")
                        print ('[INFO] %s %s'%(per, msg))
                        if 'Done' in msg:
                            print ('[INFO] TOR Socks5 listening on port: %s'%(self._connection_port))
                            break
                    if 'opened from 127.0.0.1' in line:
                        print ('[INFO] %s %s'%(req, umsg))
                        req += 1
                                     
            except KeyboardInterrupt:
                print ('[INFO] TOR service interrupted...')
                self.cmd.terminate()
                sys.exit(1)
                break
            except:
                print ('[INFO] TOR service unable to start...')
                self.cmd.terminate()
                sys.exit(1)
                break
                
        
        
    @property
    def configure_proxy(self):
        try:
            socks.set_default_proxy(self._proxy_type, self._addr, self._connection_port)
        except:
            pass
        else:
            socket.socket = socks.socksocket
            
    @property
    def set_default_proxy(self):
        socks.setdefaultproxy()

    @property
    def new_identity(self):
        print ('[INFO] TOR requesting for new identity')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._addr, int(self._control_port)))
        except:
            return 'failed'
            s.close()
        else:
            s.send(str.encode("AUTHENTICATE \"%s\"\r\n" % (self._password)))
            resp = s.recv(128)
            if resp.startswith(str.encode('250 OK')):
                s.send(str.encode('SIGNAL NEWNYM\r\n'))
                return resp
            else:
                return resp
        s.close()
    @property
    def stop(self):
        if(self.cmd):
            print ('[INFO] TOR service terminated')
            self.cmd.terminate()
        