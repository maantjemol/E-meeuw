# Webserver

The HTTPs server will establish a secure TCP connection from the webserver to the browser.  

## class Response()
A Class to compose the HTTP message. 
We pass the arguments `status` and `data`, where in our case `data` refers to our webpages. 
The class contains the method `build()`.
`build()` returns the HTTP message, the message is created using a f-string, parsing the status and data variables. 

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

## class Route()
A class to compose the route. 
We pass the arguments `webpath` and `localpath`.
The class contains the method `build()`.
`build()` will try to find the HTML file, specified in the `localpath` variable, in the folder `pages`. When it does, `build()` will build a HTTP response using the `Response.build()` method with status 200 and the file. In case the HTML file is not found, the method will return a response with status 404 and the message 'Not found'.
Furthermore, the class contains the following methods:

### method NewRoute()
This method will append a new route to a list of routes. 
The route is created inside the method, using the parameters `webpath` and `localpath`, and then added to the list `routes`.

### method InitializeRoutes()
This method will go through all the files in the folder `pages` and initialize the method `NewRoute()` to map the routes to all pages. All routes are then added to the list `routes`. 

### method FindFiles()
This method will return a list of all the files in a folder. 
In order to do this, we initialize the `glob()` method to retrieve the pathnames and add them to the list `files`.


## class HTTP_Server
This class .... We pass the arguments `self`, `address`, `port`, and `routes`.
Furtermore, the class contains the method `start()`

### method Start()
The method will print a string stating the address and port where the server will be starting. 
Next, the SSL connection is initiated. We create a `SSLContext` object. 


