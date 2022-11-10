# importeert een hoop shit
import socket, ssl, glob
import os

# Maakt alvast routes list aan voor later (scroll naar beneden voor spoilers)
routes = []

class Response():
    # Maakt het makkelijk om een responce te bouwen
    def __init__(self, status:int, data:str):
        self.status = status
        self.data = data

    # Bouwt een HTTP message om te versturen, In dit geval in de vorm:
    # 
    # HTTP/1.1 200 OK
    # Server: Your_Mom
    # Content-type: text/html; charset=UTF-8
    # "Eventuele data"
    # 
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


class Route():
    # Maakt een route aan
    def __init__(self, webpath:str, localpath:str):
        self.webpath = webpath
        self.localpath = localpath
    
    # Bouwt een response voor de route, als in een HTTP message
    def build(self):
        try:
            # Probeert het HTML bestand te zoeken
            file = open(self.localpath).read()
            response = Response(200, file).build()
            return response
        except:
            # Als het HTML bestand niet gevonden kan worden stuurt ie een 404 not found
            response = Response(404, "Not found").build()
            return response


def NewRoute(webpath, localpath):
    # Voegt gewoon een route toe aan een lijst maar dit ziet er clean uit.
    # Route(webpath, localpath) maakt een route, met een webpath in de vorm
    # van /test.html(voorbeeld) en een localpath naar het bestand ./pages/test.html(voorbeeld)

    routes.append(
        Route(webpath, localpath)
    )


def InitializeRoutes():
    # Maakt een lijst aan met alle bestanden in de map pages, dat doet FindFiles()
    files:list = FindFiles("pages")

    # Loopt door alle files heen en maakt een route
    for filepath in files:
        correctFilePath = filepath.replace("\\", "/")
        print(correctFilePath)
        route = "/" + correctFilePath.split("/", 2)[2]
        print(route)
        NewRoute(route, filepath)
    
    # Voegt een route toe aan de lijst routes 
    NewRoute("/", "./pages/index.html")
    NewRoute("/testpagina", "./pages/index.html")


def FindFiles(folder):
    # Maakt een lijst van alle bestanden in een map

    files = []
    for f in glob.glob(f'./{folder}/**/*.*', recursive=True):
        files.append(f)
    return files


def FindRoute(routes, url):
    # Zoekt in de routes en kijkt of er een route is die overeen komt met de url

    for route in routes:
        if route.webpath == url:
            return route
    return Route("/", "./pages/404.html")


class HTTP_Server():
    def __init__(self, address:str, port:int, routes:list):
        self.port = port
        self.routes = routes
        self.address = address
    
    def start(self):
        print(f"Server is starting on https://{self.address}:{self.port}\n")

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
            route = FindRoute(self.routes, request.url)

            # Maakt er een mooi HTTP objectje van en flikkert die terug naar je browser
            response =  route.build()
            connstream.sendall(response.encode())
            connstream.close()



if __name__ == "__main__":
    # We maken hier de routes aan om te gebruiken voor de webserver.
    # Denk hierbij zegmaar aan https://localhost:1111/test.html
    # Hier is /test.html de route
    InitializeRoutes()

    # Hier starten we de server op https://localhost:1111
    server = HTTP_Server("localhost", 1111, routes)
    server.start()
    
