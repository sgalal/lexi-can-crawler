#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

with open('data3.json') as f:
	data = json.loads(f.read())

all_chars = {datum['ch'] for datum in data}

d = []

for datum in data:
	ch = datum['ch']

	initial = datum['initial'] or ''
	rhyme = datum['rhyme']
	tone = datum['tone']

	words = [word for word in datum['words'] if all(ch in all_chars for ch in word)]

	d.append( \
		{ 'ch': ch
		, 'initial': initial
		, 'rhyme': rhyme
		, 'tone': tone
		, 'words': words
		})

with open('data.json', 'w', encoding='utf8') as fout:
	print(json.dumps(d, ensure_ascii=False, sort_keys=True).replace('}, ', '}\n,'), file=fout)
