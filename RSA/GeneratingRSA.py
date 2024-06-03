from Crypto.PublicKey import RSA
import os

def load_random_bits(filepath):
    with open(filepath, 'rb') as file:
        return file.read()

# Wczytanie danych losowych z pliku RandomBits.txt
random_bits = load_random_bits('TRNG/RandomBits.txt')
current_index = 0

def generate_random_bytes(n):
    global random_bits, current_index
    end_index = current_index + n
    if end_index > len(random_bits):
        random_bits += os.urandom(end_index - len(random_bits))
    random_bytes = random_bits[current_index:end_index]
    current_index = end_index
    return random_bytes

# Generowanie kluczy RSA używając niestandardowej funkcji generującej losowe bajty
rsa_key = RSA.generate(2048, e=65537, randfunc=generate_random_bytes)

# Eksportowanie kluczy do formatu PEM
private_key_pem = rsa_key.export_key()
public_key_pem = rsa_key.public_key().export_key()

# Upewnienie się, że folder RSA_keys istnieje
key_directory = 'RSA_keys'
os.makedirs(key_directory, exist_ok=True)

# Zapis kluczy do plików PEM
private_key_path = os.path.join(key_directory, 'private_key.pem')
public_key_path = os.path.join(key_directory, 'public_key.pem')

with open(private_key_path, 'wb') as private_file:
    private_file.write(private_key_pem)

with open(public_key_path, 'wb') as public_file:
    public_file.write(public_key_pem)

print("Klucze RSA zostały wygenerowane i zapisane w folderze RSA_keys.")
