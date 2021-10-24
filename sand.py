import nacl.utils
from nacl.public import PrivateKey, Box

# Generate Bob's private key, which must be kept secret
skbob = PrivateKey.generate()

# Bob's public key can be given to anyone wishing to send
#   Bob an encrypted message
pkbob = skbob.public_key

# Alice does the same and then Alice and Bob exchange public keys
skalice = PrivateKey.generate()
pkalice = skalice.public_key
print(pkalice)

# Bob wishes to send Alice an encrypted message so Bob must make a Box with
#   his private key and Alice's public key
bob_box = Box(skbob, pkalice)  # Bob side
# Alice creates a second box with her private key to decrypt the message
alice_box = Box(skalice, pkbob)  # alice side

# This is our message to send, it must be a bytestring as Box will treat it
#   as just a binary blob of data.
message = b"Alice, Kill all humans"

encrypted = bob_box.encrypt(message)

# Decrypt our message, an exception will be raised if the encryption was
#   tampered with or there was otherwise an error.
plaintext = alice_box.decrypt(encrypted)
print(plaintext.decode('utf-8'))
