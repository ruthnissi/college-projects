import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # kirim 4096 byte setiap waktu

# alamat ip atau nama host server, penerima
host = "127.0.0.1"
# port, yang di gunakan 5001
port = 5001
# nama file yang ingin kita kirim, pastikan ada
filename = "introduction.txt"
# mendapatkan ukuran file
filesize = os.path.getsize(filename)

# buat socket klien
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# kirim nama file dan ukuran file
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# mulai mengirim file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # baca byte dari file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # pengiriman file selesai
            break
        # menggunakan sendall untuk memastikan transmisi data masuk
        s.sendall(bytes_read)
        # update progress bar
        progress.update(len(bytes_read))
# close socket
s.close()