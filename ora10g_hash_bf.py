# Created by Laurent Leturgez (leturgezl[a@t]gmail.com)
# Script under GPL License.

import hashlib
from Crypto.Cipher import DES
from binascii import hexlify, unhexlify
from passlib.crypto.des import des_encrypt_block
import sys
import os

ORACLE10_MAGIC = b"\x01\x23\x45\x67\x89\xAB\xCD\xEF"

def des_cbc_encrypt(key, value, iv=b'\x00' * 8, pad=b'\x00'):
    value += pad * (-len(value) % 8) 
    hash = iv # start things off
    for offset in xrange(0,len(value),8):
        chunk = xor_bytes(hash, value[offset:offset+8])
        hash = des_encrypt_block(key, chunk)
    return hash

def calc_checksum(user, secret):
    input = (user+secret).upper().encode("utf-16-be")
    hash = des_cbc_encrypt(ORACLE10_MAGIC, input)
    hash = des_cbc_encrypt(hash, input)
    return hexlify(hash).decode("ascii").upper()

def int_to_bytes(value, count):
    return unhexlify(('%%0%dx' % (count<<1)) % value)

def bytes_to_int(value):
    return int(hexlify(value),16)

def xor_bytes(l, r):
    return int_to_bytes(bytes_to_int(l) ^ bytes_to_int(r), len(l))

if len(sys.argv) != 4:
	print ("ERROR")
	sys.exit(1)

print ("DICTFILE = "+sys.argv[1])
print ("USERNAME = "+sys.argv[2])
print ("HASH     = "+sys.argv[3])

dictfile=sys.argv[1]
username=sys.argv[2]
submitted_hash=sys.argv[3].upper()

if not os.path.isfile(dictfile):
	print ("ERROR: Dictionary file: "+dictfile+" is not a regular file")
	sys.exit(1)

f=open(dictfile, "r")
for line in f:
	p2test=line.strip('\n')
        if calc_checksum(username,p2test) == submitted_hash.upper():
		print ("PASSWORD FOUND FOR USER "+username+" !!! PASSWORD IS: "+p2test)
                print ("------")
		print ("Be careful, the found password is case unsensitive. The real password can include upper character(s)")
		print ("Now generate all combinations for this password and run ora11g_hash_bf.py script to find the case sensitive password")
		sys.exit(0)

print ("Password not found")


