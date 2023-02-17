import socket
import threading

MAX_CLIENTS = 5
PORT = 5555

clients = [1,2,3]
next_rank = 0

def handle_client(client_socket, address):
    global clients
    global next_rank

    rank = next_rank
    next_rank += 1

    clients.append((client_socket, address, rank))

    print(f"New connection from {address}, assigned rank {rank}")

    while True:
        command = client_socket.recv(1024).decode()

        if not command:
            clients.remove((client_socket, address, rank))
            client_socket.close()

            for i, (client, _, client_rank) in enumerate(clients):
                if client_rank > rank:
                    clients[i] = (client, address, client_rank - 1)

            print(f"{address} disconnected, reassigned ranks")

            return

        for client, _, client_rank in clients:
            if client_rank == rank - 1:
                client.send(command.encode())
                break
        else:
            print(f"Error: {address} tried to execute a command they don't have the rank for")

def start_server():
    global clients

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(MAX_CLIENTS)

    while True:
        client_socket, address = server_socket.accept()

        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == '__main__':
    start_server()