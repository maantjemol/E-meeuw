# importeert een hoop shit
import glob
import re
import socket
import ssl
import threading
from mail_lib import *
from server_lib import *
from database import *
from api import *
routes = []
docker = False


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


def ApiRoutes():

    routes.append(Apiroute(
        webpath="/api/sendmail",
        responseFunc=handleSendMail
    ))

    routes.append(Apiroute(
        webpath="/api/getmail",
        responseFunc=handleGetMail
    ))

    routes.append(Apiroute(
        webpath="/api/getsendmail",
        responseFunc=handleGetSendMail
    ))

    routes.append(Apiroute(
        webpath="/api/login",
        responseFunc=handleLogin
    ))

def NewRoute(webpath, localpath, contentType = "text/html", auth=False):
    routes.append(
        Route(webpath, localpath, contentType, auth=auth)
    )

def InitializeRoutes():
    files:list = FindFiles("pages")
    for filepath in files:
        filepath = filepath.replace("\\", "/")
        route = "/" + filepath.split("/", 2)[2]
        print(route)

        auth = False
        if "inbox" in route or "compose_email" in route:
            auth = True

        if filepath.split(".")[-1] == "css": # CSS support
            NewRoute(route, filepath, "text/css", auth=False)

        if filepath.split(".")[-1] == "gif": # GIF support
            NewRoute(route, filepath, "image/gif")
        
        if filepath.split(".")[-1] == "ico": # ICON support
            NewRoute(route, filepath, "image/x-icon")

        if filepath.split(".")[-1] == "png": # PNG support
            NewRoute(route, filepath, "image/png")
        
        if filepath.split(".")[-1] == "js": # JS support
            print("js")
            NewRoute(route, filepath, "text/javascript", auth=False)

        else:
            NewRoute(route, filepath, auth=auth)
    
    NewRoute("/", "./pages/index.html", auth=False)
    NewRoute("/testpagina", "./pages/index.html", auth=False)
    NewRoute("/404", "./pages/404.html", auth=False)
    NewRoute("/login", "./pages/login/login.html", auth=False)
    NewRoute("/new_message", "./pages/new_message/compose_email.html", auth=True)
    NewRoute("/inbox", "./pages/inbox/inbox.html", auth=True)


# https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security
class HTTP_Server():
    def __init__(self, address:str, port:int, routes:list):
        self.port = port
        self.routes = routes
        self.address = address
    
    def start(self):
        print(f"Web server is starting on https://{self.address}:{self.port}\n")

        # Maakt SSL connectie aan
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(domainCert, privateCert)

        # Maakt een verbinding voor HTTPS Socket, prikt zegmaar gat in computer om netwerk shit eruit te laten lopen
        bindsocket = socket.socket()
        bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
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

                print(route.auth)

                if route.auth and (not request.cookie or not getUser(request.cookie)):
                    response = Redirect("/login/login.html").build()

                print(response)

                
                connstream.sendall(response.encode())
                connstream.close()
            except Exception as e:
                print(e)

docker = False
privateCert = './cert/server.key'
domainCert = './cert/server.crt'

if docker:
    privateCert = './pbuncerts/private.key.pem'
    domainCert = './pbuncerts/domain.cert.pem'


if __name__ == "__main__":
    email_server = Email_Server("localhost", 1114)
    web_server = HTTP_Server("localhost", 1115, routes)

    if docker:
        web_server = HTTP_Server("0.0.0.0", 443, routes)
        email_server = Email_Server("0.0.0.0", 26)

    InitializeRoutes()
    ApiRoutes()

    t1 = threading.Thread(target=email_server.start)
    t3 = threading.Thread(target=web_server.start)


    t1.start()
    t3.start()
