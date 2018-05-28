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

# Writes new RSA PGPkeys to file
# sk is saved in 'privkey.pem' in ASCII-armored pem format
# pk is saved in 'pubkey.pem' in ASCII-armored pem format
# @param: sk PGPkey
# @param: pk PGPkey.pubkey
def write_key_to_file(sk, pk):
    # Open FD
    privkey = open('privkey.pem', 'w')
    pubkey = open('pubkey.pem', 'w')
    
    # Write the keys
    privkey.write(str(sk))
    pubkey.write(str(pk))
    
    # Close FD
    privkey.close()
    pubkey.close()
    
# returns email of the first UID in the key
def get_email_from_key(pgpkey):
    return pgpkey.userids[0].email

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
# @return: pgp_m string
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
        digest.update(m[i:i+512].encode('utf-8'))
    return digest.digest()

# Verify MD5 hash
# @param: m string
# @param: h string
# @return: b boolean
def verify_md5_hash(m, h):
    digest = hashlib.md5()
    for i in range(0, len(m), 512):
        digest.update(m[i:i+512].encode('utf-8'))
    return digest.digest() == h

# Unit testing function
def unitTest():
    # Hash test
    assert (verify_md5_hash(b"Hello World!", md5_hash(b"Hello World!")))
    
    # Encryption test
    sk, pk = create_pgpkey("Max Mustermann", "max@mustermann.name")
    assert ("Hello World!" == decrypt(encrypt("Hello World!", pk), sk))
    
    # Write key to file test
    write_key_to_file(sk, pk)
    
    # File encryption test
    enc_file = encrypt_file("ui.PNG", pk)
    open("enc_ui", "w").write(enc_file)
    dec_file = decrypt_file("enc_ui", sk)
    open("dec_ui.PNG", "wb").write(dec_file)

# unitTest()
