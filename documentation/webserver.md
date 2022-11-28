# Structure of the code
@Of hoort dit bij de README. 
The main file is mailserver.py. For clarity, we put some methods in a different file. We import mail_lib.py, server_lib.py and database.py.

# Webserver
The HTTPs server will establish a secure TCP connection from the webserver to the browser. The webserver consists of the class `HTTP_Server()` from the file `mailserver.py` and other classes and methods from the file `server_lib.py` 

## class Response()
A Class to compose the HTTP message. 
We pass the arguments `status` and `data`, where in our case `data` refers to our webpages. 

An example of the HTTP message it returns: 
```
 HTTP/1.1 200 OK
   Server: Your_Mom
   Content-type: text/html; charset=UTF-8
   "Eventuele data"
```

### method Build()
The class contains the method `build()`.
`build()` returns the HTTP message, the message is created using a f-string, parsing the status and data variables. 

## class Redirect()
A class to ease the process to composing the response message by ...

### method Build()
`build()` returns a HTTP message. The message is created by parsing the `webpath` variable in a string. 

## class Apiroute()
A class to 

### method Build()

## class Request()
A Class to format the request received from the browser. 
We pass the argument `request` of type bytes. 
Furthermore, the class contains the following object properties:
- `request_string`, where the bytes from the `request` argument are translated to a string. 
- `method`, the first word of the `request_string`
- `url`, the second word of the `request_string`
- `headers`, a dictionary object containing the headers of the request. 


For example, the following `request_string`: 
```http
GET /search.html HTTP/1.1
Host: www.google.com
User-Agent: Mozilla/5.0
Accept: /
```
Will result in the `method` GET, the `url` /search.html and the `headers`: 
```json
{
   "Host":"www.google.com",
   "User-Agent":"Mozilla/5.0",
   "Accept":"/"
}
```

### method Parse_json()


## class Route()
A class to compose the route. 
We pass the arguments `webpath` and `localpath`.

### method Build()
The class contains the method `build()`.
`build()` will try to find the HTML file, specified in the `localpath` variable, in the folder `pages`. When it does, `build()` will build a HTTP response using the `Response.build()` method with status 200 and the file. In case the HTML file is not found, the method will return a response with status 404 and the message 'Not found'.
Furthermore, the class contains the following methods:

### method NewRoute()
This method will append a new route to a list of routes. 
The route is created inside the method, using the parameters `webpath` and `localpath`, and then added to the list `routes`.

### method InitializeRoutes() @Different file
This method will go through all the files in the folder `pages` and initialize the method `NewRoute()` to map the routes to all pages. All routes are then added to the list `routes`. 

### method FindFiles()
This method will return a list of all the files in a folder. 
In order to do this, we initialize the `glob()` method to retrieve the pathnames and add them to the list `files`.


## class HTTP_Server @mailserver.py
This class .... We pass the arguments `self`, `address`, `port`, and `routes`.
Furtermore, the class contains the method `start()`

### method Start()
The method will print a string stating the address and port where the server will be starting. 
Next, the SSL connection is initiated. We create a `SSLContext` object. 
We create an object `socket` using the `socket` module. We set parameters (?) for the socket and assign an IP address and portnumber to the socket. `bindsocket.listen(1)` means the server is now listening for connection requests to its assigned port. `1` is the backlog argument of the method, this argument specifies the maximum number of queued connections. [Why we chose 1]. 
We stay in a while loop as long as ... (always?)
The while loop handles incoming TCP requests (?).
When a connection comes in, we return a new socket representing the connection and the address of the client. 



