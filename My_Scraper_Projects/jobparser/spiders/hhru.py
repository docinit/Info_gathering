# # -*- coding: utf-8 -*-

import scrapy
from scrapy.http import HtmlResponse
from lxml import html
from jobparser.items import JobparserItem_hh
import unicodedata
from scrapy.loader import ItemLoader




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
        vac_link = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href")
        for link_item in vac_link:
            yield response.follow(link_item, callback=self.vacansy_parse)
    def vacansy_parse(self, response: HtmlResponse):
        loader = ItemLoader(JobparserItem_hh(), response = response)
        loader.add_xpath('vac_name',"//h1[@class='bloko-header-1']/text()")
        loader.add_value('vac_url', response.url)
        loader.add_xpath('salary',"//p[@class='vacancy-salary']//text()")
        yield loader.load_item()
            