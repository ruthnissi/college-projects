"""Script Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import random  #Menambahkan modul random untuk pemilihan warna secara acak

nickname_colors = {} #Dictionary untuk menyimpan warna unik tiap nickname
color_options = ["red", "blue", "green", "purple", "orange", "magenta", "cyan", "gold", "brown", "pink"]


# Fungsi untuk menerima pesan dari server
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf-8")
            msg_list.config(state="normal") #Mengaktifkan text widget agar dapat dimodifikasi
            if ":" in msg: # Memisahkan nama dan isi pesan berdasarkan tanda ":"
                name, content = msg.split(":", 1)
                name = name.strip()
                if name not in nickname_colors:
                    color = random.choice(color_options) #Pilih warna acak untuk nickname baru
                    nickname_colors[name] = color
                    msg_list.tag_config("name_" + name, foreground=color)  #Atur warna teks berdasarkan nickname
                msg_list.insert(tkinter.END, name + ":", "name_" + name)  #Masukkan nama dengan warna
                msg_list.insert(tkinter.END, content.strip() + "\n")  #Masukkan isi pesan
            else:
                msg_list.insert(tkinter.END, msg + "\n")  #Untuk pesan sistem (tanpa nama pengirim)
            msg_list.config(state="disabled")  #Kunci kembali text widget setelah dimodifikasi
            msg_list.see(tkinter.END)
        except OSError:  # Memungkinkan klien untuk meninggalkan chat.
            break


# Fungsi untuk mengirim pesan ke server
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")  # Membersihkan input field.
    client_socket.send(bytes(msg, "utf-8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


# Fungsi untuk menangani event ketika window ditutup
def on_closing(event=None):
    my_msg.set("{quit}")
    send()

def clear_chat():
    msg_list.config(state="normal")
    msg_list.delete(1.0, tkinter.END)
    msg_list.config(state="disabled")

# Membuat jendela utama aplikasi
top = tkinter.Tk()
top.title("DiskWord")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # Untuk pesan yang akan dikirim.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # Untuk menavigasi melalui pesan sebelumnya.

# Berikut akan berisi pesan.
# Komponen GUI dengan penyesuaian warna latar belakang dan warna teks:
msg_list = tkinter.Text(
    messages_frame, 
    height=15, 
    width=50, 
    yscrollcommand=scrollbar.set, 
    state="disabled",  #Text tidak bisa diubah langsung oleh pengguna
    bg="black",        #Latar belakang hitam
    fg="#FF69B4"       #Warna teks default (pink)
)

# Menempatkan komponen GUI ke dalam frame
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

# Input field dan tombol kirim
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send) # Kirim saat menekan Enter
entry_field.pack()

# Tambahkan frame untuk tombol
button_frame = tkinter.Frame(top)
button_frame.pack()

# Tombol Send di sisi kiri
send_button = tkinter.Button(button_frame, text="Send", command=send)
send_button.pack(side=tkinter.LEFT, padx=5)

# Tombol Clear di sisi kanan dari frame
clear_button = tkinter.Button(button_frame, text="Clear", command=clear_chat)
clear_button.pack(side=tkinter.LEFT, padx=5)

# Tangani aksi ketika jendela ditutup
top.protocol("WM_DELETE_WINDOW", on_closing)


#----Sekarang pada bagian sockets----
# Input host dan port untuk koneksi
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

# Ukuran buffer dan alamat tujuan
BUFSIZ = 1024
ADDR = (HOST, PORT)

# Membuat socket dan menghubungkan ke server
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# Thread untuk menerima pesan dari server
receive_thread = Thread(target=receive)
receive_thread.start()

tkinter.mainloop()  # Starts GUI execution.