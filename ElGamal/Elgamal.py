"""
Nama    : Alfarisy Nafaro Gymnastiar
Kelas   : B
NPM     : 140810230020
PROGRAM : Elgamal Program
"""

import sys
import math

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

def modular_inverse(a: int, p: int) -> int:
    return pow(a, p - 2, p)

def letter_to_num(ch: str) -> int:
    return ord(ch) - ord('A')

def num_to_letter(n: int) -> str:
    return chr(n + ord('A'))

def input_int(prompt, min_val=None, max_val=None):
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
        except:
            print("Masukan harus bilangan bulat. Coba lagi.")
            continue
        if min_val is not None and v < min_val:
            print(f"Nilai harus >= {min_val}. Coba lagi.")
            continue
        if max_val is not None and v > max_val:
            print(f"Nilai harus <= {max_val}. Coba lagi.")
            continue
        return v

def input_plaintext(prompt):
    s = input(prompt)
    s_up = s.upper()
    filtered = ''.join(ch for ch in s_up if 'A' <= ch <= 'Z')
    removed = len(s_up) - len(filtered)
    if removed > 0:
        print(f"(Catatan: {removed} karakter non-alfabet diabaikan; hanya huruf A-Z diproses.)")
    if len(filtered) == 0:
        print("Tidak ada huruf A-Z di teks. Masukkan teks yang berisi huruf.")
        return input_plaintext(prompt)
    return filtered

def parse_pairs_input():

    print("Masukkan pasangan ciphertext (a,b).")
    print("Contoh satu baris: 11,3;11,28;11,26")
    print("Atau masukkan per baris: 11 3  (enter), 11 28 (enter), lalu baris kosong untuk selesai.")
    s = input("Masukkan (atau tekan Enter untuk mode baris): ").strip()
    pairs = []
    if s == '':
        while True:
            line = input().strip()
            if line == '':
                break
            line = line.replace(',', ' ').strip()
            parts = line.split()
            if len(parts) < 2:
                print("Format salah. Masukkan: a b  (contoh: 11 3).")
                continue
            try:
                a = int(parts[0]); b = int(parts[1])
            except:
                print("Nilai harus bilangan bulat. Coba lagi.")
                continue
            pairs.append((a, b))
    else:
        chunks = [c.strip() for c in s.replace(';', ' ; ').split(';') if c.strip() != '']
        if ';' in s:
            raw_pairs = s.split(';')
            for rp in raw_pairs:
                rp = rp.strip()
                if not rp:
                    continue
                rp = rp.replace(',', ' ').strip()
                parts = rp.split()
                if len(parts) < 2:
                    print(f"Ignored invalid entry: {rp}")
                    continue
                try:
                    a = int(parts[0]); b = int(parts[1])
                except:
                    print(f"Ignored invalid entry: {rp}")
                    continue
                pairs.append((a, b))
        else:
            s2 = s.replace(',', ' ')
            tokens = s2.split()
            if len(tokens) % 2 != 0:
                print("Jumlah nilai ganjil — harap masukkan pasangan lengkap a b.")
                return parse_pairs_input()
            for i in range(0, len(tokens), 2):
                try:
                    a = int(tokens[i]); b = int(tokens[i+1])
                except:
                    print("Format salah pada beberapa token. Ulangi input.")
                    return parse_pairs_input()
                pairs.append((a, b))
    if not pairs:
        print("Tidak ada pasangan yang dimasukkan. Coba lagi.")
        return parse_pairs_input()
    return pairs

