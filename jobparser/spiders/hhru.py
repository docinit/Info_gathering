# # -*- coding: utf-8 -*-

import scrapy
from scrapy.http import HtmlResponse
from lxml import html
from jobparser.items import JobparserItem_hh
import unicodedata




class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    search_string = input('Введите поисковый запрос для начала поиска\nвакансий на сайте hh.ru')
    search_string_hh = unicodedata.normalize('NFKD','+'.join(search_string.split())).replace('-','_')
    start_urls = ['https://spb.hh.ru/search/vacancy?text='+search_string_hh]
    def parse(self, response: HtmlResponse):
        try:
            next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        except:
            pass
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            yield response
        
        vac_name=response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/text()|//a[@data-qa='vacancy-serp__vacancy-title']/span/text()").extract()
        vac_link = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        y = html.fromstring(response.text).xpath("//div[@class = 'vacancy-serp-item__sidebar']|//div[@class = 'vacancy-serp-item__sidebar']//text()")
        yield JobparserItem_hh(vac_name=vac_name,vac_link=vac_link,y=y)
            