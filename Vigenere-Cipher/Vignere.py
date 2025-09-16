"""
Nama    : Alfarisy Nafaro Gymnastiar
Kelas   : B
NPM     : 140810230020
PROGRAM : Vignere Program
"""
import sys

def normalize_key(key: str) -> str:
    return ''.join([c.upper() for c in key if c.isalpha()])

def generate_keystream(key: str, text: str):
    key = normalize_key(key)
    if not key:
        raise ValueError('Kunci harus berisi minimal satu huruf.')
    stream = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            stream.append(key[ki % len(key)])
            ki += 1
        else:
            stream.append(None)
    return stream

def encrypt(plaintext: str, key: str) -> str:
    ks = generate_keystream(key, plaintext)
    cipher = []
    for ch, kch in zip(plaintext, ks):
        if kch is None:
            cipher.append(ch)
            continue
        offset = ord(kch) - ord('A')
        if ch.isupper():
            base = ord('A')
            c = chr((ord(ch) - base + offset) % 26 + base)
            cipher.append(c)
        else:
            base = ord('a')
            c = chr((ord(ch) - base + offset) % 26 + base)
            cipher.append(c)
    return ''.join(cipher)

def decrypt(ciphertext: str, key: str) -> str:
    ks = generate_keystream(key, ciphertext)
    plain = []
    for ch, kch in zip(ciphertext, ks):
        if kch is None:
            plain.append(ch)
            continue
        offset = ord(kch) - ord('A')
        if ch.isupper():
            base = ord('A')
            p = chr((ord(ch) - base - offset) % 26 + base)
            plain.append(p)
        else:
            base = ord('a')
            p = chr((ord(ch) - base - offset) % 26 + base)
            plain.append(p)
    return ''.join(plain)

def main():
    print("=== Vigenère Cipher ===")
    while True:
        mode = input("Pilih mode [encrypt/decrypt] (atau 'exit' untuk keluar): ").strip().lower()
        if mode == 'exit':
            print("Keluar. Sampai jumpa!")
            sys.exit(0)
        if mode not in ('encrypt', 'decrypt'):
            print("Mode tidak valid. Ketik 'encrypt' atau 'decrypt'.")
            continue
        key = input("Masukkan kunci (hanya huruf, boleh campuran huruf besar/kecil): ").strip()

        if mode == 'encrypt':
            text = input("Masukkan plaintext (teks asli yang ingin dienkripsi): ")
        else:
            text = input("Masukkan ciphertext (teks terenkripsi yang ingin didekripsi): ")

        try:
            if mode == 'encrypt':
                out = encrypt(text, key)
                print("\n=== Ciphertext ===")
                print(out)
            else:
                out = decrypt(text, key)
                print("\n=== Plaintext ===")
                print(out)
        except Exception as e:
            print("Terjadi error:", e)
        print("\n---\n")

if __name__ == '__main__':
    main()