import socket,pickle
import threading

HOST = '127.0.0.1'
PORT = 11000

class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return self.firstname + " " + self.lastname


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(HOST, PORT))

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    p = pickle.loads(request)
    print('Received ' + p.__str__())
    client_socket.send(pickle.dumps(p))
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()