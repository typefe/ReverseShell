import imp
import queue
import socket
import sys
import threading
import time
from queue import Queue


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
connections = []
addresses = []


# Creating a socket for connecting two computers.
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as sem:
        print("Socket could not be created. Error Message: {}".format(sem))


# Binding the socket and listening for incoming connections.
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port {}".format(str(port)))

        s.bind((host, port))
        s.listen(5)

    except socket.error as sem:
        print("Socket could not be binded. Error Message: {}".format(sem))
        bind_socket()


# Handling and saving multiple connections.
# Closing previous connections when server.py file is restarted.
def accept_connection():

    for c in connections:
        c.close()

    del connections[:]
    del addresses[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # Prevents timeout

            connections.append(conn)
            addresses.append(address)

            print("Connection has been established: ".format(address[0]))

        except:
            print("Error connection could not established.")
