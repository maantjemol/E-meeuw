# importeert een hoop shit
import socket, ssl, glob
import re

def getSSLSocket():
    return ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_SSLv23)


class Email_Server():
    def __init__(self, address:str, port:int):
        self.port = port
        self.address = address
        self.email = "Uwu hello :), i eat shit."
    
    def start(self):
        pass

def sendEmail(mail_from:str, mail_to:str, message:str, server_address:str, port:int):
    sock = getSSLSocket()
    sock.connect((server_address, port))
    sock.send("HELO".encode())
    response = sock.recv(2048).decode()
    print(response)
    
    if "OK" in response:
        sock.send(f"MAIL FROM: <{mail_from}>".encode())
    else:
        print(f"could not connect to server. error: {response}")
        return
    response = sock.recv(2048).decode()
    print(response)
    
    if "OK" in response:
        sock.send(f"RCPT TO: <{mail_to}>".encode())
    else:
        print(f"could not connect to server. error: {response}")
        return
    response = sock.recv(2048).decode()
    print(response)
    
    if "OK" in response:
        sock.send("DATA\r\n".encode())
    else:
        print(f"could not connect to server. error: {response}")
        return
    response = sock.recv(2048).decode()

    sock.send(f"{message}\r\n".encode())

    response = sock.recv(2048).decode()

    fullStop = '\r\n.\r\n'
    sock.send(fullStop.encode('utf-8'))

    response = sock.recv(2048).decode()

    if "250" in response:
        sock.send("QUIT".encode())
    else:
        print(f"could not connect to server. error: {response}")
        return
    
    response = sock.recv(2048).decode()

                



if __name__ == "__main__":
    # We maken hier de routes aan om te gebruiken voor de webserver.
    # Denk hierbij zegmaar aan https://localhost:1111/test.html
    # Hier is /test.html de route
    # Hier starten we de server op https://localhost:1111
    sendEmail("maantje@gmail.com", "harry@e-meeuw.com", "Hi, i would like to contact you about your extended warranty", "localhost", 1114)
    # server = Email_Server("localhost", 1114)
    # server.start()
    
