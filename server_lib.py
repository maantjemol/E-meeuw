# import necessary modules
import socket, ssl, glob
import json
from database import *
#import os 

# Create an empty list for the routes to our webpages
routes = []

class Response():
    """Response object
    """
    def __init__(self, status:int, data:str, contentType:str = "text/html", cookies = []):
        self.status = status
        self.data = data
        self.contentType = contentType

    def build(self):
        """Builds the HTTP response string

        Returns:
            string: response string
        """
        response = f"HTTP/1.1 {self.status} OK\r\nServer: e-meeuw\r\nContent-type: {self.contentType}; charset=UTF-8\n\r\n\r{self.data}\n\r\n\r"
        return response

class Redirect():
    """Redirect object
    """
    def __init__(self, webpath:str):
        self.webpath = webpath

    def build(self):
        """Builds the HTTP response for a redirect

        Returns:
            string: response string
        """
        response = f"HTTP/1.1 301 Moved Permanently\r\nLocation: {self.webpath}\r\nCache-Control: no-store\r\n\r\n"
        return response

class Apiroute():
    """Apiroute object
    """
    def __init__(self, webpath:str, responseFunc):
        self.webpath = webpath
        self.responseFunc = responseFunc
        self.auth = False


    def build(self, request):
        """Connects a function to the api route and passes the request to the function that handles the API

        Args:
            request (Request): the incomming request

        Returns:
            Response: An Response object
        """
        data = self.responseFunc(request)
        data = json.dumps(data)
        return Response(200, data, "application/json").build()



class Request():
    """Request object
    """
    # Formats a connection request to a string containing the headers
    def __init__(self, request:bytes):

        self.headers = {}
        self.request_string = request.decode()
        self.method = self.request_string.split(" ")[0]
        self.url = self.request_string.split(" ")[1]
        self.body = None
        self.cookie = None

        # Split the header string and put it in a dictionary object
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
            """Parses json in a request

            Returns:
                Object: the parsed JSON object
            """
            # Decode a JSON object to a Python object
            try:
                return json.loads(self.body)
            except:
                return {}
        

class Route():
    """Route object
    """
    def __init__(self, webpath:str, localpath:str, contentType:str = "text/html", auth=False):
        self.webpath = webpath
        self.localpath = localpath
        self.contentType = contentType
        self.auth = auth
    
    # Build a HTTP response for the route
    def build(self, request):
        """Builds a route by finding the file the route is connected to and passing it through the Response.build() method

        Args:
            request (request): Not used

        Returns:
            string: the response string
        """
        try:
            # Try to find the HTML file
            file = open(self.localpath).read()
            response = Response(200, file, self.contentType).build()
            return response
        except Exception as e:
            print(f"Error: {e}")
            # In case we cannot find the HTML file, we send a 404 error
            response = Response(404, "Not found").build()
            return response


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


def FindFiles(folder:str):
    """Finds all files in an folder

    Args:
        folder (str): the folder you want to find the files in

    Returns:
        list: a list with files in the folder
    """
    files = []
    for f in glob.glob(f'./{folder}/**/*.*', recursive=True):
        files.append(f)
    return files


def FindRoute(routes, url):
    # Search the list routes for a route that matches the url of the connection request

    for route in routes:
        if route.webpath == url:
            return route
    # If there is no match, we return the route to our error page        
    return Route("/", "./pages/404.html")

