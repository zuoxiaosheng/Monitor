#!/usr/bin/python

import os
import subprocess
import time
from config import db
utc = int(time.time())
CWD = '/root/Monitor/'
scripts = os.listdir(CWD + 'scripts/')

documents = {}
for node in open(CWD + 'nodes'):
	[ip, hostname] = node.rstrip('\r\n').split(' ')[:2]
	documents[ip] = {'agent': ip, 'hostname': hostname, 'unixSecondsUTC': utc}

for item in scripts:
	item = CWD + 'scripts/' + item
	sp = subprocess.Popen(item, stdout=subprocess.PIPE)
	lines = sp.stdout.readlines()
	for line in lines:
		d = eval(line)
		for key in d:
			documents[d['agent']][key] = d[key]

if documents:
	for key in documents:
		db['ext'].insert(documents[key])
	documents = None
