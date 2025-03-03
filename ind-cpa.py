from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import hashlib

# Funzione per cifrare il messaggio con AES CBC
def aes_cbc_encrypt(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext

# Funzione per decifrare il messaggio con AES CBC
def aes_cbc_decrypt(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

# Funzione per generare una chiave simmetrica AES e un IV
def generate_aes_key_iv():
    key = get_random_bytes(16)  # AES-128
    iv = get_random_bytes(AES.block_size)  # Vettore di inizializzazione
    return key, iv

# Simulazione di un attacco CPA (Chosen Plaintext Attack)
def chosen_plaintext_attack(plaintext1, plaintext2):
    # Generazione della chiave AES e dell'IV
    key, iv = generate_aes_key_iv()

    # Cifriamo entrambi i testi in chiaro
    ciphertext1 = aes_cbc_encrypt(key, iv, plaintext1)
    ciphertext2 = aes_cbc_encrypt(key, iv, plaintext2)

    # Avversario che cerca di distinguere i testi cifrati
    # Supponiamo che l'attaccante abbia accesso ai due testi cifrati e debba determinare quale testo in chiaro corrisponde al quale.
    # In un caso IND-CPA sicuro, l'attaccante non dovrebbe essere in grado di distinguere tra i due testi cifrati.
    return ciphertext1, ciphertext2

# Eseguiamo l'attacco con due testi in chiaro
plaintext1 = "This is a confidential message!"
plaintext2 = "This is another confidential message!"
ciphertext1, ciphertext2 = chosen_plaintext_attack(plaintext1, plaintext2)

print("Ciphertext 1:", ciphertext1.hex())
print("Ciphertext 2:", ciphertext2.hex())

# In una situazione reale, l'attaccante non dovrebbe essere in grado di distinguere tra i due ciphertext
# senza conoscere la chiave di cifratura.
