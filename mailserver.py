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
    """The Email server
    """
    def __init__(self, address:str, port:int):
        self.port = port
        self.address = address
    
    def start(self):
        """Starts the email server
        """
        print(f"SMTP server is starting on {self.address}:{self.port}\n")

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('./cert/server.crt', './cert/server.key')

        bindsocket = socket.socket()
        bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        bindsocket.bind((self.address, self.port))
        # Begin listening on socket
        bindsocket.listen(1)
        

        while True:
            # Accepts TCP
            newsocket, fromaddr = bindsocket.accept()
            connstream = context.wrap_socket(newsocket, server_side=True) # Magie

            acceptEmail(connstream)

            connstream.close()


def ApiRoutes():
    """Appends API routes to the routes array
    """
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

def NewRoute(webpath:str, localpath:str, contentType:str = "text/html", auth:bool = False):
    """Initializes a new route and adds it to the routes array

    Args:
        webpath (str): the url used in the browser
        localpath (str): the path of the file requested
        contentType (str, optional): the contenttype of the request/file. Defaults to "text/html".
        auth (bool, optional): Can only view this route when you are logged in. Defaults to False.
    """
    routes.append(
        Route(webpath, localpath, contentType, auth=auth)
    )


def InitializeRoutes():
    """Initializes routes by looping thru files and adding them to the routes
    """
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
        
        if filepath.split(".")[-1] == "js": # JS support
            NewRoute(route, filepath, "text/javascript", auth=False)

        else:
            NewRoute(route, filepath, auth=auth)
    
    NewRoute("/", "./pages/index.html", auth=False)
    NewRoute("/testpagina", "./pages/index.html", auth=False)
    NewRoute("/404", "./pages/404.html", auth=False)
    NewRoute("/login", "./pages/login/login.html", auth=False)
    NewRoute("/new_message", "./pages/new_message/compose_email.html", auth=True)
    NewRoute("/inbox", "./pages/inbox/inbox.html", auth=True)


class HTTP_Server():
    """The HTTP server class
    """
    def __init__(self, address:str, port:int, routes:list):
        self.port = port
        self.routes = routes
        self.address = address
    
    def start(self):
        """Starts the HTTPs server
        """
        print(f"Web server is starting on https://{self.address}:{self.port}\n")

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(domainCert, privateCert)

        bindsocket = socket.socket()
        bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
        bindsocket.bind((self.address, self.port))
        # gaat luisteren of er ook shit naar binnen komt
        bindsocket.listen(1)

        while True:
            try:
                # Accepts request
                newsocket, fromaddr = bindsocket.accept()
                connstream = context.wrap_socket(newsocket, server_side=True) # Magic
                request = connstream.recv(1024)

                # Makes a request object
                request = Request(request)

                # prints request
                print(f"Accepting request from {fromaddr[0]}: {request.url}")

                # Searches Route 
                route = FindRoute(self.routes, request.url)

                # Builds HTTP response
                response =  route.build(request)

                if route.auth and (not request.cookie or not getUser(request.cookie)):
                    response = Redirect("/login/login.html").build()

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
