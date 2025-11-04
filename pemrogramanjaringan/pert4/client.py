import socket

HOST = '127.0.0.1'
PORT = 5555

sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))

while True:
    message = input("Message: ")
    sock.send(message.encode('utf-8'))

    reply = sock.recv(1024).decode('utf-8')
    print(f"Received: {reply}")