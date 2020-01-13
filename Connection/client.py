import socket, pickle

HOST = '127.0.0.1'
PORT = 11000

class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return self.firstname + " " + self.lastname


# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect((HOST, PORT))

# send some data (in this case a HTTP GET request)
client.send(pickle.dumps(Person('Aleksandar', 'Novakovic'))) #Return the pickled representation of the object as a string, instead of writing it to a file

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)

print(pickle.loads(response).__str__()) #Read a pickled object hierarchy from a string.