# importeert een hoop shit
import socket, ssl, glob
import json
import uuid
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


class Apiroute():
    def __init__(self, webpath:str, responseFunc):
        self.webpath = webpath
        self.responseFunc = responseFunc

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

        def parse_json(self):
            try:
                return json.loads(self.body)
            except:
                return {}


        print(self.body)
        

class Route():
    # Maakt een route aan
    def __init__(self, webpath:str, localpath:str, contentType:str = "text/html"):
        self.webpath = webpath
        self.localpath = localpath
        self.contentType = contentType
    
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


def NewRoute(webpath, localpath, contentType = "text/html"):
    # Voegt gewoon een route toe aan een lijst maar dit ziet er clean uit.
    # Route(webpath, localpath) maakt een route, met een webpath in de vorm
    # van /test.html(voorbeeld) en een localpath naar het bestand ./pages/test.html(voorbeeld)

    routes.append(
        Route(webpath, localpath, contentType)
    )


def InitializeRoutes():
    # Maakt een lijst aan met alle bestanden in de map pages, dat doet FindFiles()
    files:list = FindFiles("pages")

    # Loopt door alle files heen en maakt een route
    for filepath in files:
        filepath = filepath.replace("\\", "/")
        route = "/" + filepath.split("/", 2)[2]
        print(route)

        if filepath.split(".")[-1] == "css": # CSS support
            NewRoute(route, filepath, "text/css")

        if filepath.split(".")[-1] == "gif": # GIF support
            NewRoute(route, filepath, "image/gif")
        
        if filepath.split(".")[-1] == "ico": # ICON support
            NewRoute(route, filepath, "image/x-icon")

        if filepath.split(".")[-1] == "png": # PNG support
            NewRoute(route, filepath, "image/png")
        
        if filepath.split(".")[-1] == "js": # JS support
            print("js")
            NewRoute(route, filepath, "text/javascript")

        else:
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


def addUser(email:str, password:str):
    user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password": password
    }
    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    
    database = json.loads(fileCont)
    database["users"].append(user)
    json_database = json.dumps(database)
    
    with open("./database/database.json", "w") as f:
        f.write(json_database)

def getUser(id:str):
    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for user in database["users"]:
        if user["id"] == id:
            return user["id"]
    
    return None

def getSession(email:str, password:str):
    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for user in database["users"]:
        if user["email"] == email:
            if user["password"] == password:
                return user["id"]
    
    return None



    
if __name__ == "__main__":
    print(getSession(email="maantjemol@e-meeuw.de", password="jemoeder"))