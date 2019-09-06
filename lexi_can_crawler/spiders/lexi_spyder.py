# -*- coding: utf-8 -*-

import json
import scrapy

class LexiSpider(scrapy.Spider):
	name = "lexi"

	def start_requests(self):
		# Read data
		with open('data2.json') as f:
			data = json.loads(f.read())

		# Construct URL
		url_root = 'http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/search.php?q='

		for datum in data:
			ch, url = datum[0], datum[1]
			url_full = url_root + url
			yield scrapy.Request(url=url_full, callback=self.parse, meta={ 'character': ch })

	def parse(self, response):
		def check_is_variant_pron(data_td_6):
			'''Check if it is an variant pronunciation (異讀字)
			'''
			explanation = data_td_6.css('font[color="forestgreen"]').get()
			return explanation and '的異讀字' in explanation

		def get_words(ch, data_td_6):
			'''Get all words of a data row
			'''
			def split_commas(s):
				'''
				>>> split_commas('不能, 照片,必修')
				['不能', '照片', '必修']
				>>> split_commas(None)
				[]
				'''
				return [] if not s else [x.strip() for x in s.split(',') if x.strip()]

			basic_words = split_commas(''.join(data_td_6.css('div[nowrap]::text').extract()))
			more_words = split_commas(''.join(data_td_6.css('div[id$="_detial"]::text').extract()))
			all_words = basic_words + more_words
			filtered_all_words = [x for x in all_words if ch in x]  # Dealing with error data like '蜮'
			return filtered_all_words

		ch = response.meta['character']
		data_rows = response.css('form > table:first-child > tr:not(:first-child)')

		for data_row in data_rows:
			data_td_6 = data_row.css('td:nth-child(6)')

			is_variant_pron = check_is_variant_pron(data_td_6)
			words = get_words(ch, data_td_6)

			if words or not is_variant_pron:
				initial = data_row.css('td:nth-child(1) > font[color="red"]::text').get()
				rhyme = data_row.css('td:nth-child(1) > font[color="green"]::text').get()
				tone = data_row.css('td:nth-child(1) > font[color="blue"]::text').get()

				yield \
					{ 'ch': ch
					, 'initial': initial
					, 'rhyme': rhyme
					, 'tone': tone
					, 'words': words
					}
