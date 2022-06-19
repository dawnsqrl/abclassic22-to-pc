from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad


# Encrypt data with AES
def encrypt(data: str):
    key = bytes.fromhex('3434695559356154726c61596f6574396c6170526c614b3145686c6563356930')
    iv = bytes.fromhex('0' * 32)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
