# importeert een hoop shit
import socket, ssl, glob
import re

def getSSLSocket():
    return ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_SSLv23)


class Email_Server():
    def __init__(self, address:str, port:int):
        self.port = port
        self.address = address
    
    def start(self):
        sock = getSSLSocket()
        sock.connect((self.address, self.port))
        sock.send("HELO".encode())
        response = sock.recv(2048).decode()
        print(response)

        


                

                



if __name__ == "__main__":
    # We maken hier de routes aan om te gebruiken voor de webserver.
    # Denk hierbij zegmaar aan https://localhost:1111/test.html
    # Hier is /test.html de route
    # Hier starten we de server op https://localhost:1111
    server = Email_Server("localhost", 1112)
    server.start()
    
