# encrypts and decrpts files using AES encryption
import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def get_key(password: str, salt: bytes) -> bytes:
    # Derive a key from the password and salt using PBKDF2
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
def encrypt_file(file_path: str, password: str):
    # random salt for key 
    salt = secrets.token_bytes(16) 
    iv = secrets.token_bytes(16)
    key = get_key(password, salt)
    
    # reads the file user wants encrypted 
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    
    # sets up AES for encryption
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    # writes the salt, iv, and ciphertext to a new file with .enc extension
    output_path = file_path + '.enc'
    with open(output_path, 'wb') as f:
        f.write(salt + iv + ciphertext)
    print(f"File encrypted: {output_path}")
    
# decrypts the file by reading the salt and iv from the encrypted file
def decrypt_file(file_path: str, password: str):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # takes first 16 bytes as salt, next 16 bytes as iv, and the rest as the ciphertext
    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]
    key = get_key(password, salt)
    
    # setting up AES for decryption
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # writes the decrypted plaintext to a new file without the .enc extension
    output_path = file_path[:-4]  # removes .enc 
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    print(f"File decrypted: {output_path}")
    
    