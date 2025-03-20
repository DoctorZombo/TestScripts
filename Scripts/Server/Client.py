import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
c = sock.send(input().encode())
data = sock.recv(1024)
sock.close()

print (data)