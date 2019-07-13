import socket, sys, connect4logic


def enterDetails():
    address = input("Enter server address: ")
    port = input("Enter port: ")
    while not port.isdigit():
        port = input("Enter a valid port: ")
    port = int(port)
    roomName = input("Enter room name: ")
    return address, port, roomName


def connector(address, port, roomName):
    """Creates connection between client and server"""
    try:
        print("Connecting...")
        sock = socket.socket()
        sock.connect((address, port))
        sock.sendall(roomName.encode())
        sock.settimeout(10)
        print("Connected.")
        return sock
    except socket.timeout:
        input("Connection failed")
        sys.exit()


def waitForStart(sock):
    """Wait for message from server saying 'started', indicated game starting, print all recieved"""
    exit = False
    while not exit:
        try:
            message = sock.recv(4096)
            messageDecoded = message.decode()
            if messageDecoded.lower() == "start":
                exit = True
            else:
                print(messageDecoded)
        except socket.timeout:
            continue
        except ConnectionResetError:
            input("Connection closed, press enter to end")
            sys.exit()
    start()


def start():
    print("Launch game")


address, port, roomName = enterDetails()
sock = connector(address, port, roomName)
waitForStart(sock)