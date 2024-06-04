#importowanie potrzebnych modułów z bibliotek
from Crypto.PublicKey import RSA    #służy do operacji związanych z kluczami RSA
import os

def main(randomBitsFile):
    #funkcja zwracająca zawartość (w bajtach) pliku z losowymi bitami
    def load_random_bits(file): #argumentem funkcji jest plik z losowymi
        with open(file, 'rb') as file:
            return file.read()

    #wczytanie danych losowych z pliku RandomBits.txt do random_bits 
    random_bits = load_random_bits(randomBitsFile)

    #ustawienie indeksu, który jest indeksem bieżącej pozycji w random_bits
    current_index = 0

    #funkcja generująca n losowych bajtów
    def generate_random_bytes(n):
        nonlocal random_bits, current_index   
        end_index = current_index + n   #indeks końcowy potrzebnych bajtów
        if end_index > len(random_bits):    #warunek sprawdzający, czy wymagana jest większa ilość bajtów dla wygnerowania kluczy, niż ta posiadana
            random_bits += os.urandom(end_index - len(random_bits)) #jeżeli potrzeba więcej bajtów to są one dodawana za pomocą metody urandom(size) 
        random_bytes = random_bits[current_index:end_index] #random_bytes przechowuje bajty od current_index do end_index ze zmiennej random_bits
        current_index = end_index   #aktualizowanie current_index na end_index
        return random_bytes #zwracanie wygenerowanych losowych bajtów potrzebnych dla funkcji generate

    #generowanie kluczy RSA używając niestandardowej funkcji generującej losowe bajty
    rsa_key = RSA.generate(2048, e=65537, randfunc=generate_random_bytes)
    #2048 to rozmiar modułu RSA/długość klucza (w bitach)
    #e to publiczny wykładnik RSA
    #randfunc to funkcja do generowania losowych liczb, która przyjmuje pojedynczą liczbę całkowitą N i zwraca ciąg losowych danych o długości N bajtów

    #eksportowanie kluczy do formatu PEM i przypisanie ich do zmiennych
    #export_key() to metoda eksportująca klucz RSA do formatu PEM
    private_key_pem = rsa_key.export_key()  #prywatny
    public_key_pem = rsa_key.public_key().export_key()  #publiczny

    #upewnienie się, że folder RSA_keys istnieje
    key_directory = 'RSA/RSA_keys' #przypisanie ścieżki do zmiennej key_directory (miejsce, gdzie zapiszą się klucze)
    if not os.path.exists(key_directory):   #sprawdzamy, czy katalog w ogóle istnieje
        os.makedirs(key_directory, exist_ok=True)   #funkcja, która tworzy folder RSA_keys, jeśli jeszcze nie istnieje

    #tworzenie pełnych ścieżek do plików z kluczami
    private_key_path = os.path.join(key_directory, 'private_key.pem')   #pełna ścieżka do pliku z kluczem prywatnym
    public_key_path = os.path.join(key_directory, 'public_key.pem') #pełna ścieżka do pliku z kluczem publicznym

    #zapisywanie klucza prywatnego
    with open(private_key_path, 'wb') as private_file:
        private_file.write(private_key_pem)

    #zapisywanie klucza publicznego
    with open(public_key_path, 'wb') as public_file:
        public_file.write(public_key_pem)

    print("Klucze RSA zostały wygenerowane i zapisane w folderze RSA_keys.")