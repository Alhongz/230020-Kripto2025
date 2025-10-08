from PIL import Image
import os

def data_ke_biner(data):
    """Mengubah data (string atau bytes) menjadi representasi biner."""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, bytearray):
        return ''.join([format(i, "08b") for i in data])
    raise TypeError("Tipe data tidak didukung.")

def sembunyikan_data(gambar_pembawa, data_rahasia):
    """Menyembunyikan data ke dalam gambar."""
    gambar_stego = gambar_pembawa.copy()
    lebar, tinggi = gambar_pembawa.size
    
    kapasitas_maks = lebar * tinggi * 3
    if len(data_rahasia) > kapasitas_maks:
        raise ValueError("Error: Ukuran data rahasia melebihi kapasitas gambar pembawa!")

    indeks_data = 0
    data_selesai = False
    
    for y in range(tinggi):
        for x in range(lebar):
            pixel = list(gambar_pembawa.getpixel((x, y)))
            
            for i in range(3):
                if indeks_data < len(data_rahasia):
                    pixel[i] = pixel[i] & 254 | int(data_rahasia[indeks_data])
                    indeks_data += 1
                else:
                    data_selesai = True
                    break
            
            gambar_stego.putpixel((x, y), tuple(pixel))
            
            if data_selesai:
                break
        if data_selesai:
            break
            
    return gambar_stego

def ekstrak_data(gambar_stego, panjang_bit):
    """Mengekstrak sejumlah bit data dari gambar steganografi."""
    lebar, tinggi = gambar_stego.size
    data_biner = ""
    bit_terekstrak = 0
    
    for y in range(tinggi):
        for x in range(lebar):
            pixel = gambar_stego.getpixel((x, y))
            for i in range(3):
                if bit_terekstrak < panjang_bit:
                    data_biner += str(pixel[i] & 1)
                    bit_terekstrak += 1
                else:
                    break
            if bit_terekstrak >= panjang_bit:
                break
        if bit_terekstrak >= panjang_bit:
            break
            
    return data_biner


def encode_teks(path_gambar_pembawa, pesan_rahasia, path_output):
    """Fungsi utama untuk menyembunyikan teks ke dalam gambar."""
    print("Mulai proses encoding teks...")
    try:
        gambar = Image.open(path_gambar_pembawa, 'r').convert("RGB")
    except FileNotFoundError:
        print(f"Error: File gambar '{path_gambar_pembawa}' tidak ditemukan.")
        return

    delimiter = "_-_END_-_"
    data_rahasia = pesan_rahasia + delimiter
    
    data_biner = data_ke_biner(data_rahasia)
    
    try:
        gambar_hasil = sembunyikan_data(gambar, data_biner)
        gambar_hasil.save(path_output, "PNG")
        print(f"Pesan berhasil disembunyikan di '{path_output}'")
    except ValueError as e:
        print(e)


def decode_teks(path_gambar_stego):
    """Fungsi utama untuk membaca teks tersembunyi dari gambar."""
    print("Mulai proses decoding teks...")
    try:
        gambar = Image.open(path_gambar_stego, 'r')
    except FileNotFoundError:
        print(f"Error: File gambar '{path_gambar_stego}' tidak ditemukan.")
        return

    data_biner_terekstrak = ""
    pesan_ditemukan = ""
    delimiter = "_-_END_-_"
    lebar, tinggi = gambar.size
    
    for y in range(tinggi):
        for x in range(lebar):
            pixel = gambar.getpixel((x, y))
            for warna in pixel[:3]: # Hanya R, G, B
                data_biner_terekstrak += str(warna & 1)
                
                if len(data_biner_terekstrak) % 8 == 0:
                    char_biner = data_biner_terekstrak[-8:]
                    try:
                        pesan_ditemukan += chr(int(char_biner, 2))
                        if pesan_ditemukan.endswith(delimiter):
                            print("Pesan tersembunyi berhasil ditemukan!")
                            return pesan_ditemukan[:-len(delimiter)]
                    except ValueError:
                        pass
    
    print("Decoding selesai, namun delimiter akhir pesan tidak ditemukan.")
    return None


def encode_gambar(path_gambar_pembawa, path_gambar_rahasia, path_output):
    """Fungsi utama untuk menyembunyikan file gambar ke dalam gambar lain."""
    print("Mulai proses encoding gambar...")
    try:
        gambar_pembawa = Image.open(path_gambar_pembawa, 'r').convert("RGB")
    except FileNotFoundError:
        print(f"Error: File gambar pembawa '{path_gambar_pembawa}' tidak ditemukan.")
        return
        
    try:
        with open(path_gambar_rahasia, "rb") as f:
            data_gambar_rahasia = f.read()
    except FileNotFoundError:
        print(f"Error: File gambar rahasia '{path_gambar_rahasia}' tidak ditemukan.")
        return
    
    ukuran_data = len(data_gambar_rahasia)
    
    biner_ukuran = format(ukuran_data, '032b')
    
    biner_data_gambar = data_ke_biner(data_gambar_rahasia)
    
    data_untuk_disembunyikan = biner_ukuran + biner_data_gambar
    
    try:
        gambar_hasil = sembunyikan_data(gambar_pembawa, data_untuk_disembunyikan)
        gambar_hasil.save(path_output, "PNG")
        print(f"Gambar berhasil disembunyikan di '{path_output}'")
    except ValueError as e:
        print(e)


def decode_gambar(path_gambar_stego, path_output_rahasia):
    """Fungsi utama untuk mengekstrak gambar tersembunyi."""
    print("Mulai proses decoding gambar...")
    try:
        gambar_stego = Image.open(path_gambar_stego, 'r')
    except FileNotFoundError:
        print(f"Error: File gambar '{path_gambar_stego}' tidak ditemukan.")
        return
        
    biner_ukuran = ekstrak_data(gambar_stego, 32)
    ukuran_file_rahasia = int(biner_ukuran, 2)
    
    total_bit_ekstrak = 32 + (ukuran_file_rahasia * 8)
    
    print(f"Ukuran file rahasia terdeteksi: {ukuran_file_rahasia} bytes")
    print(f"Mengekstrak {total_bit_ekstrak} bits...")
    
    data_biner_lengkap = ekstrak_data(gambar_stego, total_bit_ekstrak)
    
    biner_data_gambar = data_biner_lengkap[32:]
    
    data_bytes = bytearray()
    for i in range(0, len(biner_data_gambar), 8):
        byte = biner_data_gambar[i:i+8]
        if len(byte) < 8: continue
        data_bytes.append(int(byte, 2))
        
    with open(path_output_rahasia, "wb") as f:
        f.write(data_bytes)
    
    print(f"Gambar rahasia berhasil diekstrak dan disimpan di '{path_output_rahasia}'")


if __name__ == '__main__':
    print("--- DEMO STEGANOGRAFI TEKS ---")
    pesan = "Aku Fans Manchester United"
    encode_teks('carrier.png', pesan, 'stego_hasil_teks.png')
    pesan_hasil_decode = decode_teks('stego_hasil_teks.png')
    
    if pesan_hasil_decode:
        print("Pesan yang diekstrak:", pesan_hasil_decode)
    
    print("\n" + "="*40 + "\n")
    
    print("--- DEMO STEGANOGRAFI GAMBAR ---")
    encode_gambar('carrier.png', 'secret.png', 'stego_hasil_gambar.png')
    decode_gambar('stego_hasil_gambar.png', 'rahasia_terungkap.png')