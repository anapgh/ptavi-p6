#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        for line in self.rfile:
            message_client = line.decode('utf-8')
            if message_client != '\r\n':
                parametros_client = ''.join(message_client).split()
                method = parametros_client[0]
                others = parametros_client[1:]
                sip = others[0].split(':')[0]
                version = others[1]
                if sip != 'sip' or version != 'SIP/2.0':
                    request = (b"SIP/2.0 400 Bad Request\r\n\r\n")
                    self.wfile.write(request)
                else:
                    if method == 'INVITE':
                        request = (b'SIP/2.0 100\r\n\r\n')
                        request = (request + b'Trying SIP/2.0 180 Ringing\r\n\r\n')
                        request = (request + b'SIP/2.0 200 OK\r\n\r\n')
                        self.wfile.write(request)
                    elif method == 'BYE':
                        request = (b"SIP/2.0 200 OK\r\n\r\n")
                        self.wfile.write(request)
                    else:
                        request = (b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
                        self.wfile.write(request)



if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        audio_file = sys.argv[3]
        serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    except (IndexError, ValueError):
        sys.exit('Usage: python3 server.py IP port audio_file')

    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
