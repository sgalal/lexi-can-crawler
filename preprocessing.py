#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import re
import json
import os.path

# Download classified character table

file_name1 = 'data1.txt'

if not os.path.exists(file_name1):
	source_url = 'http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/classified.php?st=0'
	urllib.request.urlretrieve(source_url, file_name1)

# Extract data

d = []

file_name2 = 'data2.json'

if not os.path.exists(file_name2):
	with open(file_name1, encoding='big5hkscs') as f:
		for line in re.finditer(r'<a href="search.php\?q=([%0-9A-Za-z_]+)">(.)</a>', f.read()):
			word = line[2]
			url = line[1]
			d.append((word, url))

	with open(file_name2, 'w') as fout:
		print(json.dumps(d, ensure_ascii=False, sort_keys=True).replace('], ', ']\n,'), file=fout)
