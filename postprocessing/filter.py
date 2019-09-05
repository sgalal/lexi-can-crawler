#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Dealing with error data like '蜮'

import json

with open('result.json') as f:
    data = json.loads(f.read())

d = []

for datum in data:
	ch = datum['character']
	r = (datum['initial'] or '') + datum['rhyme'] + datum['tone']
	wrds = [x for x in datum['explanation'] if ch in x]
	d.append({ 'character': ch, 'romanization': r, 'words': wrds })

with open('data.json', 'w') as fout:
	print(json.dumps(d, ensure_ascii=False, sort_keys=True).replace('}, ', '}\n,'), file=fout)
