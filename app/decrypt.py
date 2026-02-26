from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
import sys


def auto_decrypt():
    key_path = Path(__file__).parent.parent / "private_key.pem"
    encrypted_path = Path(__file__).parent.parent / ".env.encrypted"
    env_path = Path(__file__).parent.parent / ".env"
    
    if env_path.exists():
        return
    
    if not key_path.exists():
        print("💡 Get private_key.pem from the repository owner")
        sys.exit(1)
    
    if not encrypted_path.exists():
        print("Need env.encrypted")
        sys.exit(1)
    # Decrypt
    try:
        with open(key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        
        with open(encrypted_path, "rb") as f:
            encrypted = base64.b64decode(f.read())
        
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        with open(env_path, "wb") as f:
            f.write(decrypted)
        
        print("Decrypted, subba")
    except Exception as e:
        print(f"Decryption failed: {e}")
        sys.exit(1)