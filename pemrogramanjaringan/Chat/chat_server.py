"""Server untuk aplikasi chat multithread (asynchronous)."""

from socket import AF_INET, socket, SOCK_STREAM  # Import socket untuk komunikasi
from threading import Thread  # Import Thread untuk menangani banyak klien secara bersamaan

# Fungsi untuk menerima koneksi dari klien yang masuk
def accept_incoming_connections():
    """Mengatur penanganan untuk klien yang masuk."""
    try:
        while True:
            client, client_address = SERVER.accept()  # Menerima koneksi baru
            print("%s:%s connected." % client_address)
            client.send(bytes("Type your name and press enter!", "utf-8"))  # Instruksi awal ke klien
            addresses[client] = client_address  # Menyimpan alamat klien
            Thread(target=handle_client, args=(client,)).start()  # Membuat thread baru untuk klien
    except KeyboardInterrupt:
        #Menangani KeyboardInterrupt agar server bisa ditutup dengan Ctrl+C tanpa error
        print("\nServer shutting down manually.")


# Fungsi untuk menangani komunikasi dengan satu klien
def handle_client(client):  # Mengambil socket klien sebagai argumen.
    """Menangani koneksi klien tunggal."""

    name = client.recv(BUFSIZ).decode("utf-8")  # Menerima nama pengguna
    welcome = 'Welcome %s! If you want to leave, type {quit}.' % name
    client.send(bytes(welcome, "utf-8"))  # Mengirim pesan sambutan
    msg = "%s telah bergabung dengan chat!" % name
    broadcast(bytes(msg, "utf-8"))  # Menginformasikan semua klien
    clients[client] = name  # Menyimpan klien dengan nama

    while True:
        msg = client.recv(BUFSIZ)  # Menerima pesan dari klien
        if msg != bytes("{quit}", "utf-8"):
            broadcast(msg, name+": ")  # Kirim ke semua klien dengan prefix nama
        else:
            #Menangani error saat klien memutuskan koneksi secara tidak normal
            try:
                client.send(bytes("{quit}", "utf-8"))  # Coba kirim perintah keluar ke klien
            except (ConnectionResetError, OSError):
                print(f"[WARNING] Could not send quit message to {clients.get(client, 'Unknown')}")

            client.close()  # Tutup koneksi
            del clients[client]  # Hapus dari daftar klien
            broadcast(bytes("%s telah keluar dari chat." % name, "utf8"))  # Informasikan ke semua klien
            break


# Fungsi untuk mengirim pesan ke semua klien
def broadcast(msg, prefix=""):  # prefix untuk identifikasi nama.
    """Broadcasts pesan ke semua klien."""

    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf-8") + msg)  # Kirim pesan ke masing-masing klien
        except OSError:
            #Jika socket error, dilewati agar server tidak crash
            pass


# Dictionary untuk menyimpan klien aktif dan alamat mereka
clients = {}  # Menyimpan {socket: nama}
addresses = {}  # Menyimpan {socket: alamat}

# Konfigurasi alamat server
HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

# Membuat socket server dan binding ke alamat
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# Bagian utama yang dijalankan saat server diaktifkan
if __name__ == "__main__":
    SERVER.listen(5)  # Server mendengarkan sampai 5 koneksi antrian
    print("Menunggu koneksi...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Jalankan thread penerimaan koneksi
    ACCEPT_THREAD.join()  # Tunggu hingga thread selesai
    SERVER.close()  # Tutup server saat selesai
