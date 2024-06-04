import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_256
from Crypto.Signature import pkcs1_15
import os
import RSA.GeneratingRSA
import A.CreatingDigitalSignature
import B.DecryptionOfDigitalSignature

def generate_keys():
    file_path_GK = filedialog.askopenfilename()
    RSA.GeneratingRSA.main(file_path_GK)
    messagebox.showinfo("Success", "Keys generated successfully! You can now use the public key.")

def create_signature():
    if os.path.exists("RSA/RSA_keys/private_key.pem") and os.path.exists("RSA/RSA_keys/public_key.pem"):
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
        os.remove("RSA/RSA_keys/private_key.pem")
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

# GUI setup
root = tk.Tk()
root.title("Digital Signature Tool")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Title
title_label = tk.Label(root, text="Digital Signature Tool", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Frame for buttons
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

generate_btn = tk.Button(frame, text="Generate Keys", command=generate_keys, bg="#4CAF50", fg="white", font=("Helvetica", 12))
generate_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

sign_btn = tk.Button(frame, text="Create Digital Signature", command=create_signature, bg="#2196F3", fg="white", font=("Helvetica", 12))
sign_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

verify_btn = tk.Button(frame, text="Verify Digital Signature", command=verify_signature, bg="#ffc680", fg="white", font=("Helvetica", 12))
verify_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

clear_btn = tk.Button(frame, text="Delete keys and signature", command=delete_everything, bg="#f44336", fg="white", font=("Helvetica", 12))
clear_btn.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

root.mainloop()
