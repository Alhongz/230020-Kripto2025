'''
Nama    : Alfarisy Nafaro Gymnastiar
Kelas   : B
NPM     : 140810230020
PROGRAM : Hill Cipher Program
'''

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("Tidak ada invers modulo (gcd != 1).")
    return x % m

def matrix_det(mat):
    n = len(mat)
    if n == 1:
        return mat[0][0]
    if n == 2:
        return mat[0][0]*mat[1][1] - mat[0][1]*mat[1][0]
    det = 0
    for c in range(n):
        minor = [row[:c] + row[c+1:] for row in mat[1:]]
        det += ((-1) ** c) * mat[0][c] * matrix_det(minor)
    return det

def matrix_transpose(mat):
    return [list(row) for row in zip(*mat)]

def matrix_mul(A, B, mod=None):
    m = len(A); n = len(A[0]); p = len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            s = 0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s % mod if mod is not None else s
    return C

def matrix_cofactor(mat):
    n = len(mat)
    cof = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for idx,row in enumerate(mat) if idx != i]
            cof[i][j] = ((-1) ** (i + j)) * matrix_det(minor)
    return cof

def matrix_mod_inv(mat, modulus):
    n = len(mat)
    det = matrix_det(mat)
    det_mod = det % modulus
    det_inv = modinv(det_mod, modulus)
    cof = matrix_cofactor(mat)
    adj = matrix_transpose(cof)
    inv = [[(det_inv * adj[i][j]) % modulus for j in range(n)] for i in range(n)]
    return inv

def clean_text(s):
    return ''.join([c for c in s.upper() if 'A' <= c <= 'Z'])

def text_to_numbers(s):
    return [ord(c) - ord('A') for c in s]

def numbers_to_text(nums):
    return ''.join(chr((n % 26) + ord('A')) for n in nums)

def chunk(lst, n):
    res = []
    for i in range(0, len(lst), n):
        block = lst[i:i+n]
        if len(block) < n:
            block += [ord('X') - ord('A')] * (n - len(block))
        res.append(block)
    return res

def encrypt(plaintext, key):
    mod = 26
    pt = text_to_numbers(clean_text(plaintext))
    n = len(key)
    blocks = chunk(pt, n)
    cipher_nums = []
    for block in blocks:
        col = [[x] for x in block]
        prod = matrix_mul(key, col, mod)
        for i in range(n):
            cipher_nums.append(prod[i][0] % mod)
    return numbers_to_text(cipher_nums)

def decrypt(ciphertext, key):
    mod = 26
    ct = text_to_numbers(clean_text(ciphertext))
    n = len(key)
    inv_key = matrix_mod_inv(key, mod)
    blocks = chunk(ct, n)
    plain_nums = []
    for block in blocks:
        col = [[x] for x in block]
        prod = matrix_mul(inv_key, col, mod)
        for i in range(n):
            plain_nums.append(prod[i][0] % mod)
    return numbers_to_text(plain_nums)

def find_key_from_plain_cipher(plaintext, ciphertext, n):
    mod = 26
    pt = text_to_numbers(clean_text(plaintext))
    ct = text_to_numbers(clean_text(ciphertext))
    min_len = n * n
    if len(pt) < min_len or len(ct) < min_len:
        raise ValueError(f"Perlu minimal {min_len} huruf plaintext & ciphertext.")
    pt_blocks = chunk(pt, n)
    ct_blocks = chunk(ct, n)
    for start in range(0, len(pt_blocks) - n + 1):
        P = [[pt_blocks[start + col][row] for col in range(n)] for row in range(n)]
        C = [[ct_blocks[start + col][row] for col in range(n)] for row in range(n)]
        try:
            P_inv = matrix_mod_inv(P, mod)
        except Exception:
            continue
        K = matrix_mul(C, P_inv, mod)
        return [[x % mod for x in row] for row in K]
    raise ValueError("Tidak ditemukan P invertible pada pasangan yang diberikan.")

# ---- helper input key ----
def input_key():
    while True:
        try:
            n = int(input("Masukkan ukuran kunci n (mis. 2 atau 3): ").strip())
            if n <= 0:
                print("Ukuran harus positif.")
                continue
            print(f"Masukkan {n} baris, tiap baris {n} angka (pisahkan spasi). Contoh untuk 3x3: 6 24 1")
            mat = []
            for i in range(n):
                row = input(f"Baris {i+1}: ").strip().split()
                if len(row) != n:
                    raise ValueError("Jumlah angka di baris tidak cocok.")
                mat.append([int(x) % 26 for x in row])
            # cek invertible (untuk dekripsi nanti)
            det = matrix_det(mat) % 26
            if egcd(det, 26)[0] != 1:
                print("Peringatan: determinan matriks tidak coprime dengan 26 -> tidak invertible modulo 26.")
            return mat
        except ValueError as e:
            print("Input salah:", e)
            print("Coba lagi.\n")

def print_matrix(mat):
    for r in mat:
        print(' '.join(str(x) for x in r))

def main():
    print("Hill Cipher — A..Z (mod 26).")
    while True:
        print("\nMENU:")
        print("1) Encrypt")
        print("2) Decrypt")
        print("3) Recover key")
        print("0) Keluar")
        choice = input("=> ").strip()
        if choice == '1':
            plaintext = input("Masukkan plaintext (akan dibersihkan non-alfabet): ")
            key = input_key()
            try:
                ct = encrypt(plaintext, key)
                print("Ciphertext:", ct)
            except Exception as e:
                print("Gagal enkripsi:", e)
        elif choice == '2':
            ciphertext = input("Masukkan ciphertext: ")
            key = input_key()
            try:
                pt = decrypt(ciphertext, key)
                print("Plaintext (hasil decrypt):", pt)
            except Exception as e:
                print("Gagal dekripsi:", e)
        elif choice == '3':
            plaintext = input("Masukkan plaintext (yang sudah ada): ")
            ciphertext = input("Masukkan ciphertext (yang bersesuaian): ")
            try:
                n = int(input("Masukkan ukuran kunci n yang dicari (mis. 2 atau 3): "))
                K = find_key_from_plain_cipher(plaintext, ciphertext, n)
                print("Kunci ditemukan:")
                print_matrix(K)
            except Exception as e:
                print("Gagal recover key:", e)
        elif choice == '0':
            print("Keluar.")
            break
        else:
            print("Pilihan tidak dikenal. Pilih 0-3.")

if __name__ == "__main__":
    main()