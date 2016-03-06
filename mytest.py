#!/usr/bin/env python
import subprocess
while True:
	try:
		print("\033[92m{}\033[00m" .format("Start tests\n"))
		subprocess.call("rm -rf coverage", shell=True)
		subprocess.call("coverage erase", shell=True)
		ret = subprocess.call("coverage run manage.py test --visible -v 3 --failfast", shell=True)
		if ret==0:
			for x in range(0, 100):
				print("\033[92m{}\033[00m" .format("Great success!! Praise the Gods!"))
			break
		for x in range(0, 100):
			print("\033[91m{}\033[00m" .format("Ei onnaa"))
		print("\n");
	except:
		raise