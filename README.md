# PQC-Learning-Module-WP1

Open Source Tool PQC :

1. Open Quantum Safe - liboqs -> https://openquantumsafe.org/liboqs/
2. TQ42 Crypthography Library -> https://github.com/terra-quantum-public/tq42-pqc-oss
3. NTRU Cryptosystem -> https://ntru.org/
4. OpenFHE -> https://github.com/openfheorg
_______________________________________________________

Implementing Hybrid TLS in OpenSSL (Using OQS-OpenSSL)

Last update https://github.com/open-quantum-safe/oqs-provider/

✅ Steps to Build & Install oqs-provider (Post-Quantum OpenSSL)
Follow these steps to correctly install and integrate Open Quantum Safe (OQS) Provider with OpenSSL.

1️⃣ Install Dependencies
Ensure your system has the necessary dependencies installed:
sudo apt update && sudo apt install -y \
    cmake gcc g++ ninja-build perl python3-pytest \
    python3-pytest-xdist python3-cryptography \
    curl unzip doxygen graphviz
    
2️⃣ Clone the OQS-Provider Repository
cd ~/PQC  # Navigate to your PQC working directory
git clone --recursive https://github.com/open-quantum-safe/oqs-provider.git
cd oqs-provider

3️⃣ Build and Install OpenSSL 3 with OQS Support
Since OQS-Provider works with OpenSSL 3, we need to build it correctly:
mkdir build && cd build
cmake -GNinja ..
ninja
sudo ninja install

4️⃣ Verify OpenSSL Installation
openssl list -providers

5️⃣ Test PQC Algorithms
openssl list -signature-algorithms | grep OQS
openssl list -kem-algorithms | grep OQS


🔸 Step 2: Generate a Hybrid Key Pair ECDSA (classical) + PQC signature certificate using Dilithium2.
openssl genpkey -algorithm dilithium2 -out server_dilithium2.key -provider oqsprovider
openssl req -new -key server_dilithium2.key -out server_dilithium2.csr -provider oqsprovider
openssl req -x509 -days 365 -key server_dilithium2.key -in server_dilithium2.csr \
  -out server_dilithium2.crt -provider oqsprovider


🔸 Step 3: Configure OpenSSL Server with Hybrid TLS
openssl s_server -cert server_dilithium2.crt -key server_dilithium2.key \
  -provider oqsprovider -www


🔸 Step 4: Test the Connection
openssl s_client -connect localhost:4433 -provider oqsprovider

If successful, you should see a successful TLS handshake.
✅ Expected Output:
New, TLSv1.3, Cipher is OQS_KEM_KYBER512 with TLS_AES_128_GCM_SHA256

________________________________________________________________________________________

Access https://openquantumsafe.org/liboqs/ in Python for PQC open surce to run following demos :

1.  Kyber512.py : implements a hybrid key exchange protocol combining X25519 (classical elliptic-curve key exchange) and Kyber512 (post-quantum key encapsulation mechanism) using the liboqs library
2.  ind-cpa.py : simulates an IND-CPA (Indistinguishability under Chosen-Plaintext Attack) test using AES-CBC encryption.
                 IND-CPA is a security property that ensures an adversary cannot distinguish between two ciphertexts, even if they can choose plaintexts to encrypt
3.  sig.py : demonstrates post-quantum digital signatures using liboqs, a library that implements PQC algorithms, using ML-DSA-44 is a lattice-based signature scheme that is quantum-resistant
4.  rand.py : demonstrates the use of post-quantum secure random number generators (RNGs), supports system-based and OpenSSL
5.  kem.py :  implements ML-KEM-512, a post-quantum Key Encapsulation Mechanism (KEM)


