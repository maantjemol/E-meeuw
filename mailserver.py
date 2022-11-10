# importeert een hoop shit
import socket, ssl, glob
import re

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
            
            # Recieve connection and HELO message
            request = connstream.recv(1024).decode()
            if request[:4] == "HELO":
                print(request)
                connstream.sendall("250 OK".encode())
            else:
                connstream.sendall("450".encode())
                connstream.close()
                break

            request = connstream.recv(1024).decode()
            if "MAIL FROM" in request:
                regex = r"(?<=<).*?(?=>)" # Everything between < >
                email = re.findall(regex, request)
                print(email)
                connstream.sendall("250 OK".encode())
            else:
                connstream.sendall("450".encode())
                connstream.close()
                break
                

                



if __name__ == "__main__":
    # We maken hier de routes aan om te gebruiken voor de webserver.
    # Denk hierbij zegmaar aan https://localhost:1111/test.html
    # Hier is /test.html de route
    # Hier starten we de server op https://localhost:1111
    server = Email_Server("localhost", 1112)
    server.start()
    
