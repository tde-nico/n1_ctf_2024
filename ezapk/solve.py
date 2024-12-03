from base64 import b64decode
from Crypto.Cipher import ARC4

b64 = 'iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A='
bdecoded = b64decode(b64)

def xor(a):
	b = bytearray(a)
	for i in range(len(b)):
		b[i] ^= rand() % 256
	return b

rand = lambda: 0xe9
key = bytes([rand() for _ in range(16)])
dec = ARC4.new(key).decrypt(bdecoded)
flag = xor(dec)
print(flag)

# N1CTF{MysT3r10us_C0d3_2024N1CTF!}
