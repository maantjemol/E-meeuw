import socket
import ssl

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8123
test = f"dsfg{SERVER_HOST}"
# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = ssl.wrap_socket (server_socket, certfile='./server.pem', server_side=True)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)


class Response():
    def __init__(self, status:int, data:str):
        self.status = status
        self.data = data

    def build(self):
        response = f"HTTP/1.0 {self.status} OK\n\r{self.data}"
        return response


def unpack_request(request):
    print(request)

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    unpack_request(request)
    response = Response(200, "<h1>Hi, welcome to my site</h1>").build()

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
