import sys
import socket

SEND_BUFFER_SIZE = 2048

def client(server_ip, server_port):
    """TODO: Open socket and send message from sys.stdin"""
    #socket creation
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #socket connection
    sock.connect((server_ip, server_port))

    #continously reads 2048 bytes chunks of data from stdin and sends to the server using sendall to prevent partial sends until no data is left to read
    #then the socket is closed
    input_data = sys.stdin.buffer.read(SEND_BUFFER_SIZE)
    while input_data:
        sock.sendall(input_data)
        input_data = sys.stdin.buffer.read(SEND_BUFFER_SIZE)
    sock.close()


def main():
    """Parse command-line arguments and call client function """
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 client-python.py [Server IP] [Server Port] < [message]")
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    client(server_ip, server_port)

if __name__ == "__main__":
    main()