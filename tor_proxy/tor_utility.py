#!/usr/bin/env python
import os
import socket

def check_path(filename):
    path,ext = filename.split('*')
    for dirpath, dirname, files in os.walk(path):
        for f in files:
            if f.endswith(ext):
                path = os.path.join(dirpath, f)
    return path

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', int(port))) == 0
