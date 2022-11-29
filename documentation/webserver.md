# Structure of the code
@Of hoort dit bij de README. 
The main file is mailserver.py. For clarity, we put some methods in a different file. We import mail_lib.py, server_lib.py and database.py.

# Webserver
The HTTPs server will establish a secure TCP connection from the webserver to the browser. The webserver consists of the class `HTTP_Server()` from the file `mailserver.py` and other classes and methods from the file `server_lib.py` 

## class Response()
A Class to build a HTTP response message. 
We pass the arguments `status`, `data`, `contentType` and `cookies`.  Here, `data` refers to our webpages. Furthermore, `contentType` defaults to `"text/html"` and  `cookies` is set to an empty list.

An example of the HTTP message `response()` returns: 
```http
HTTP/1.1 200 OK
Server: Your_Mom
Content-type: text/html; charset=UTF-8
"Eventuele data"
```

### method Build()
The class contains the method `build()` to compose the HTTP message.
The message is created using a f-string, by parsing the `status`, `contentType` and `data` variables to a string containing a template for the message. 


## class Redirect()
In case we cannot reach a page, we can redirect the user to another one. This is the purpose of this class. `Redirect()` returns a HTTP message similar to the one `response()` produces.

An example of the HTTP message `redirect()` returns: 
```http
HTTP/1.1 301 Moved Permanently
Location: login/login.html
Cache-Control: no-store
```

### method Build()
`build()` returns a HTTP message. The message is created by parsing the `webpath` variable in a string containing a template for this message. In the template, the statuscode is already set to 301 and the cache-control is turned off, meaning browsers are not allowed to cache a response and must pull it from the server each time it's requested. This is necessary to keep the browser from passing over the original location indefinitely. 

## class Apiroute()
A class to format a HTTP response to ... based on information from the api?

### method Build()
The cookie and succes variable obtained when executing responseFunc are formatted to a JSON string by `json.dumps`.
`build()` returns a HTTP message with `statuscode` 200, the JSON string and `contentType` "application/json". 

## class Request()
A Class to format the request received from the browser. 
We pass the argument `request` of type bytes. 
Furthermore, the class initializes the following object properties:
- `request_string`; where the bytes from the `request` argument are translated to a string. 
- `method`, the first word of the `request_string`
- `url`, the second word of the `request_string`
- `body`, this variable defaults to `none`
- `cookie`, this variable defaults to `none`
- `headers`, a dictionary object containing the different headers of the request.

For example, the following `request_string`: 
```http
GET /search.html HTTP/1.1
Host: www.google.com
User-Agent: Mozilla/5.0
Cookie: id=51ed9756-11f4-46e7-8596-f1627a89b8ea;
Accept: /
```
Will result in the `method` GET, the `url` /search.html, the `cookie` 51ed9756-11f4-46e7-8596-f1627a89b8ea and the `headers`: 
```json
{
   "Host":"www.google.com",
   "User-Agent":"Mozilla/5.0",
   "Cookie":"id=51ed9756-11f4-46e7-8596-f1627a89b8ea",
   "Accept":"/"
}
```

Finally, for the `cookie` variable, we remove the 'id=' to suit our future format purposes. 

### method Parse_json()
A method that returns a JSON document in the format of a Python object. We utilize the method `json.loads()` to chance the format. 

## class Route()
A class to build the route. 
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



152 Redirecten als: User bestaat niet, er zijn geen cookies. 