from server_lib import *
import json

routes = []
cookies = [{"Uwu":"test"}]

def NewRoute(webpath, localpath, contentType = "text/html"):
    routes.append(
        Route(webpath, localpath, contentType)
    )



def InitializeRoutes():
    files:list = FindFiles("pages")
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
    
    NewRoute("/", "./pages/index.html")
    NewRoute("/testpagina", "./pages/index.html")


def handleLogin(request):
    resp = {
        "tesasdfast": "uwu"
    }

    cookies.append({"sadfasdf":"test"})

    return resp


def ApiRoutes():
    routes.append(Apiroute(
        webpath="/api/login",
        responseFunc=handleLogin
    ))


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
            if type(route) == type(Apiroute("t", None)): #Api route
                response = route.build(request)
            else:
                response =  route.build(cookies)
            
            connstream.sendall(response.encode())
            connstream.close()



if __name__ == "__main__":
    InitializeRoutes()
    ApiRoutes()
    server = HTTP_Server("localhost", 1111, routes)
    server.start()