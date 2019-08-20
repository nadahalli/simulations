from Crypto import Random
from Crypto.Util import number
import hashlib
from Crypto.Cipher import AES
import os
import binascii

rsa_key = number.long_to_bytes(number.getRandomInteger(2048))
aes_key = binascii.unhexlify(hashlib.blake2b(rsa_key, digest_size = 16).hexdigest())

iv = Random.new().read(AES.block_size)
cypher = AES.new(aes_key, AES.MODE_CFB, iv)

# Generated using something like: https://github.com/libbitcoin/libbitcoin-explorer/wiki/How-to-Spend-From-a-Multisig-Address

raw_tx_with_sig = "01000000010506344de69d47e432eb0174500d6e188a9e63c1e84a9e8796ec98c99b7559f701000000fdfd00004730440220695a28c42daa23c13e192e36a20d03a2a79994e0fe1c3c6b612d0ae23743064602200ca19003e7c1ce0cecb0bbfba9a825fc3b83cf54e4c3261cd15f080d24a8a5b901483045022100aa9096ce71995c24545694f20ab0482099a98c99b799c706c333c521e51db66002206578f023fa46f4a863a6fa7f18b95eebd1a91fcdf6ce714e8795d902bd6b682b014c69522102b66fcb1064d827094685264aaa90d0126861688932eafbd1d1a4ba149de3308b21025cab5e31095551582630f168280a38eb3a62b0b3e230b20f8807fc5463ccca3c21021098babedb3408e9ac2984adcf2a8e4c48e56a785065893f76d0fa0ff507f01053aeffffffff01c8af0000000000001976a91458b7a60f11a904feef35a639b6048de8dd4d9f1c88ac00000000"

encrypted_msg = iv + cypher.encrypt(bytes.fromhex(raw_tx_with_sig))

iv = encrypted_msg[:16]
cipher = AES.new(aes_key, AES.MODE_CFB, iv)
decrypted_msg = cipher.decrypt(encrypted_msg[16:])

raw_tx_with_sig_decrypted = decrypted_msg.hex()
print(raw_tx_with_sig == raw_tx_with_sig_decrypted)


