import socket, ssl

#Hallo ik ben Manuel!

class Response():
    def __init__(self, status:int, data:str):
        self.status = status
        self.data = data

    def build(self):
        response = f"HTTP/1.1 {self.status} OK\nServer: Your_Mom\nContent-type: text/html; charset=UTF-8\n\r\n\r{self.data}\n\r\n\r"
        return response


class Request():
    def __init__(self, request:bytes):
        self.headers = {}
        self.request_string = request.decode()
        self.method = self.request_string.split(" ")[0]
        self.url = self.request_string.split(" ")[1]

        print("Request: \n", self.request_string)

        # split header string and add it to dict
        lines = self.request_string.split('\n',1)[1]
        for line in lines.split("\n")[0:-2]:
            # print(line)
            words = line.split(":", 1)
            self.headers[words[0]] = words[1].replace("\n", "").replace("\r", "")



def HTTPS_server(address:str, port:int):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('/Users/maantje/programmeren/Uni/Python/EoCS/cert/server.crt', '/Users/maantje/programmeren/Uni/Python/EoCS/cert/server.key')

    bindsocket = socket.socket()
    bindsocket.bind((address, port))
    bindsocket.listen(1)

    while True:
        newsocket, fromaddr = bindsocket.accept()
        print("Accepting request!")
        connstream = context.wrap_socket(newsocket, server_side=True)
        request = connstream.recv(1024)

        request = Request(request)


        response = Response(200, "<h1>Hi, welcome to my site</h1>").build()
        print("Response: \n", response)
        connstream.sendall(response.encode())
        connstream.close()


if __name__ == "__main__":
    HTTPS_server("localhost", 1112)
