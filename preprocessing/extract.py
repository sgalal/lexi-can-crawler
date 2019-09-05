#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import re
import json

d = []

with open('preprocessing/classified.php.txt', encoding='big5hkscs') as f:
	for line in re.finditer(r'<a href="search.php\?q=([%0-9A-Za-z_]+)">(.)</a>', f.read()):
		word = line[2]
		url = line[1]
		d.append((word, url))

with open('preprocessing/data.json', 'w') as fout:
	print(json.dumps(d, ensure_ascii=False, sort_keys=True).replace(', ', '\n, '), file=fout)
