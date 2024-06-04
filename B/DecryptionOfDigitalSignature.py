#importowanie potrzebnych modułów z bibliotek
from Crypto.Hash import SHA3_256    #służy do generowania hashu za pomocą algorytmu SHA3 
from Crypto.PublicKey import RSA    #służy do operacji związanych z kluczami RSA
from Crypto.Signature import pkcs1_15   #służy do generowania i weryfikacji podpisów cyfrowych

def main(fileToHash, signatureToCheck, publicKey):
    #funkcja do generowania skrótu pliku (tak samo działająca jak w pliku CreatingDigitalSignature.py)
    def generate_file_hash(file_path):
        hash_obj = SHA3_256.new()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)
        return hash_obj

    #funkcja do ładowania klucza publicznego
    def load_public_key(file_path):
        with open(file_path, 'rb') as f: #otwieranie pliku w trybie binarnym
            return RSA.import_key(f.read()) #zwracanie załadowanego klucza publicznego po zaimportowaniu go (import_key)
                                            #RSA.import_key() zamienia ciąg bajtów na obiekt klucza RSA

    #funkcja do weryfikacji podpisu cyfrowego
    def verify_digital_signature(file_path, signature, public_key_path):
        public_key = load_public_key(public_key_path)   #ładowanie kluca publicznego
        file_hash = generate_file_hash(file_path)   #generowanie skrótu dla podanego pliku
        
        try:
            pkcs1_15.new(public_key).verify(file_hash, signature)   #tworzymy nowy obiekt weryfikujący z użyciem klucza publicznego 
                                                                    #oraz weryfikujemy nim czy podpis zgadza się z zahashowanym plikiem
            return True
        except (ValueError, TypeError): #wyjątek w przypadku, gdy nie powiedzie się operacja i podpis jest nieprawidłowy
            return False


    file_to_check = fileToHash
    public_key_path = publicKey

    #otwieranie pliku z podpisem cyfrowym i przypisuje jego zawartość do zmiennej signature
    with open(signatureToCheck, 'rb') as f: 
        signature = f.read()

    if verify_digital_signature(file_to_check, signature, public_key_path):
        print("Podpis cyfrowy jest prawidłowy.")
        return True
    else:
        print("Podpis cyfrowy jest nieprawidłowy.")
        return False