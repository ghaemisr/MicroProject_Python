import socket
UDP_IP = "0.0.0.0"


def receive(port, status):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
    if status == "Receive":
        sock.bind((UDP_IP, port))
        data, address = sock.recvfrom(1024)
        return data
    elif status == "Stop":
        # sock.shutdown(socket.SHUT_WR)
        sock.close()
    # while True:
    #     data, address = sock.recvfrom(1024)  # buffer size is 1024 bytes
    #     print("received message:", data)
