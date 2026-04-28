# -*- coding: utf-8 -*-

# digital_signature.py
# Uses RSA digital signatures to sign a file and verify its authenticity

import os
import logging

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


# set up logging so signing and verification events are recorded in audit.log
logging.basicConfig(
    filename='audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)


# generates RSA private/public key files if they do not already exist
def generate_keys():
    # if both key files already exist, do not create new ones
    # this keeps the same key pair for future signing and verification
    if os.path.exists("private_key.pem") and os.path.exists("public_key.pem"):
        return

    # creates a new RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # gets the matching public key from the private key
    public_key = private_key.public_key()

    # saves the private key to a PEM file
    with open("private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # saves the public key to a PEM file
    with open("public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print("RSA keys generated.")
    logging.info("RSA key pair generated")


# signs the file contents using the private key
def sign_file(file_path: str):
    # make sure the RSA keys exist before trying to sign
    generate_keys()

    # load the private key from the saved PEM file
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    # read the file contents as bytes
    with open(file_path, "rb") as f:
        file_data = f.read()

    # create a digital signature for the file data using RSA + SHA-256
    signature = private_key.sign(
        file_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # save the signature in a separate file with .sig added to the end
    signature_file = file_path + ".sig"
    with open(signature_file, "wb") as f:
        f.write(signature)

    print(f"Signature saved to: {signature_file}")
    logging.info(f"File signed: {file_path}")


# verifies the file using the public key and saved signature
def verify_signature(file_path: str):
    # check that the public key exists, since it is needed for verification
    if not os.path.exists("public_key.pem"):
        print("Public key not found.")
        logging.warning(f"Signature verification failed, missing public key: {file_path}")
        return

    # the signature is expected to be stored in a separate .sig file
    signature_file = file_path + ".sig"

    # check that the original file exists
    if not os.path.exists(file_path):
        print("Signature file not found.")
        logging.warning(f"Signature verification failed, missing signature: {file_path}")
        return

    # load the public key from the PEM file
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    # read the original file contents
    with open(file_path, "rb") as f:
        file_data = f.read()

    # read the saved digital signature
    with open(signature_file, "rb") as f:
        signature = f.read()

    try:
        # verify that the signature matches the file contents
        # if the file was changed, verification will fail
        public_key.verify(
            signature,
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature verified: file is authentic.")
        logging.info(f"Signature verified: {file_path}")

    except Exception:
        # if verification fails, the file may have been changed
        # or the signature may not belong to this file
        print("WARNING: Signature verification failed.")
        logging.warning(f"Signature verification failed: {file_path}")