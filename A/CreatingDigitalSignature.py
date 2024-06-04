#importowanie potrzebnych modułów z bibliotek
from Crypto.Hash import SHA3_256    #służy do generowania hashu za pomocą algorytmu SHA3 
from Crypto.PublicKey import RSA    #służy do operacji związanych z kluczami RSA
from Crypto.Signature import pkcs1_15   #służy do generowania i weryfikacji podpisów cyfrowych

def main(fileToHash):
    #funkcja do generowania skrótu pliku
    def generate_file_hash(file_path):
        hash_obj = SHA3_256.new()   #stworzenie nowego obiektu hashującego
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):    #przypisywanie do zmiennej chunk kawałków (po 8192 bajty) pliku, który ma być zhashowany 
                hash_obj.update(chunk)  #aktualizowanie obiektu hashującego dla każdego kawałka
            #while kończy się w przypadku, gdy chunk jest none, 
            #czyli nic już do niego nie zostało przypisane, bo plik do zahashowania się skończył
        return hash_obj

    #funkcja do ładowania klucza prywatnego
    def load_private_key(file_path):
        with open(file_path, 'rb') as f:    #otwieranie pliku w trybie binarnym
            return RSA.import_key(f.read()) #zwracanie załadowanego klucza prywatnego po zaimportowaniu go (import_key)
                                            #RSA.import_key() zamienia ciąg bajtów na obiekt klucza RSA

    #funkcja do tworzenia podpisu cyfrowego
    def create_digital_signature(file_path, private_key_path):
        private_key = load_private_key(private_key_path)    #ładowanie klucza prywatnego
        file_hash = generate_file_hash(file_path)   #generowanie skrótu pliku (zahashowanie)
        signature = pkcs1_15.new(private_key).sign(file_hash)   #stworzenie podpisu cyfrowego za pomocą klucza prywatnego oraz 'pkcs1_15'
        return signature

    file_to_check = fileToHash  #file_to_check otrzymuje ścieżkę do pliku, który ma być podpisany
    private_key_path = "RSA/RSA_keys/private_key.pem"   #private_key_path ustawia ścieżkę do wygenerowanego klucza prywatnego

    signature = create_digital_signature(file_to_check, private_key_path)
        
    with open('A/signature.txt', 'wb') as f:
            f.write(signature)

    print("Podpis cyfrowy został wygenerowany i zapisany do pliku signature.txt")
