# PQC-Learning-Module-WP1

git clone --branch OQS-OpenSSL_1_1_1-stable https://github.com/open-quantum-safe/openssl.git
cd openssl
./config
make -j$(nproc)
sudo make install

Pre-requisites see
https://github.com/open-quantum-safe/liboqs-python

Prerequisites
Install Dependencies:
Run pip install kyber-py cryptography in your Python environment.

kyber-py provides Kyber768 (NIST Level 3, ~AES-192 equivalent).

cryptography provides X25519 for classical ECDH.

Python Version: Tested with Python 3.8+ (March 3, 2025).

_______________________________________________________

Implementing Hybrid TLS in OpenSSL (Using OQS-OpenSSL)
🔸 Step 1: Install OpenSSL with PQC Support
OQS-OpenSSL is a fork of OpenSSL that includes support for Kyber, Dilithium, Falcon, and other PQC algorithms.

🔹 Install OQS-OpenSSL
bash

git clone --branch OQS-OpenSSL_1_1_1-stable https://github.com/open-quantum-safe/openssl.git
cd openssl
./config
make -j$(nproc)
sudo make install

🔸 Step 2: Generate a Hybrid Key Pair (ECDH + Kyber)
Use OQS-OpenSSL to create a hybrid key exchange mechanism that includes both ECDH and Kyber.

bash

openssl req -x509 -new -newkey oqs_kem_default+ecdh_secp384r1 -keyout hybrid_key.pem -out hybrid_cert.pem -nodes -days 365
oqs_kem_default = Uses Kyber-768 as the default PQC algorithm.
ecdh_secp384r1 = Classical ECDH key exchange for backward compatibility.
🔸 Step 3: Configure OpenSSL Server with Hybrid TLS
Edit the OpenSSL configuration file (openssl.cnf) and enable hybrid key exchange:

bash

[oqs_tls]
keyExchangeAlgorithms = OQS_KEM_Kyber768+ECDH_secp384r1
Start the TLS server with the hybrid key:

bash

openssl s_server -cert hybrid_cert.pem -key hybrid_key.pem -tls1_3 -www
🔸 Step 4: Test the Connection
On the client side, test the TLS connection using OpenSSL:

bash

openssl s_client -connect localhost:4433 -groups OQS_KEM_Kyber768+ECDH_secp384r1

If successful, the session key will be established using both Kyber and ECDH, ensuring security against classical and quantum threats.

________________________________________________________________________________________

Access https://openquantumsafe.org/liboqs/ in Python for PQC open surce to run following demos :

1.  Kyber512.py : implements a hybrid key exchange protocol combining X25519 (classical elliptic-curve key exchange) and Kyber512 (post-quantum key encapsulation mechanism) using the liboqs library
2.  ind-cpa.py : simulates an IND-CPA (Indistinguishability under Chosen-Plaintext Attack) test using AES-CBC encryption.
                 IND-CPA is a security property that ensures an adversary cannot distinguish between two ciphertexts, even if they can choose plaintexts to encrypt
3.  sig.py : demonstrates post-quantum digital signatures using liboqs, a library that implements PQC algorithms, using ML-DSA-44 is a lattice-based signature scheme that is quantum-resistant
4.  rand.py : demonstrates the use of post-quantum secure random number generators (RNGs), supports system-based and OpenSSL
5.  kem.py :  implements ML-KEM-512, a post-quantum Key Encapsulation Mechanism (KEM)


