import sys, os
import pygame
import socket
import threading

BUFFER_SIZE = 2048
QUEUE_LENGTH = 10

players = []
grid = [[0 for x in range(3)] for y in range(3)]
# server_port = input("Enter port number: ")
# server_port = int(server_port)
server_port = 6728
host = ""
thread_counter = 0

    #socket creation
server_id = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #socket binding
server_id.bind((host, server_port))

    #socket listening
server_id.listen(QUEUE_LENGTH)


def  handle_client(conn, addr, ID):
    while True:
        data = conn.recv(BUFFER_SIZE)
        print(data.decode())
        if data:
            players[(1+ID)%2].sendall(data)
    conn.close()

while True:
        conn, addr = server_id.accept()
        print('Connected to: ' + addr[0] + ':' + str(addr[1]))
        if len(players)<3:
            players.append(conn)
            if len(players)==2:
                for i in range(len(players)):
                    players[i].send(str(i).encode())
        thread = threading.Thread(target=handle_client, args=(conn, addr, thread_counter))
        thread.daemon = True
        thread.start()
        thread_counter += 1
        print('Thread Number: ' + str(thread_counter))
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
server_id.close()
# create_thread(waiting_for_connection)

# def start_server(server_port):

#     sys.stdout.flush()

#     #while loop that continously loops while the server waits for a client socket connection and when a connection is accepted
#     #data is continously received in 2048 byte chunks and written to stdout until no more data is received and then the client socket is closed
#     while True:
#         (client_socket, ip) = server_id.accept()
#         msg = client_socket.recv(RECV_BUFFER_SIZE)
#         while msg:
#             sys.stdout.buffer.write(msg)
#             sys.stdout.flush()
#             msg = client_socket.recv(RECV_BUFFER_SIZE)
#         client_socket.close()


# def main():
#     """Parse command-line argument and call server function """
#     if len(sys.argv) != 2:
#         sys.exit("Usage: python server-python.py [Server Port]")
#     server_port = int(sys.argv[1])
#     start_server(server_port)

# if __name__ == "__main__":
#     main()
