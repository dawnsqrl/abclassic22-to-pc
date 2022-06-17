import base64
from Cryptodome.Cipher import AES


def encrypt(data):
    key = b'3434695559356154726c61596f6574396c6170526c614b3145686c6563356930'
    iv = b'\0'
    cipher = AES.new(key, AES.MODE_CBC, iv)
