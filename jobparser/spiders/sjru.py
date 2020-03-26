# # -*- coding: utf-8 -*-

import scrapy
import unicodedata
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem_sj



class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    search_string = input('Введите поисковый запрос для начала поиска\nвакансий на сайте superjob.ru\n')
    search_string_sj = unicodedata.normalize('NFKD','%20'.join(search_string.split()))
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords='+search_string_sj]
    def parse(self, response: HtmlResponse):
        try:
            next_page = response.xpath("//a[contains(@class,'f-test-link-Dalshe')]/@href").extract_first()
        except:
            pass
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        else:
            yield response
        vac_link = response.xpath("//div[contains(@class,'_3LJqf')]//@href").extract()
        for link_item in vac_link:
            global link
            link = link_item.split('?')[0]
            yield response.follow(link, callback=self.vacansy_parse)
    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract()[0]
        salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        currency = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/span[last()]/text()").get(default='₽')
        salary = unicodedata.normalize('NFKD','#'.join(salary)).split('#')
        yield JobparserItem_sj(name=name,salary=salary,currency=currency,link=link)