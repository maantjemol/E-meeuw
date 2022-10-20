import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/Users/maantje/programmeren/Uni/Python/EoCS/cert/localhost.crt', '/Users/maantje/programmeren/Uni/Python/EoCS/cert/localhost.key')

class Response():
    def __init__(self, status:int, data:str):
        self.status = status
        self.data = data

    def build(self):
        response = f"HTTP/1.0 {self.status} OK\n\r{self.data}"
        return response


def unpack_request(request):
    print(request)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('0.0.0.0', 8443))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        client_connection, client_address = ssock.accept()

        request = client_connection.recv(1024).decode()
        unpack_request(request)
        response = Response(200, "<h1>Hi, welcome to my site</h1>").build()

        # Send HTTP response
        client_connection.sendall(response.encode())
        client_connection.close()