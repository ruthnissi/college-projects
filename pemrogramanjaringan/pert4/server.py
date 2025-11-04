import socket 

HOST = '127.0.0.1'
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))

sock.listen()

client, address = sock.accept()

while True:
    message = client.recv(1024).decode('utf-8')
    print(f"Received from {address} : {message}")

    reply = input("Reply: ")
    client.send(reply.encode('utf-8'))