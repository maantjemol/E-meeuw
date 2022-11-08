# importeert een hoop shit
import socket, ssl, glob

# Maakt alvast routes list aan voor later (scroll naar beneden voor spoilers)
routes = []

class Response():
    # Maakt het makkelijk om een responce te bouwen
    def __init__(self, status:int, data:str):
        self.status = status
        self.data = data

        
    def build(self):
        response = f"HTTP/1.1 {self.status} OK\nServer: Your_Mom\nContent-type: text/html; charset=UTF-8\n\r\n\r{self.data}\n\r\n\r"
        return response


class Request():
    # Maakt een request bruikbaar, inclusief headers
    def __init__(self, request:bytes):

        self.headers = {}
        self.request_string = request.decode()
        self.method = self.request_string.split(" ")[0]
        self.url = self.request_string.split(" ")[1]

        # split header string en stopt het in een dict voor gebruik
        lines = self.request_string.split('\n',1)[1]
        for line in lines.split("\n")[0:-2]:
            words = line.split(":", 1)
            self.headers[words[0]] = words[1].replace("\n", "").replace("\r", "")


class HTTP_Server():
    def __init__(self, address:str, port:int, routes:list):
        self.port = port
        self.routes = routes
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
            request = connstream.recv(1024)

            # Zet gare string om naar cool object met url en shit om beter te kunnen gebruiken
            request = Request(request)
            # print dat er een request wordt gedaan
            print(f"Accepting request from {fromaddr[0]}: {request.url}")

            # Zoekt de route op die hoort bij /info.html fzo 

            # Maakt er een mooi HTTP objectje van en flikkert die terug naar je browser
            response =  "test"
            connstream.sendall(response.encode())
            connstream.close()



if __name__ == "__main__":
    # We maken hier de routes aan om te gebruiken voor de webserver.
    # Denk hierbij zegmaar aan https://localhost:1111/test.html
    # Hier is /test.html de route
    InitializeRoutes()

    # Hier starten we de server op https://localhost:1111
    server = HTTP_Server("localhost", 1112, routes)
    server.start()
    
