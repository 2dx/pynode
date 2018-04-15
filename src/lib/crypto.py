#!/user/bin/env python
# -*- coding: utf-8 -*-

import base64
import hashlib
import sys
import struct
import binascii
from . import const

import nacl.encoding
import nacl.signing
import nacl.hash

def b2hex(b):
	return nacl.encoding.HexEncoder.encode(b).decode()

def hex2b(h):
	return nacl.encoding.HexEncoder.decode(h)

def b2int(b):
	return struct.unpack('<I', b)[0]

def int2b(i):
	return struct.pack('<I', i)

def b2long(b):
	return struct.unpack('<q', b)[0]

def long2b(l):
	return struct.pack('<q', l)

def b2string(b):
	return b.decode('utf-8')

def string2b(s):
	return s.encode('utf-8')

def int2hex(i):
	return b2hex(int2b(i))

def sk():
	sk = nacl.signing.SigningKey.generate()
	return sk.encode(encoder=nacl.encoding.HexEncoder).decode()

def sk2pk(sk):
	sk = sk.encode()
	sk = nacl.signing.SigningKey(sk, encoder=nacl.encoding.HexEncoder)
	pk = sk.verify_key
	return pk.encode(encoder=nacl.encoding.HexEncoder).decode()

def pk2addr(pk):
	pk = pk.encode()
	sha512HASHER = nacl.hash.sha512
	sha256HASHER = nacl.hash.sha256
	pk = hex2b(pk)
	digest = sha512HASHER(pk, encoder=nacl.encoding.HexEncoder)
	ripemd160HASHER = hashlib.new('ripemd160')
	ripemd160HASHER.update(hex2b(digest.decode()))
	digest = ripemd160HASHER.digest()
	if const.NODE.VERSION == const.VERSION.MAIN:
		digest = b'\x64' + digest
	elif const.NODE.VERSION == const.VERSION.TEST:
		digest = b'\x98' + digest
	digestHash = sha256HASHER(digest, encoder=nacl.encoding.HexEncoder)
	checksum = hex2b(digestHash[0:8].decode()) # 4byte
	address = base64.b32encode(digest + checksum)
	return address.decode('utf-8')

def sign(mess, sk):
	sk = nacl.signing.SigningKey(sk, encoder=nacl.encoding.HexEncoder)
	mess = hex2b(mess)
	signed = sk.sign(mess)
	return b2hex(signed[:64])

def verify(sig, mess, pk):
	pk = nacl.signing.VerifyKey(pk, encoder=nacl.encoding.HexEncoder)
	mess = hex2b(mess)
	sig = hex2b(sig)
	signed = sig+mess
	try:
		return pk.verify(signed) == mess
	except:
		return False

def sha256_from_byte(b):
	sha256HASHER = nacl.hash.sha256
	digest = sha256HASHER(b, encoder=nacl.encoding.HexEncoder)
	return digest

def sha256_from_hex(hex):
	b = hex2b(hex)
	return sha256_from_byte(b)

