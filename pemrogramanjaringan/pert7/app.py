import random
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tebak', methods=['POST'])
def tebak():
    tebakan = int(request.form['tebakan'])
    angka = random.randint(1, 100)

    if tebakan == angka:
        pesan = "Selamat! Anda berhasil menebak angka {}.".format(angka)
    elif tebakan < angka:
        pesan = "Tebakan Anda terlalu rendah."
    else:
        pesan = "Tebakan Anda terlalu tinggi."

    return render_template('hasil.html', pesan=pesan)

if __name__ == '__main__':
    app.run(debug=True)