#!/usr/bin/python
import itertools, sys

def cc(s):
	return (''.join(t) for t in itertools.product(*zip(s.lower(), s.upper())))

for item in list(cc(sys.argv[1])):
	print(item);

#print (list(cc('laurent')))



