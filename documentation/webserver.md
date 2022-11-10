# Webserver

The HTTPs server will establish a secure TCP connection from the webserver to the browser.  

## class Response()
A Class to compose the HTTP message. 
We pass the arguments `status` and `data`, where in our case `data` refers to our webpages. 
The class contains the method `build()`.
`Build()` returns the HTTP message, the message is created using a f-string, parsing the status and data variables. 

## class Request()
A Class to format the request. 
We pass the argument `request` of type bytes. 
Furthermore, the class contains the following object properties:
- `request_string`, where the bytes from the `request` argument are translated to a string. 
- `method`, the first word of the `request_string`
- `url`, the second word of the `request_string`
- `headers`, a dictionary object. 


For example, the following `request_string`: 
```http
GET /search.html HTTP/1.1
Host: www.google.com
User-Agent: Mozilla/5.
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
