# Program Steganografi LSB dengan Python

Ini adalah sebuah program steganografi sederhana yang ditulis dalam Python. Program ini memungkinkan Anda untuk menyembunyikan (encode) dan mengekstrak (decode) pesan rahasia atau bahkan file gambar lain di dalam sebuah gambar "pembawa" (*carrier*).

Metode yang digunakan adalah **LSB (Least Significant Bit)**, yaitu teknik memodifikasi bit yang paling tidak signifikan dari data piksel gambar untuk menyisipkan data rahasia. Perubahan ini sangat minim sehingga tidak dapat terdeteksi oleh mata manusia.

---

## Fitur

* **Encode Teks**: Menyembunyikan pesan teks ke dalam sebuah gambar.
* **Decode Teks**: Mengekstrak pesan teks dari sebuah gambar.
* **Encode Gambar**: Menyembunyikan sebuah file gambar (misal: `secret.jpg`) ke dalam gambar lain (`carrier.png`).
* **Decode Gambar**: Mengekstrak file gambar yang tersembunyi.

---

## Persyaratan

Untuk menjalankan program ini, Anda hanya memerlukan Python 3 dan library `Pillow`.

Anda dapat menginstal `Pillow` menggunakan pip:
```bash
pip install Pillow
```

## ⚙️ Cara Kerja Teknis

Program ini bekerja dengan memanipulasi nilai warna RGB (Red, Green, Blue) dari setiap piksel pada gambar pembawa.

### Konsep Dasar LSB (Least Significant Bit)
Setiap komponen warna (R, G, atau B) diwakili oleh angka 8-bit (0-255).
* Contoh: Nilai warna **210** dalam biner adalah `1101001`**`0`**.
* **LSB** adalah bit paling kanan (dalam contoh ini adalah `0`).

Dengan mengubah LSB ini, nilai desimal hanya berubah 1 (menjadi 211 atau `1101001`**`1`**). Perubahan sekecil ini tidak akan terlihat, tetapi kita bisa memanfaatkannya untuk menyimpan 1 bit data (`0` atau `1`).

### Proses Encoding (Menyembunyikan)

1.  **Konversi Data ke Biner**:
    * **Teks**: Setiap karakter diubah menjadi biner 8-bit. Sebuah *delimiter* (penanda akhir) seperti `_-_END_-_` ditambahkan ke akhir pesan untuk memberitahu program decode kapan harus berhenti.
    * **Gambar**: File gambar dibaca sebagai data *bytes* mentah. Ukuran file (misalnya, 25000 bytes) diubah menjadi biner 32-bit dan diletakkan di **awal** data. Ini berfungsi sebagai "header" yang memberitahu program decode berapa banyak data yang harus diekstrak.

2.  **Penyisipan Bit**:
    Program membaca gambar pembawa piksel per piksel. Untuk setiap piksel, terdapat 3 nilai warna (R, G, B), yang berarti kita bisa menyimpan 3 bit data per piksel.
    * Program mengambil bit dari data rahasia satu per satu.
    * LSB dari nilai R, G, B diganti dengan bit data rahasia tersebut.
    * Proses ini berlanjut hingga semua bit data rahasia berhasil disisipkan.

3.  **Penyimpanan**:
    Gambar yang pikselnya telah dimodifikasi disimpan sebagai file **baru**. Format **PNG** sangat disarankan karena bersifat *lossless* (tidak ada data yang hilang saat kompresi), sehingga data LSB yang kita sisipkan tetap aman.

### Proses Decoding (Mengekstrak)

1.  **Ekstraksi LSB**:
    Program membaca gambar yang berisi pesan rahasia piksel per piksel. Dari setiap nilai R, G, B, program hanya mengambil LSB-nya (`0` atau `1`).

2.  **Rekonstruksi Data**:
    * **Teks**: Bit-bit yang diekstrak dirangkai kembali. Setiap 8 bit diubah menjadi karakter. Program akan berhenti ketika menemukan *delimiter* `_-_END_-_`.
    * **Gambar**: Program pertama-tama mengekstrak **32 bit pertama** untuk mengetahui ukuran file yang tersembunyi. Setelah itu, program melanjutkan ekstraksi bit sebanyak ukuran yang didapat.

3.  **Penyimpanan Hasil**:
    * **Teks**: Pesan teks yang sudah direkonstruksi akan dicetak di terminal.
    * **Gambar**: Kumpulan *bytes* yang berhasil diekstrak akan ditulis menjadi sebuah file gambar baru.
