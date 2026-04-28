# uses SHA-256 to hash files to verify their integrity 

import hashlib
import secrets 

# reads file and returns a sha256 hash as a hex string
def hash_file(file_path: str) -> str:
    with open (file_path, 'rb') as f: 
        return hashlib.sha256(f.read()).hexdigest()
    
# hashes are saved to a text file for later verification
def save_hash(file_path: str):
    file_hash = hash_file(file_path)
    with open(file_path + '.hash', 'w') as f:
        f.write(file_hash)
    print(f"Hash saved: {file_hash}")
    
# checks hash of file against saved hash 
def verify_hash(file_path: str):
    with open(file_path + '.hash', 'r') as f:
        stored_hash = f.read()
    current_hash = hash_file(file_path)
 
    if secrets.compare_digest(current_hash, stored_hash):
        print("File integrity verified: hashes match")
    else:
        print("WARNING: hashes do not match, file may have been tapered with")



