from server_lib import *
import json

routes = []

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
    request_data = json.loads(request.body)
    
    session = getSession(email=request_data["username"], password=request_data["password"])
    
    resp = {
        "error": "Username or password not correct",
        "success": False
    }

    if session:
        resp = {
            "cookie": session,
            "success": True
        }

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
        context.load_cert_chain(domainCert, privateCert)

        # Maakt een verbinding voor HTTPS Socket, prikt zegmaar gat in computer om netwerk shit eruit te laten lopen
        bindsocket = socket.socket()
        bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        bindsocket.bind((self.address, self.port))
        # gaat luisteren of er ook shit naar binnen komt
        bindsocket.listen(1)

        while True:
            try:
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
                response =  route.build(request)
                
                connstream.sendall(response.encode())
                connstream.close()
            except Exception as e:
                print(e)

docker = False
privateCert = './cert/server.key'
domainCert = './cert/server.crt'

if __name__ == "__main__":
    InitializeRoutes()
    ApiRoutes()
    if docker:
        server = HTTP_Server("0.0.0.0", 443, routes)
        privateCert = './pbuncerts/private.key.pem'
        domainCert = './pbuncerts/domain.cert.pem'
    else: 
        server = HTTP_Server("localhost", 1113, routes)
    server.start()