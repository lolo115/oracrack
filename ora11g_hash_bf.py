#!/usr/bin/python

import hashlib
import binascii as ba
import sys
import os

if len(sys.argv) != 4:
        print ("ERROR")
        print ("---------------------------------------------------------------------------")
        print ("Usage:")
        print (sys.argv[0]+" <DICTIONARY FILE> <USERNAME> <10G_PASSWORD_HASH>")
        sys.exit(1)

print ("DICTFILE = "+sys.argv[1])
print ("USERNAME = "+sys.argv[2])
print ("HASH     = "+sys.argv[3])

dictfile=sys.argv[1]
username=sys.argv[2]
submitted_hash=sys.argv[3]
hash_digest=submitted_hash[0:40].upper()
hash_salt=submitted_hash[40:60].upper()


if not os.path.isfile(dictfile):
        print ("ERROR: Dictionary file: "+dictfile+" is not a regular file")
        sys.exit(1)

f=open(dictfile, "r")
for line in f:
        p2test=line.strip('\n')
	source1_to_hash=p2test+ba.unhexlify(hash_salt)        
        sha1_hash1=hashlib.sha1(source1_to_hash).hexdigest()
#	print ("USERNAME = "+username+" - PASSWORD = "+p2test+" - S:"+sha1_hash1.upper()+hash_salt)

        if sha1_hash1.upper()+hash_salt == submitted_hash.upper():
                print ("PASSWORD FOUND FOR USER "+username+" !!! PASSWORD IS: "+p2test)
		sys.exit(0)
print("Password not found")


