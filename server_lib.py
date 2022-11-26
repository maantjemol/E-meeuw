# importeert een hoop shit
import socket, ssl, glob
import json
from database import *
#import os 

# Maakt alvast routes list aan voor later (scroll naar beneden voor spoilers)
routes = []

class Response():
    # Maakt het makkelijk om een responce te bouwen
    def __init__(self, status:int, data:str, contentType:str = "text/html", cookies = []):
        self.status = status
        self.data = data
        self.contentType = contentType


    # Bouwt een HTTP message om te versturen, In dit geval in de vorm:
    # 
    # HTTP/1.1 200 OK
    # Server: Your_Mom
    # Content-type: text/html; charset=UTF-8
    # "Eventuele data"
    # 

    def build(self):
        response = f"HTTP/1.1 {self.status} OK\r\nServer: e-meeuw\r\nContent-type: {self.contentType}; charset=UTF-8\n\r\n\r{self.data}\n\r\n\r"
        return response

class Redirect():
    # Maakt het makkelijk om een responce te bouwen
    def __init__(self, webpath:str):
        self.webpath = webpath

    def build(self):
        response = f"HTTP/1.1 301 Moved Permanently\r\nLocation: {self.webpath}\r\nCache-Control: no-store\r\n\r\n"
        return response

class Apiroute():
    def __init__(self, webpath:str, responseFunc):
        self.webpath = webpath
        self.responseFunc = responseFunc
        self.auth = False


    def build(self, request):
        data = self.responseFunc(request)
        data = json.dumps(data)
        return Response(200, data, "application/json").build()



class Request():
    # Maakt een request bruikbaar, inclusief headers
    def __init__(self, request:bytes):

        self.headers = {}
        self.request_string = request.decode()
        self.method = self.request_string.split(" ")[0]
        self.url = self.request_string.split(" ")[1]
        self.body = None
        self.cookie = None

        # print(self.request_string)
        # split header string en stopt het in een dict voor gebruik
        lines = self.request_string.split('\n',1)[1]

        lines = lines.split("\r\n\r\n")

        header_lines = lines[0]
        try:
            self.body = lines[1]
        except:
            self.body = None

        for line in header_lines.split("\r\n"):
            words = line.split(":", 1)
            self.headers[words[0]] = words[1][1:]
        
        try:
            self.cookie = self.headers["Cookie"].split("id=")[1]
        except:
            pass


        def parse_json(self):
            try:
                return json.loads(self.body)
            except:
                return {}


        print(self.body)
        

class Route():
    # Maakt een route aan
    def __init__(self, webpath:str, localpath:str, contentType:str = "text/html", auth=False):
        self.webpath = webpath
        self.localpath = localpath
        self.contentType = contentType
        self.auth = auth
    
    # Bouwt een response voor de route, als in een HTTP message
    def build(self, request):
        try:
            # Probeert het HTML bestand te zoeken
            file = open(self.localpath).read()
            response = Response(200, file, self.contentType).build()
            return response
        except Exception as e:
            print(f"Error: {e}")
            # Als het HTML bestand niet gevonden kan worden stuurt ie een 404 not found
            response = Response(404, "Not found").build()
            return response


def NewRoute(webpath, localpath, contentType = "text/html", auth = False):
    # Voegt gewoon een route toe aan een lijst maar dit ziet er clean uit.
    # Route(webpath, localpath) maakt een route, met een webpath in de vorm
    # van /test.html(voorbeeld) en een localpath naar het bestand ./pages/test.html(voorbeeld)

    routes.append(
        Route(webpath, localpath, contentType, auth=auth)
    )


# def InitializeRoutes():
#     # Maakt een lijst aan met alle bestanden in de map pages, dat doet FindFiles()
#     files:list = FindFiles("pages")

#     # Loopt door alle files heen en maakt een route
#     for filepath in files:
#         filepath = filepath.replace("\\", "/")
#         route = "/" + filepath.split("/", 2)[2]
#         print(route)

#         if filepath.split(".")[-1] == "css": # CSS support
#             NewRoute(route, filepath, "text/css")

#         if filepath.split(".")[-1] == "gif": # GIF support
#             NewRoute(route, filepath, "image/gif")
        
#         if filepath.split(".")[-1] == "ico": # ICON support
#             NewRoute(route, filepath, "image/x-icon")

#         if filepath.split(".")[-1] == "png": # PNG support
#             NewRoute(route, filepath, "image/png")
        
#         if filepath.split(".")[-1] == "js": # JS support
#             print("js")
#             NewRoute(route, filepath, "text/javascript")

#         else:
#             if "inbox" in route:
#                 NewRoute(route, filepath)
#             else:
#                 NewRoute(route, filepath)

    
#     # Voegt een route toe aan de lijst routes 
#     NewRoute("/", "./pages/index.html")
#     NewRoute("/testpagina", "./pages/index.html")


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

