import socket
import tqdm
import os
# device IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
# menerima 4096 byte setiap kali
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# membuat socket server
# TCP socket
s = socket.socket()

# mengikat socket ke alamat lokal
s.bind((SERVER_HOST, SERVER_PORT))

# memungkinkan server menerima koneksi
# 5 di sini adalah jumlah koneksi yang tidak diterima
# sistem akan mengizinkan sebelum menolak koneksi baru
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# terima koneksi jika ada
client_socket, address = s.accept() 
# jika kode di bawah ini dijalankan, itu berarti pengirim terhubung
print(f"[+] {address} is connected.")

# terima info file
# terima menggunakan socket klien, bukan socket server
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# hapus jalur absolut jika ada
filename = os.path.basename(filename)
# convert ke integer
filesize = int(filesize)

# mulai menerima file dari soket
# dan menulis ke aliran file
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # membaca 1024 byte dari soket (menerima)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # tidak ada yang diterima
            # pengiriman file selesai
            break
        # tulis ke file byte yang baru saja di terima
        f.write(bytes_read)
        # update progress bar
        progress.update(len(bytes_read))

# close client socket
client_socket.close()
# close server socket
s.close()