def encrypt_mode():
    print("\n--- MODE ENCRYPT ---")
    # input p valid prime
    while True:
        p = input_int("Masukkan bilangan prima p: ")
        if not is_prime(p):
            print("p bukan prima. Masukkan p yang prima.")
            continue
        break
    g = input_int(f"Masukkan g (1 < g < {p}): ", min_val=2, max_val=p-1)
    x = input_int(f"Masukkan kunci privat x (1..{p-2}): ", min_val=1, max_val=p-2)
    k = input_int(f"Masukkan nonce k (1..{p-2}): ", min_val=1, max_val=p-2)
    plaintext = input_plaintext("Masukkan plaintext (hanya huruf A-Z diproses): ")

    y = pow(g, x, p)
    a = pow(g, k, p)
    yk = pow(y, k, p)
    print(f"\nPublic key y = g^x mod p = {g}^{x} mod {p} = {y}")
    print(f"a = g^k mod p = {g}^{k} mod {p} = {a}")
    print(f"y^k mod p = {y}^{k} mod {p} = {yk}\n")

    ms = [letter_to_num(ch) for ch in plaintext]
    if any(m >= p for m in ms):
        print("ERROR: Ada m >= p. Pilih p lebih besar atau gunakan enkripsi blok.")
        print("Detail m:", list(zip(plaintext, ms)))
        return

    bs = []
    print("Enkripsi per-huruf:")
    for i, ch in enumerate(plaintext, start=1):
        m = ms[i-1]
        b = (m * yk) % p
        bs.append(b)
        print(f"{i:2d}. '{ch}' -> m={m:2d}; b = (m * y^k) mod p = ({m} * {yk}) mod {p} = {b}")

    print("\nCiphertext (pasangan (a,b) untuk tiap huruf):")
    for i, b in enumerate(bs, start=1):
        print(f"{i:2d}. (a={a}, b={b})")
    print("\nSelesai mode encrypt.\n")

def decrypt_mode():
    print("\n--- MODE DECRYPT ---")
    p = input_int("Masukkan p (yang dipakai saat enkripsi): ")
    x = input_int("Masukkan kunci privat x: ")
    pairs = parse_pairs_input()
    a_values = [a for a,_ in pairs]
    if len(set(a_values)) > 1:
        print("Peringatan: ada lebih dari 1 nilai 'a' berbeda. Program akan memproses setiap pasangan secara independen.")
    recovered_nums = []
    recovered_letters = []
    for idx, (a,b) in enumerate(pairs, start=1):
        if a % p == 0:
            print(f"{idx:2d}. Peringatan: a mod p == 0 (tidak biasa).")
        s = pow(a, x, p)
        if math.gcd(s, p) != 1:
            print(f"{idx:2d}. Gagal: s dan p tidak koprima sehingga inverse tidak ada (s={s}).")
            recovered_nums.append(None)
            recovered_letters.append('?')
            continue
        s_inv = modular_inverse(s, p)
        m = (b * s_inv) % p
        recovered_nums.append(m)
        if 0 <= m <= 25:
            recovered_letters.append(num_to_letter(m))
        else:
            recovered_letters.append(f"[{m}]")
        print(f"{idx:2d}. (a={a}, b={b}) -> s = a^x mod p = {s}; s^-1 = {s_inv}; m = (b*s^-1) mod p = {m}")

    print("\nHasil dekripsi per pasangan:")
    for i, (m, ch) in enumerate(zip(recovered_nums, recovered_letters), start=1):
        print(f"{i:2d}. m = {m}  ->  {ch}")
    if all(isinstance(m, int) and 0 <= m <= 25 for m in recovered_nums):
        text = ''.join(num_to_letter(m) for m in recovered_nums)
        print("\nPlaintext (gabungan):", text)
    else:
        print("\nPlaintext tidak semua berbentuk huruf A-Z; beberapa m di luar rentang 0..25.")
    print("\nSelesai mode decrypt.\n")

def main():
    print("=== ElGamal (encrypt/decrypt) ===")
    while True:
        cmd = input("Pilih mode [encrypt/decrypt/exit]: ").strip().lower()
        if cmd == 'exit':
            print("Keluar. Sampai jumpa!")
            sys.exit(0)
        if cmd == 'encrypt':
            encrypt_mode()
        elif cmd == 'decrypt':
            decrypt_mode()
        else:
            print("Perintah tidak dikenali. Ketik 'encrypt', 'decrypt', atau 'exit'.")

if __name__ == "__main__":
    main()