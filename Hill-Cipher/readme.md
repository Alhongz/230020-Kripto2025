# Hill Cipher — README

## Identitas

### Nama  : Alfarisy Nafaro Gymnastiar
### NPM   : 140810230020

## Ringkasan singkat

Program ini mengimplementasikan Hill Cipher ukuran n x n (mis. 2×2, 3×3). Saya bisa memasukkan
plaintext/ciphertext lewat terminal, memasukkan matriks kunci sendiri (baris per baris), lalu memilih pilihan menu:
encrypt / decrypt / recover key. Teks non-alfabet akan dihapus, huruf otomatis diubah ke UPPERCASE, dan padding x
ditambahkan bila perlu

## Alur Program

1. Tampilan Menu Awal
  - <img width="488" height="134" alt="image" src="https://github.com/user-attachments/assets/1cf0b72e-8eb6-4c01-9e5a-c6ace2b691c1" />
  - User disajikan pilihan untuk enkripsi dekripsi recovery key dan keluar
2. Menu Enkripsi
  - <img width="705" height="231" alt="image" src="https://github.com/user-attachments/assets/20688360-5e13-419f-a3a9-39edfc1d60f6" />
  - User diminta untuk memasukan plainteks yang akan di enkrip dan nantinya user diminta untuk memilih dimensi untuk matriks dan mengisi matriksnya
3. Menu Dekripsi
  - <img width="670" height="219" alt="image" src="https://github.com/user-attachments/assets/08d4065a-3bb1-4d5f-b3ef-7130a8c65a2b" />
  - User diminta untuk memasukan chiperteks yang akan di dekrip dan juga kuncinya
4. Menu Recover Key
  - <img width="462" height="216" alt="image" src="https://github.com/user-attachments/assets/fc301da5-7570-44e3-b4ea-fadc8e0d5e42" />
  - User diminta untuk memasukan plainteks dan chiperteks yang sesuai



## Penjelasan singkat cara kerja (konsep)

- Teks → angka: A→0 .. Z→25.
- Bagi plaintext menjadi blok panjang n; bila kurang, pad dengan X (23).
- Enkripsi setiap blok: C = K * P (mod 26) (K matriks kunci n×n, P kolom n×1).
- Dekripsi: hitung K^{-1} (mod 26), lalu P = K^{-1} * C (mod 26).
- Recover key (known-plaintext): jika tersedia n blok plaintext & ciphertext yang membentuk matriks P (invertible), maka K = C * P^{-1} (mod 26).

## Troubleshooting

- Error: determinan tidak invertible / gagal dekripsi → periksa kembali kunci; pastikan gcd(det,26) == 1.
- Recover key gagal → pastikan pasangan plaintext↔ciphertext cukup panjang (≥ n*n) dan pilih window yang menghasilkan P invertible; jika masih gagal, coba pasangan berbeda.
- Masalah input angka → masukkan angka integer saja, pisahkan dengan spasi. Program memodulo 26 otomatis.


