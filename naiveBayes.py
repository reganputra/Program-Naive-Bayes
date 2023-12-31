import pandas as pd
import numpy as np
from tabulate import tabulate
import tkinter as tk
from tkinter import StringVar, Radiobutton, Button, OptionMenu
from ttkthemes import ThemedStyle

# Membaca file excel
path = r"C:\Kuliah\Semester 3\Statistika Komputasi\Tugas\coba.xlsx"
data = pd.read_excel(path)

data = data[['Work', 'Usia', 'Status', 'Penghasilan',
             'Kendaraan', 'Kepemilikan', 'Atap Bangunan', 'Keterangan']]
print(data.head(10))

train_layak = data[data['Keterangan'] == 'Layak']
train_tidak_layak = data[data['Keterangan'] == 'Tidak Layak']

# kategori
pekerjaan_kategori = ['Wirasswasta', 'Tidak Bekerja']
usia_kategori = ['20-29', '30-40']
status_perkawinan_kategori = ['Kawin', 'Belum Kawin']
penghasilan_kategori = ['2000000-3000000', 'diatas 5000000', '≤1000000']
kendaraan_kategori = ['Motor', 'Mobil', 'Angkutan Umum']
kepemilikan_kategori = ['Orang Tua', 'Menyewa', 'Pribadi']
atap_bangunan_kategori = ['Asbes', 'Genteng']

atribut_list = ['Work', 'Usia', 'Status', 'Penghasilan',
                'Kendaraan', 'Kepemilikan', 'Atap Bangunan']

# Menghitung Probabilitas setiap
def hitung_probabilitas_atribut(data, atribut, keterangan, kategori):
    prob_atribut = {}
    for k in kategori:
        for h in keterangan.unique():
            data_kategori = data[(data[atribut.name] == k)
                                 & (data['Keterangan'] == h)]
            prob_atribut[f'{k} - {h}'] = data_kategori.shape[0] / \
                data[data['Keterangan'] == h].shape[0]
    return prob_atribut

def naive_bayes(data, atribut_list, kategori_list):
    hasil_prob = {}
    for atribut, kategori in zip(atribut_list, kategori_list):
        prob_atribut = hitung_probabilitas_atribut(
            data, data[atribut], data['Keterangan'], kategori)
        hasil_prob[atribut] = prob_atribut
    return hasil_prob

# call function hitung probabilitas
hasil_prob = naive_bayes(data, atribut_list, [
                         pekerjaan_kategori, usia_kategori, status_perkawinan_kategori,
                         penghasilan_kategori, kendaraan_kategori, kepemilikan_kategori,
                         atap_bangunan_kategori])

# Show table
def display_sorted_table(atribut, hasil_prob):
    sorted_items = sorted(
        hasil_prob[atribut].items(), key=lambda x: x[0].split()[0])
    print(f"Probabilitas {atribut}:")
    print(tabulate(pd.DataFrame(sorted_items, columns=[
          'Kategori', 'Probabilitas']), headers='keys', tablefmt='pipe', showindex=False))
    print("\n")

for atribut in atribut_list:
    display_sorted_table(atribut, hasil_prob)

def naive_bayes_predict(data_test, hasil_prob, atribut_list):
    predictions = []

    for _, row in data_test.iterrows():
        layak_prob = 1
        tidak_layak_prob = 1

        for atribut in atribut_list:
            value = row[atribut]
            layak_prob *= hasil_prob[atribut].get(f'{value} - Layak', 0)
            tidak_layak_prob *= hasil_prob[atribut].get(
                f'{value} - Tidak Layak', 0)

        layak_prob *= len(train_layak) / len(data)
        tidak_layak_prob *= len(train_tidak_layak) / len(data)

        # Memilih kelas dengan probabilitas tertinggi
        prediction = 'Layak' if layak_prob > tidak_layak_prob else 'Tidak Layak'
        predictions.append(prediction)

    return predictions

# Contoh penggunaan
def get_user_input():
    user_input = {}
    input_frame = tk.Frame(root, padx=10, pady=10)
    input_frame.pack()

    for atribut in atribut_list:
        var = StringVar()

        # Membuat GUI untuk dropdown menu
        frame = tk.Frame(input_frame)
        frame.pack(side=tk.LEFT, padx=10)

        tk.Label(frame, text=f"{atribut}:").pack()

        style = ThemedStyle(frame)
        style.set_theme("winnative")

        # Membuat dropdown menu
        options = data[atribut].unique()
        dropdown = tk.OptionMenu(frame, var, *options)
        dropdown.pack(anchor=tk.W)

        user_input[atribut] = var

    return user_input

def predict_naive_bayes():
    user_input = {atribut: var.get() for atribut, var in user_input_vars.items()}
    data_test = pd.DataFrame(user_input, index=[0])

    predictions = naive_bayes_predict(data_test, hasil_prob, atribut_list)

    # Displaying the prediction
    result_label.config(text=f'Hasil Prediksi: {predictions[0]}')

    # Calculating probabilities
    layak_prob = 1
    tidak_layak_prob = 1

    for atribut in atribut_list:
        value = user_input[atribut]
        layak_prob *= hasil_prob[atribut].get(f'{value} - Layak', 0)
        tidak_layak_prob *= hasil_prob[atribut].get(f'{value} - Tidak Layak', 0)

    layak_prob *= len(train_layak) / len(data)
    tidak_layak_prob *= len(train_tidak_layak) / len(data)

    # Menampilkan probabilitas prediksi
    prob_label.config(text=f'Probabilitas Layak: {layak_prob:.4f}\nProbabilitas Tidak Layak: {tidak_layak_prob:.4f}')

root = tk.Tk()
root.title("Prediksi Naive Bayes")

# Membuat input pengguna dengan radio button
user_input_vars = get_user_input()

# Membuat tombol untuk melakukan prediksi
predict_button = Button(root, text="Prediksi", command=predict_naive_bayes)
predict_button.pack()

# Membuat label untuk menampilkan hasil prediksi
result_label = tk.Label(root, text="")
result_label.pack()

prob_label = tk.Label(root, text="")
prob_label.pack()

root.mainloop()
