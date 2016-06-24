import socket
UDP_IP = "0.0.0.0"


def receive(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
    sock.bind((UDP_IP, port))

    while True:
        data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
