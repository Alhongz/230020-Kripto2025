# Alur Program: Vigenère

## Fungsi utama
- encrypt(plaintext, key) — menghasilkan ciphertext.
- decrypt(ciphertext, key) — mengembalikan plaintext.

### Alur ketika program dijalankan
- Tampilkan judul "Vigenère Cipher (Interaktif)".
- Loop utama: minta user memilih mode encrypt, decrypt, atau exit.
- Minta kunci (key) — hanya huruf akan dipakai; huruf dikonversi ke uppercase.
- Jika mode encrypt — minta plaintext; jika decrypt — minta ciphertext.
- Buat keystream dengan mengulangi huruf kunci hanya untuk posisi huruf pada teks (karakter non-alfabet dilewati dan dikembalikan apa adanya).
- Untuk tiap karakter huruf, hitung pergeseran (A=0, B=1, ...). Jika enkripsi: (plain + offset) mod 26. Jika dekripsi: (cipher - offset) mod 26.
- Pertahankan kapitalisasi asli (huruf besar tetap besar, huruf kecil tetap kecil). Non-alfabet tetap tidak berubah.
- Tampilkan hasil, lalu kembali ke menu utama.

### Catatan implementasi
- Kunci dikendalikan oleh fungsi normalize_key yang menghapus karakter non-huruf.
- Keystream hanya di-generate untuk huruf, sehingga spasi dan tanda baca tetap pada posisinya.
