### Method getSSLSocket()

The SSL wrapper for socket objects is a module that provides acces to Transport Layer Security. ("Secure Sockets Layer").

### Method getEmailUid()

This method reads the existing database in json and converts it into a Python Dictionary.
It then checks if the used email corresponds with an existing one in the database.

### Method sendEmail()

This method will try to encrypt your email and send it out. It will do so by first connecting to the allocated socket. If the socket is found the response will be set.
The function will proceed to try and connect to the server and encrypt your username, data and message.

### Method acceptEmail()

This method tries to recieve the e-mail. It tries to recognize if the sent mail is sent by the correct user and will start decoding the message. After the message has been scanned it will print the decoded message.

## Class Email_server()

A class that sets up the e-mail server and opens up connections that e-mails can be sent through. It sets up the certificates and connects the HTTPS socket.
If information is passing, through the TCP connection will be established and e-mails will be able to get recieved.

### Method ApiRoutes()

A method that directs all the routes to a selection of routes that have been programmed.

### Method NewRoute()

A method that uses different paramaters to create a new route in the existing array of routes.

### Method InitializeRoutes()

A method that starts up all the routes in and make sure all the javascript and underlying css is working propperly

## Class HTTP_Server()

A class that runs the HTTP server by connecting all the ports and routes with eachother.
