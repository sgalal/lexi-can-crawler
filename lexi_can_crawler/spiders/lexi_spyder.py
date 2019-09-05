import json
import scrapy

class LexiSpider(scrapy.Spider):
    name = "lexi"

    def start_requests(self):
        # Read data
        with open('preprocessing/data.json') as f:
            data = json.loads(f.read())

        # Construct URL
        url_root = 'http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/search.php?q='

        for datum in data:
            ch, url = datum[0], datum[1]
            url_full = url_root + url
            yield scrapy.Request(url=url_full, callback=self.parse, meta={ 'character': ch })

    def parse(self, response):
        data_rows = response.css('form > table:first-child > tr:not(:first-child)')

        for data_row in data_rows:
            explanation = data_row.css('td:nth-child(6)')

            # Check if it is an variant pronunciation (異讀字)
            is_variant_pronun = '的異讀字' in explanation[0].get()
            if not is_variant_pronun:
                character = response.meta['character']
                initial = data_row.css('td:nth-child(1) > font[color="red"]::text').get()
                rhyme = data_row.css('td:nth-child(1) > font[color="green"]::text').get()
                tone = data_row.css('td:nth-child(1) > font[color="blue"]::text').get()

                yield \
                    { 'character': character
                    , 'initial': initial
                    , 'rhyme': rhyme
                    , 'tone': tone
                    , 'explanation': self.get_explanation(explanation)
                    }

    def get_explanation(self, response):
        basic_words = ''.join(response.css('div[nowrap]::text').extract())
        more_words = ''.join(response.css('div[id$="_detial"]::text').extract())
        return self.split_commas(basic_words) + self.split_commas(more_words)

    def split_commas(self, s):
        '''
        >>> split_commas('不能, 照片,必修')
        ['不能', '照片', '必修']
        >>> split_commas(None)
        []
        '''
        return [] if not s else [x.strip() for x in s.split(',') if x.strip()]
