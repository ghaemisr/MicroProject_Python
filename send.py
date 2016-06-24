import socket

UDP_PORT = 7000
MESSAGE = "Salam Jigare man!!"

print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(MESSAGE.encode(), ('<broadcast>', UDP_PORT))
