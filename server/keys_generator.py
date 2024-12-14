#this file generate pablic and private key for the server and save them in files data/private_pem.pem and data/public_pem.pem. used only by the programer and not by the server itself

#RSA_cryptography.py
#Importing necessary modules
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify

check_msg=b"meseg"
#Generating private key (RsaKey object) of key length of 1024 bits
private_key = RSA.generate(1024)
#Generating the public key (RsaKey object) from the private key
public_key = private_key.publickey()
print(type(private_key), type(public_key))

#Converting the RsaKey objects to string 
private_pem = private_key.export_key().decode()
public_pem = public_key.export_key().decode()
print(type(private_pem), type(public_pem))
#Writing down the private and public keys to 'pem' files
with open('data/private_pem.pem', 'w') as pr:
    pr.write(private_pem)
with open('data/public_pem.pem', 'w') as pu:
    pu.write(public_pem)
    
#Importing keys from files, converting it into the RsaKey object   
pr_key = RSA.import_key(open('data/private_pem.pem', 'r').read())
pu_key = RSA.import_key(open('data/public_pem.pem', 'r').read())
print(type(pr_key), type(pu_key))

#Instantiating PKCS1_OAEP object with the public key for encryption
cipher = PKCS1_OAEP.new(key=pu_key)
#Encrypting the message with the PKCS1_OAEP object
cipher_text = cipher.encrypt(check_msg)
print(cipher_text,len(cipher_text))
#Instantiating PKCS1_OAEP object with the private key for decryption
decrypt = PKCS1_OAEP.new(key=pr_key)
#Decrypting the message with the PKCS1_OAEP object
decrypted_message = decrypt.decrypt(cipher_text)
print(decrypted_message,len(decrypted_message),len(check_msg))
