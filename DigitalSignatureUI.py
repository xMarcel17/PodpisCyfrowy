#biblioteka tkinter oraz moduły potrzebne do stworzenia GUI, wyboru plików i wyświetlania komunikatów
import tkinter as tk
from tkinter import filedialog, messagebox

#moduły z bilbioteki cryptodome używane w celach kryptograficznych
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_256
from Crypto.Signature import pkcs1_15

#biblioteka używana do sprawdzania obecności plików, usuwania ich
import os

#pliki, w których wykonywane są poszczególne operacje 
import RSA.GeneratingRSA
import A.CreatingDigitalSignature
import B.DecryptionOfDigitalSignature

def generate_keys():
    file_path_GK = filedialog.askopenfilename() #otwarcie okna dialogowego do wyboru pliku
    RSA.GeneratingRSA.main(file_path_GK)
    messagebox.showinfo("Success", "Keys generated successfully! You can now use the public key.")  #wyświetlanie komunikatu

def create_signature():
    if os.path.exists("RSA/RSA_keys/private_key.pem") and os.path.exists("RSA/RSA_keys/public_key.pem"):    #sprawdzenie czy istnieją klucze
        file_path_CS = filedialog.askopenfilename() 
        A.CreatingDigitalSignature.main(file_path_CS)
        messagebox.showinfo("Success", f"Signature created for {file_path_CS} and saved as signature.txt")
    else:
        messagebox.showerror("Error", f"Can't create digital signature without generating RSA keys first.")

def verify_signature():
    file_path_VS_1 = filedialog.askopenfilename(title='Select file to check')
    if file_path_VS_1 == '':
        messagebox.showerror("Error", f"The file to check was not selected. Start over!")
        return
    file_path_VS_2 = filedialog.askopenfilename(title='Load the signature')
    file_extension2 = file_path_VS_2[-4:]
    if file_extension2 != '.txt':
        if file_path_VS_2 == '':
            messagebox.showerror("Error", f"The signature was not loaded. Start over!")
            return
        else: 
            messagebox.showerror("Error", f"The signature has wrong type. Start over!")
            return
    file_path_VS_3 = filedialog.askopenfilename(title='Load the public key')
    file_extension3 = file_path_VS_3[-4:]
    if file_extension3 != '.pem':
        if file_path_VS_3 == '':
            messagebox.showerror("Error", f"The public key was not loaded. Start over!")
            return
        else: 
            messagebox.showerror("Error", f"The public key has wrong type. Start over!")
            return

    if B.DecryptionOfDigitalSignature.main(file_path_VS_1, file_path_VS_2, file_path_VS_3):
        messagebox.showinfo("Success", f"Signature for the selected file is valid.")
    else:
        messagebox.showerror("Error", f"Signature for the selected file is invalid.")

def delete_everything():
    signatureCheck = False
    publicKeyCheck = False
    privateKeyCheck = False
    
    if os.path.exists("RSA/RSA_keys/private_key.pem"):
        os.remove("RSA/RSA_keys/private_key.pem")   #usuwanie plików
        privateKeyCheck = True
    if os.path.exists("RSA/RSA_keys/public_key.pem"):
        os.remove("RSA/RSA_keys/public_key.pem")
        publicKeyCheck = True
    if os.path.exists("A/signature.txt"):
        os.remove("A/signature.txt")
        signatureCheck = True

    if privateKeyCheck and publicKeyCheck and signatureCheck:
        messagebox.showinfo("Success", f"Signature and generated keys have been deleted.")
    if signatureCheck and publicKeyCheck==False and privateKeyCheck==False:
        messagebox.showinfo("Success", f"Signature has been deleted.")
    if signatureCheck==False and publicKeyCheck and privateKeyCheck:
        messagebox.showinfo("Success", f"RSA Keys have been deleted.")
    else:
        messagebox.showerror("Error", f"No things to delete.")

#GUI konfiguracja
root = tk.Tk()  #root to główne okno aplikacji i jest tu tworzone
root.title("Digital Signature Tool")    #tytuł okna
root.geometry("400x300")    #rozmiary okna
root.configure(bg="#f0f0f0")    #kolor tła okna

#etykieta tytułowa
title_label = tk.Label(root, text="Digital Signature Tool", font=("Helvetica", 16, "bold"), bg="#f0f0f0")   #stworzenie etykiety, gdzie root to okno główne, do którego jest ona przypisana
title_label.pack(pady=10)   #ustawienie odstępu pionowego

#ramka na przyciski
frame = tk.Frame(root, bg="#f0f0f0")    #dodanie ramki na przyciski i jest przypisana do root
frame.pack(pady=30)

#tworzenie przycisku, gdzie frame jest ramką, do której przypisany jest ten przycisk
#po kliknięciu na przycisk wywołuję się funkcja z command
generate_btn = tk.Button(frame, text="Generate RSA Keys", command=generate_keys, bg="#4CAF50", fg="white", font=("Helvetica", 12))
#dodanie przycisku do ramki umieszczając go w odpowiedniej kolumnie i wierszu oraz ustawiając odpowiednie odstępy i poziom
generate_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

sign_btn = tk.Button(frame, text="Create Digital Signature", command=create_signature, bg="#2196F3", fg="white", font=("Helvetica", 12))
sign_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

verify_btn = tk.Button(frame, text="Verify Digital Signature", command=verify_signature, bg="#a67b5b", fg="white", font=("Helvetica", 12))
verify_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

clear_btn = tk.Button(frame, text="Delete keys and signature", command=delete_everything, bg="#f44336", fg="white", font=("Helvetica", 12))
clear_btn.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

#uruchomienie pętli głównej aplikacji Tkinter, która czeka na interakcję użytkownika i reaguje na nie zgodnie z funkcjami
root.mainloop()