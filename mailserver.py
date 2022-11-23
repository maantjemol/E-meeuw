# importeert een hoop shit
import glob
import re
import socket
import ssl


def fprint(s:str):
    print(f"> {s}")

global fromEmail
global SendEmail

def acceptEmail(connstream):
    
    email = ''

    print("got connection!")

    request = connstream.recv(1024).decode()

    fromEmail = ""
    rcptEmail = ""

    if "HELO" in request:
        fprint(request)
        connstream.sendall("250 OK".encode())
    else:
        connstream.sendall("450".encode())
        connstream.close()
        return



    request = connstream.recv(1024).decode()
    if "MAIL FROM" in request:
        regex = r"(?<=<).*?(?=>)" # Everything between < >
        fromEmail = re.findall(regex, request)[0]
        fprint(request)
        print(fromEmail)
        connstream.sendall("250 OK".encode())
    else:
        connstream.sendall("450".encode())
        connstream.close()
        return

    request = connstream.recv(1024).decode()
    if "RCPT TO" in request:
        regex = r"(?<=<).*?(?=>)" # Everything between < >
        rcptEmail = re.findall(regex, request)[0]
        fprint(request)
        print(rcptEmail)
        connstream.sendall("250 OK".encode())
    else:
        connstream.sendall("450".encode())
        connstream.close()
        return
    
    request = connstream.recv(1024).decode()
    if "DATA" in request:
        fprint(request)
        connstream.sendall("354 End data with <CR><LF>.<CR><LF>".encode())
    else:
        connstream.sendall("450".encode())
        connstream.close()
        return
    
    while True:
        request = connstream.recv(1024).decode()
        if '\r\n.\r\n' in request:
            connstream.sendall("250 OK: queued as 12345".encode())
            break
        else:
            connstream.sendall("250 OK".encode())
            email += request
    
    request = connstream.recv(1024).decode()
    if request == "QUIT":
        connstream.sendall("221 Bye".encode())
        connstream.close()

    fprint(email)
           


class Email_Server():
    def __init__(self, address:str, port:int):
        self.port = port
        self.address = address
    
    def start(self):
        print(f"Server is starting on {self.address}:{self.port}\n")

        # Maakt SSL connectie aan
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('./cert/server.crt', './cert/server.key')

        # Maakt een verbinding voor HTTPS Socket, prikt zegmaar gat in computer om netwerk shit eruit te laten lopen
        bindsocket = socket.socket()
        bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        bindsocket.bind((self.address, self.port))
        # gaat luisteren of er ook shit naar binnen komt
        bindsocket.listen(1)
        

        while True:
            # Accepteert TCP connectie en maakt hem veilig met magie fzo
            newsocket, fromaddr = bindsocket.accept()
            connstream = context.wrap_socket(newsocket, server_side=True) # Magie

            acceptEmail(connstream)

            connstream.close()

            
            

                



if __name__ == "__main__":
    server = Email_Server("localhost", 1114)
    server.start()
    
