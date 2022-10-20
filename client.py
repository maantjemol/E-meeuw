import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("0.0.0.0", 8123))
sock.send(b"GET / HTTP/1.0\r\nHost: localhost\r\n\r\n")
response = sock.recv(4096)
sock.close()
print(response.decode())