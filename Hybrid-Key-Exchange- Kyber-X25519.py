from kyber import Kyber768  # Using Kyber768 (NIST Level 3, ~AES-192 security)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization
import os

# Step 1: Classical X25519 Key Exchange
def x25519_key_exchange():
    # Alice generates her private/public key pair
    alice_private = x25519.X25519PrivateKey.generate()
    alice_public = alice_private.public_key()

    # Bob generates his private/public key pair
    bob_private = x25519.X25519PrivateKey.generate()
    bob_public = bob_private.public_key()

    # Simulate exchange: Alice and Bob swap public keys
    # Alice computes shared secret using Bob's public key
    alice_shared = alice_private.exchange(bob_public)
    # Bob computes shared secret using Alice's public key
    bob_shared = bob_private.exchange(alice_public)

    # Both should get the same 32-byte shared secret
    assert alice_shared == bob_shared, "X25519 shared secrets don't match!"
    return alice_shared

# Step 2: PQC Kyber Key Exchange
def kyber_key_exchange():
    # Server (Bob) generates Kyber key pair
    public_key, private_key = Kyber768.keygen()

    # Client (Alice) generates a secret and encapsulates it with Bob's public key
    ciphertext, alice_secret = Kyber768.enc(public_key)

    # Server (Bob) decapsulates the ciphertext to recover the secret
    bob_secret = Kyber768.dec(ciphertext, private_key)

    # Both should get the same 32-byte secret
    assert alice_secret == bob_secret, "Kyber shared secrets don't match!"
    return alice_secret

# Step 3: Combine Secrets with HKDF
def combine_secrets(x25519_secret, kyber_secret, info=b"Hybrid Key Exchange"):
    # Concatenate the two secrets
    combined_input = x25519_secret + kyber_secret

    # Use HKDF to derive a secure 32-byte session key
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # Output 32-byte key
        salt=None,  # Optional salt
        info=info   # Context-specific info
    )
    hybrid_key = hkdf.derive(combined_input)
    return hybrid_key

# Main function to run hybrid key exchange
def hybrid_key_exchange():
    print("Starting Hybrid Key Exchange with X25519 and Kyber768...")

    # Perform X25519 key exchange
    x25519_secret = x25519_key_exchange()
    print(f"X25519 Shared Secret (32 bytes): {x25519_secret.hex()}")

    # Perform Kyber key exchange
    kyber_secret = kyber_key_exchange()
    print(f"Kyber Shared Secret (32 bytes): {kyber_secret.hex()}")

    # Combine secrets into a hybrid key
    hybrid_key = combine_secrets(x25519_secret, kyber_secret)
    print(f"Hybrid Shared Key (32 bytes): {hybrid_key.hex()}")

    return hybrid_key

if __name__ == "__main__":
    # Install dependencies: pip install kyber-py cryptography
    try:
        hybrid_key = hybrid_key_exchange()
        print("Hybrid key exchange completed successfully!")
    except ImportError as e:
        print(f"Error: Missing library - {e}. Install with 'pip install kyber-py cryptography'")
    except AssertionError as e:
        print(f"Error: Key exchange failed - {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")