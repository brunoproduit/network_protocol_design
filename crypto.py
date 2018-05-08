import pgpy, hashlib
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm
from Crypto.PublicKey import RSA
from Crypto import Random

#creates new PGPkeys (privatekey, publickey)
def create_pgpkey(name, email):
    key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
    uid = pgpy.PGPUID.new(name, email=email)
    key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
            ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
            compression=CompressionAlgorithm.ZIP)
    return key, key.pubkey

#returns pgpy.PGPkey
def read_key_from_file(filename):
    return pgpy.PGPKey.from_file(filename)

#returns pgpy.PGPMessage from a string
def create_pgp_message(message):
    return pgpy.PGPMessage.new(message, encoding="UTF8")

#returns pgpy.PGPMessage from a file
def create_pgp_message_from_file(filepath):
    return pgpy.PGPMessage.new(filepath, file=True)

#uses the public key to encrypt the message (pgpy.PGPMessage, pgpy.PGPKey -> pgpy.PGPMessage)
def encrypt(pgp_msg, pk):
    return pk.encrypt(pgp_msg)

#uses the private key to decrypt the message (pgpy.PGPMessage, pgpy.PGPKey -> pgpy.PGPMessage)
def decrypt(pgp_msg, sk):
    return sk.decrypt(pgp_msg)

#uses the masterkey (trusted 3rd party) to verify public key (takes paths as input)
def verify(masterkeyfile, pkfile):
    pk = read_key_from_file(pkfile)
    master = read_key_from_file(masterkeyfile)
    return master.verify(pk)

def md5_hash(message):
    dig = hashlib.md5()
    dig.update(message)
    return dig.digest()

def verify_md5_hash(message, hash):
    dig = hashlib.md5()
    dig.update(message)
    return dig.digest() == hash

#MD5 test
#hash = md5_hash("Hey")
#print(verify_md5_hash("Hey", hash))



secretkey, publickey = create_pgpkey("anne kala", "kala_ann@ttu.ee")

msg = create_pgp_message(b"Hey")

print(msg)

enc = encrypt(msg, publickey)
print(type(enc))

dec = decrypt(enc, secretkey)
print(dec)