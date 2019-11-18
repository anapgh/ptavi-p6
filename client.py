#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

try:
    METHOD = sys.argv[1]
    SIP = sys.argv[2]
    login = SIP.split('@')
    server = login[1].split(':')
    user = login[0]
    ip, port = server
except (IndexError, ValueError):
    print('Usage: python3 client.py method receiver@IP:SIPport')

if METHOD == 'INVITE' or 'BYE':
    SIP = (METHOD + ' sip:' + user + '@' + ip + ' SIP/2.0')
else:
    SIP = METHOD

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((ip, int(port)))

    my_socket.send(bytes(SIP , 'utf-8') + b'\r\n\r\n')
    data = my_socket.recv(1024)
    request = data.decode('utf-8')
    if METHOD == 'INVITE':
        request = request.split('\r\n\r\n')[2]
        if request == 'SIP/2.0 200 OK':
            SIP = ('ACK' + ' sip:' + user + '@' + ip + ' SIP/2.0')
            my_socket.send(bytes(SIP , 'utf-8') + b'\r\n\r\n')
