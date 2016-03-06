#!/usr/bin/env python
import subprocess

while True:
	print("\033[01;42m")
	try:
		raise
		#subprocess.call('coverage erase')
		ret = subprocess.call('coverage run mange.py test -v 3 --failfast')
		if ret == 0:
			break;
		else :
			raise
	except:
		print("\033[01;41m")
		pass