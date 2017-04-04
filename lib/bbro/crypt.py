import base64
import hashlib
import bcrypt
from Crypto.Cipher import AES
from Crypto import Random

class AESCipher(object):

    def __init__(self, key):
        self.key = key

    def derive_key_and_iv(self, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + self.key + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]

    def encrypt(self, in_file, out_file, key_length=32):
        bs = AES.block_size
        salt = Random.new().read(bs - len('Salted__'))
        key, iv = derive_key_and_iv(salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out_file.write('Salted__' + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * bs)
            if len(chunk) == 0 or len(chunk) % bs != 0:
                padding_length = (bs - len(chunk) % bs) or bs
                chunk += padding_length * chr(padding_length)
                finished = True
            out_file.write(cipher.encrypt(chunk))

    def decrypt(self, in_file, out_file, key_length=32):
        bs = AES.block_size
        salt = in_file.read(bs)[len('Salted__'):]
        key, iv = derive_key_and_iv(salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                try:
                    padding_length = ord(chunk[-1])
                except:
                    padding_length = ord('')
                chunk = chunk[:-padding_length]
                finished = True
            out_file.write(chunk)

class HashDigester(object):

    def __init__(self, bufsize=2*20):
        self.BUF_SIZE = bufsize

    def sha256_hash(self, file):
        self.sha256 = hashlib.sha256()
        f = open(file, 'rb')
        while 1:
            data = f.read(self.BUF_SIZE)
            if not data:        # to prevent full memory
                break
            self.sha256.update(data)
        f.close()
        return sha256.hexdigest()