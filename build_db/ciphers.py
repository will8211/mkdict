#!/usr/bin/env python3

import codecs

import blowfish


def encrypt(id_int):

    cipher = blowfish.Cipher(b"taro")

    id_str = str(id_int).zfill(8)
    id_bytes = bytes(id_str, "utf-8")
    encoded_bytes = cipher.encrypt_block(id_bytes)
    encoded_hex = codecs.encode(encoded_bytes, "hex")
    encoded_str = str(encoded_hex)[2:-1]

    return encoded_str


def decrypt(encoded_str):

    cipher = blowfish.Cipher(b"taro")

    decoded_bytes = bytes.fromhex(encoded_str)
    decoded_str = cipher.decrypt_block(decoded_bytes)
    decoded_int = int(decoded_str)

    return decoded_int


from time import time

start = time()

for i in range(0, 50):
    code = encrypt(i)
    print(code)
    decode = decrypt(code)

print("It took: " + str(time() - start) + " seconds.")
