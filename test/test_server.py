import unittest
import socket
import threading
import time

from ..server import Server

# import Server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server(max_clients=2)
        self.server_thread = threading.Thread(target=self.server.run)
        self.server_thread.start()
        time.sleep(0.1)  # wait for the server to start

    def tearDown(self):
        self.server.server_socket.close()
        self.server_thread.join()

    def test_client_connection(self):
        # create a client socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8000))
        # wait for the server to accept the connection
        time.sleep(0.1)
        # check that a client was added to the server's list of clients
        self.assertEqual(len(self.server.clients), 1)

    def test_max_clients_reached(self):
        # create two client sockets and connect to the server
        client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket1.connect(('localhost', 8000))
        client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket2.connect(('localhost', 8000))
        # wait for the server to accept the connections
        time.sleep(0.1)
        # check that both clients were added to the server's list of clients
        self.assertEqual(len(self.server.clients), 2)
        # create a third client socket and connect to the server
        client_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket3.connect(('localhost', 8000))
        # wait for the server to reject the connection
        time.sleep(0.1)
        # check that the third client was not added to the server's list of clients
        self.assertEqual(len(self.server.clients), 2)

    def test_client_leave(self):
        # create a client socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8000))
        # wait for the server to accept the connection
        time.sleep(0.1)
        # check that a client was added to the server's list of clients
        self.assertEqual(len(self.server.clients), 1)
        # close the client socket
        client_socket.close()
        # wait for the server to remove the client
        time.sleep(0.1)
        # check that the client was removed from the server's list of clients
        self.assertEqual(len(self.server.clients), 0)

    if __name__ == '_main_':
        unittest.main()