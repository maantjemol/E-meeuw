# importeert een hoop shit
import glob
import re
import socket
import ssl
import threading
from mail_lib import *
from server_lib import *
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


def handleSendMail(request):
    request_data = json.loads(request.body)
    user_data = getUser(request_data["uid"])

    if not user_data:
        return {"success": False, "error": "uid not found"}
    
    from_email = user_data["email"]

    to_email = request_data["to_email"]
    subject = request_data["subject"]
    uid = request_data["uid"]
    contents = request_data["contents"]

    addSendEmail(
        from_email = from_email,
        to_email = to_email,
        subject = subject,
        uid = uid,
        contents = contents,
    )
    # session = getSession(email=request_data["username"], password=request_data["password"])
    server_address = to_email.split("@")[-1]
    port = 25

    if("e-meeuw.de" in server_address):
        server_address = "localhost"
        port = 1114

    sendEmail(
        mail_from = from_email, 
        mail_to = to_email, 
        message = contents, 
        server_address = server_address, 
        subject=subject,
        port=port
    )

    resp = {
        "success": True
    }

    return resp

def handleGetMail(request):
    request_data = json.loads(request.body)

    if not request_data["uid"]:
        return {"success": False, "error": "no UID"}

    emails = getMail(request_data["uid"])

    resp = {
        "success": True,
        "emails": emails
    }

    return resp


def ApiRoutes():

    routes.append(Apiroute(
        webpath="/api/sendmail",
        responseFunc=handleSendMail
        # {
        #     "from_email": from_email,
        #     "uid": uid,
        #     "to_email": to_email,
        #     "subject": subject,
        #     "contents": contents
        # }
    ))

    routes.append(Apiroute(
        webpath="/api/getmail",
        responseFunc=handleGetMail
        # {
        #     "uid": uid,
        # }
    ))

    routes.append(Apiroute(
        webpath="/api/login",
        responseFunc=handleLogin
    ))

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
    email_server = Email_Server("localhost", 1114)
    web_server = HTTP_Server("localhost", 1115, routes)

    InitializeRoutes()
    ApiRoutes()

    t1 = threading.Thread(target=email_server.start)
    t3 = threading.Thread(target=web_server.start)


    t1.start()
    t3.start()

    
    
