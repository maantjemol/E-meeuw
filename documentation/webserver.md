# Webserver
The HTTPs server will establish a secure TCP connection from the webserver to the browser. The webserver consists of the class `HTTP_Server()` from the file `mailserver.py` and other classes and methods from the file `server_lib.py`.

#

# Contents of `server_lib.py`
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
The class contains the method `build()` to compose the HTTP message.The message is created using a f-string, by parsing the `status`, `contentType` and `data` variables to a string containing a template for the message. We return the string.


## class Redirect()
In case we cannot reach a page, we want to redirect the user to another one. `Redirect()` returns a HTTP message similar to the one `response()` produces, but this message points to a page of our chosing. We use `Redirect()` to bring the user to the login page when necessary. 

An example of the HTTP message `redirect()` returns: 
```http
HTTP/1.1 301 Moved Permanently
Location: login/login.html
Cache-Control: no-store
```

### method Build()
`build()` returns a HTTP message. The message is created by parsing the `webpath` variable in a string containing a template for this message. In the template, the statuscode is already set to 301 and the cache-control is turned off, meaning browsers are not allowed to cache a response and must pull it from the server each time it's requested. This is necessary to keep the browser from passing over the original location indefinitely. 

## class Apiroute()
A class to format a HTTP response so it is able to connect to the api route.

### method Build()
The Python objects obtained when executing responseFunc are formatted to a JSON string by `json.dumps`.
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
A method that returns a JSON object decoded to be in the format of a Python object. We call the method `json.loads()` to change the format of the input. 


## class Route()
A class to build a HTTP response for the route. We pass the arguments `webpath`, `localpath`, `contentType` and `auth`, where `ContentType` defaults to "text/html" and `auth` defaults to False.
`Webpath` refers to the url and `localpath` refers to the path to the file locally. 

### method Build()
The class contains the method `build()`. `build()` will search the file the route is connected to. When we access the file, `build()` will build a HTTP response by calling the `Response.build()` method with status 200, the file and contentType. In case the HTML file is not found, the method will return a response with status 404 and the message 'Not found'.


## function NewRoute()
This function will append a new route to the list of routes created at the top of the file `server_lib.py`. 
We pass the arguments
- `webpath`, the url used in the browser
- `localpath`, the path of the file requested
- `contentType`, the contenttype of the request/file. This argument defaults to `"text/html"`.
- `auth`, defaults to `False`. This route is only visible when the user is logged in, `auth` then evaluates to `True`. 

We call the class `Route()` and append the object to our list `routes`. 


## function FindFiles()
This function will return a list of all the files in the folder specified as the argument of this function. In order to do this, we initialize the `glob()` method to retrieve the pathnames and add them to the list `files`. We then return the list `files`.


## function FindRoutes()
This function will compare the route and url to see if they match. When the route's `webpath` equals the `url` provided as argument, the method will return the route. In case the two do not match, we return the route to our errorpage.  


#
# Contents of `mailserver.py`

## class HTTP_Server 
This class combines the classes and methods from `server_lib.py` to a working HTTP server. We pass the arguments `self`, `address`, `port`, and `routes`.
- `address` refers to the domain name of the server
- `port` refers to the number of the port we want to use for the server
- `routes` refers to the list of all our webpages
Furtermore, the class contains the method `start()`

### method Start()
First, the method will print a string stating the address and port where the server will be starting. 

Next, the SSL connection is initiated. To do so, we create `context`, a `SSLContext` object with secure default settings for the given purpose. Here, `Purpose.CLIENT_AUTH` loads CA certificates for client certificate verification on the server side. 
The method `load_cert_chain()` loads an X.509 certificate and its private key into the SSLContext object. With `domainCert` and `privateCert`, we either refer to the certificates linked to our domain, e-meeuw, or certificates we created ourselves. Which one we use depends on whether we go live trough docker or not. The loaded certificate will be used during the SSL Handshake with the peer.

`Bindsocket` is an object `socket` using the `socket` module. We set the options related to a socket and assign an address and portnumber to the socket. 
`bindsocket.listen(1)` means the server is now listening for connection requests to its assigned port. `1` is the backlog argument of the method, this argument specifies the maximum number of queued connections.

### While loop
We enter the while loop where we handle the connections, we stay in this loop for as long as we run this program. 

When a connection request comes in from a client, we accept the connection using the method `accept()`. The method returns a tuple of a new instance of SSLSocket and the IP address of the client, we store them in the variables `newsocket` and `fromaddr`. 
Next, we add the SSL layer to our server socket `newsocket` with `context.wrap_socket()`, the secured socket is called `connstream`.
We store the data received by `connstream` in `request`, a bytes object. The maximum amount of data to be received is at once is set to `1024`. 

We format the request we got from the server socket with `Request()`, this returns the headers of the request as a string. We also print the IP address of the client and url of the request. 

We search for the `route` matching the url from the request with `FindRoute()`
We format a HTTP response for the request using `route.build()`.

If the `route.auth` equals true but we cannot find cookies or a user, we set the HTTP response to redirect to our login page. 

We convert `response` to bytes and send this information from the socket `connstream` to the connected remote socket. Finally, we close the `connstream` socket. 

## __main__
We start the servers.


#
To write this  documentation, I mostly used the documentation Python provides for the SSL module. 