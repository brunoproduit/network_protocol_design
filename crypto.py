import pgpy, hashlib
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm,\
                           SymmetricKeyAlgorithm, CompressionAlgorithm

# creates new RSA PGPkeys (privatekey, publickey) 
# Size of RSA key is 4096
# @param: name string
# @param: email: string
# @return: (sk PGPkey, pk PGPkey.pubkey)
def create_pgpkey(name, email):
    key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
    uid = pgpy.PGPUID.new(name, email=email)
    key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA512, HashAlgorithm.SHA384, HashAlgorithm.SHA256, HashAlgorithm.SHA224],
            ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
            compression=CompressionAlgorithm.ZIP)
    return key, key.pubkey

# Import key from file
# @param: filename string
# @return: k PGPkey
def read_key_from_file(filename):
    return pgpy.PGPKey.from_file(filename)

# Create PGPMessage from string
# @param: m string
# @return: pgp_m PGPMessage
def create_pgp_message(m):
    return pgpy.PGPMessage.new(m, encoding="UTF8")

# Create PGPMessage from file
# @param: filename string
# @return: pgp_m PGPMessage
def create_pgp_message_from_file(filename):
    return pgpy.PGPMessage.new(filename, file=True)

# Encrypt string
# @param: m string
# @param: pk PGPkey.pubkey
# @return: pgp_m PGPMessage
def encrypt(m, pk):
    return str(pk.encrypt(create_pgp_message(m)))

# Encrypt file
# @param: filename string
# @param: pk PGPkey.pubkey
# @return: pgp_m string
def encrypt_file(filename, pk):
    return str(pk.encrypt(create_pgp_message_from_file(filename)))

# Decrypt string
# @param: c string
# @param: sk PGPkey
# @return: m string
def decrypt(c, sk):
    pgpy.PGPMessage.from_blob(c)
    return sk.decrypt(pgpy.PGPMessage.from_blob(c)).message

# Decrypt file
# @param: filename string
# @param: sk PGPkey
# @return: m string
def decrypt_file(filename, sk):
    return decrypt(open(filename, 'rb').read(), sk)

# uses the masterkey (trusted 3rd party) to verify public key
# Calculate MD5 hash
# @param: masterkeyfile string
# @param: pkfile string
# @return: verify boolean
def verify(masterkeyfile, pkfile):
    pk = read_key_from_file(pkfile)
    master = read_key_from_file(masterkeyfile)
    return master.verify(pk)

# Calculate MD5 hash
# @param: m string
# @return: h string
def md5_hash(m):
    digest = hashlib.md5()
    for i in range(0, len(m), 512):
        digest.update(m[i:i+512])
    return digest.digest()

# Verify MD5 hash
# @param: m string
# @param: h string
# @return: b boolean
def verify_md5_hash(m, h):
    digest = hashlib.md5()
    for i in range(0, len(m), 512):
        digest.update(m[i:i+512])
    return digest.digest() == h

# Unit testing function
# TODO test file encryption
def unitTest():
    # Hash test
    assert (verify_md5_hash(b"Hello World!", md5_hash(b"Hello World!")))
    
    # Encryption test
    sk, pk = create_pgpkey("Bruno Produit", "bruno@produit.name")
    assert ("Hello World!" == decrypt(encrypt("Hello World!", pk), sk))

unitTest()
