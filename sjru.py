# # -*- coding: utf-8 -*-

import scrapy
import numpy as np
import unicodedata
from scrapy.http import HtmlResponse
from pymongo import MongoClient




class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    search_string = input('Введите поисковый запрос для начала поиска\nвакансий на сайте superjob.ru\n')
    search_string_sj = unicodedata.normalize('NFKD','%20'.join(search_string.split()))
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords='+search_string_sj]
    def parse(self, response: HtmlResponse):
        try:
            next_page = response.xpath("//a[contains(@class,'f-test-link-Dalshe')]/@href").extract_first()
            print(next_page)
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
        client = MongoClient('127.0.0.1:27017')
        vacancy_db = client['vacancy_db']
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract()[0]
        salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        currency = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/span[last()]/text()").get(default='₽')
        salary = unicodedata.normalize('NFKD','#'.join(salary)).split('#')
        print(salary,currency)
        if salary[0]=='до':
            max_salary = salary[2]
            min_salary = np.nan
        elif salary[0]=='от':
            min_salary = salary[2]
            max_salary = np.nan
        elif '—' in ''.join(salary):
            min_salary = ''.join(salary).split('—')[0]
            max_salary = ''.join(salary).split('—')[1]
        elif str(salary[0])[0:10]=='По договор':
            min_salary = np.nan
            max_salary = np.nan
            currency = ''
        elif len(salary)>=2:
            min_salary = ''.join(salary[0])
            max_salary =''.join(salary[1])
        else:
            min_salary = salary[0]
            max_salary = salary[0]
        print(name,'\n',min_salary,max_salary,currency)
        vacancy_db.super_job.insert_one({'vacancy_name':name,\
                                        'min_salary':min_salary,\
                                        'max_salary':max_salary,\
                                        'currency':currency,\
                                        'vac_link':link\
                                        })
        yield {link:{max_salary,min_salary}}