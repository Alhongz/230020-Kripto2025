# Alur Program ElGamal

## Fungsi Utama
- Mode encrypt: Menerima p, g, x, k dan plaintext (A-Z), menampilkan pasangan (a,b) per huruf.
- Mode decrypt: Menerima p, x dan satu atau lebih pasangan (a,b); mengembalikan m dan (jika 0..25) huruf yang cocok.

### Alur mode ENCRYPT
- Minta input p (periksa prima), g, x (private key), k (nonce), dan plaintext.
- Konversi plaintext ke uppercase dan filter hanya huruf A–Z.
- Hitung public key y = g^x mod p.
- Hitung a = g^k mod p dan y^k mod p.
- Untuk tiap huruf: m = angka(huruf) (A=0..Z=25), lalu b = (m * y^k) mod p.
- Tampilkan daftar pasangan (a,b). (Jika k sama untuk semua huruf, a akan sama untuk tiap pasangan.)

### Alur mode DECRYPT
- Minta input p dan x (private key).
- Terima pasangan (a,b) dalam format fleksibel (baris, atau 11,3;11,28;...).
- Untuk tiap pasangan: hitung s = a^x mod p. Dihitung s_inv = s^{-1} mod p (menggunakan Fermat, asumsi p prima).
- Ambil m = (b * s_inv) mod p. Jika 0 <= m <= 25, ubah menjadi huruf A–Z.
- Gabungkan hasil bila semua m berada di rentang 0..25.
- Tampilkan m, huruf (atau nilai numerik bila di luar rentang), dan ringkasan.

### Validasi & error handling
- Program memeriksa apakah p prima sebelum melanjutkan di mode encrypt.
- Jika ada m >= p, program menghentikan enkripsi karena representasi huruf tidak bisa dikodekan (solusi: pilih p lebih besar atau gunakan blok/segmentasi).
- Jika s tidak koprima dengan p (kasus tidak normal), program mengeluarkan peringatan.
