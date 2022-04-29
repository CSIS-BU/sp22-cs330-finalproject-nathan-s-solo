import socket
import threading

BUFFER_SIZE = 2048
QUEUE_LENGTH = 10

players = []
server_port = input("Enter port number: ")
server_port = int(server_port)
host = ""
thread_counter = 0

    #socket creation
server_id = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #socket binding
server_id.bind((host, server_port))

    #socket listening
server_id.listen(QUEUE_LENGTH)


def  handle_client(conn, addr, t_counter):
    while True:
        data = conn.recv(BUFFER_SIZE).decode()
        print(data)
        if data:
            if data == "GAMEOVER":
                players.clear()
                conn.close()
                return
            else:
                players[(1+t_counter)%2].sendall(data.encode())
        elif not data:
            print(players)
            players.clear()
            conn.close()
            return

#loop that accepts connections and adds the socket connection to a list if there are less then 2 already in the list. then creates a thread so multiple clients can connect simultaneously
while True:
        conn, addr = server_id.accept()
        if len(players)<3:
            players.append(conn)
            print(len(players))
            if len(players)==2:
                for i in range(len(players)):
                    players[i].send(str(i).encode())
        thread = threading.Thread(target=handle_client, args=(conn, addr, thread_counter))
        thread.daemon = True
        thread.start()
        thread_counter += 1
        print('Thread Count: ' + str(thread_counter))
        print("Active Connections: ", (threading.active_count() - 1))
server_id.close()
