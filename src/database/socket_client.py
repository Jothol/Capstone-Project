import socket
import sys
import threading
from threading import Thread

from kivy.clock import Clock

HEADER_LENGTH = 10


class ListenChat():

    def __init__(self):
        self.incoming_message_callback = None
        self.error_callback = None
        self.session_name = None
        self.listen_event = None
        self.client_socket = None

    # Connects to the server
    def connect(self, ip, port, my_username, error_callback, session_name=None):

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to a given ip and port
            self.client_socket.connect((ip, port))
        except Exception as e:
            # Connection error
            error_callback('Connection error: {}'.format(str(e)))
            return False

        # Prepare username and header and send them
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username = (my_username + "-" + session_name).encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(username_header + username)

        return True

    # Sends a message to the server
    def send(self, message):
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.strip()
        print(message)
        if message is not None:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(message_header + message)

    # Starts listening function in a thread
    # incoming_message_callback - callback to be called when new message arrives
    # error_callback - callback to be called on error

    def start_listening(self, incoming_message_callback, error_callback, session_name=None):
        self.incoming_message_callback = incoming_message_callback
        self.error_callback = error_callback
        self.session_name = session_name
        threading.Thread(target=self.step1(), daemon=True)


    def step1(self):
        self.listen_event = Clock.schedule_interval(self.listen_message, 0.1)

    # Listens for incomming messages
    def listen_message(self, dt):
        try:
            # Now we want to loop over received messages (there might be more than one) and print them

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = self.client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                self.error_callback('Connection closed by the server')

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = self.client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = self.client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = self.client_socket.recv(message_length).decode('utf-8')

            if self.session_name is not None:
                if username.split('-')[1] == self.session_name:
                    self.incoming_message_callback(username.split('-')[0], message)
            else:
                self.incoming_message_callback(username, message)
            # Print message


        except Exception as e:
            # Any other exception - something happened, exit
            print(e)
            self.error_callback('Reading error: {}'.format(str(e)))

    def cancel_message(self):
        self.client_socket.close()
        Clock.unschedule(self.listen_message)
