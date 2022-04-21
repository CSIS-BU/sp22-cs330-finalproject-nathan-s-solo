import sys
import socket

RECV_BUFFER_SIZE = 2048
QUEUE_LENGTH = 10

def server(server_port):
    """TODO: Listen on socket and print received message to sys.stdout"""
    #socket creation
    server_id = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #socket binding
    server_id.bind(('', server_port))

    #socket listening
    server_id.listen(QUEUE_LENGTH)
    sys.stdout.flush()

    #while loop that continously loops while the server waits for a client socket connection and when a connection is accepted
    #data is continously received in 2048 byte chunks and written to stdout until no more data is received and then the client socket is closed
    while True:
        (client_socket, ip) = server_id.accept()
        msg = client_socket.recv(RECV_BUFFER_SIZE)
        while msg:
            sys.stdout.buffer.write(msg)
            sys.stdout.flush()
            msg = client_socket.recv(RECV_BUFFER_SIZE)
        client_socket.close()


def main():
    """Parse command-line argument and call server function """
    if len(sys.argv) != 2:
        sys.exit("Usage: python server-python.py [Server Port]")
    server_port = int(sys.argv[1])
    server(server_port)

if __name__ == "__main__":
    main()
