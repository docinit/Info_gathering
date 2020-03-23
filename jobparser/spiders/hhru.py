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
        # client = MongoClient('127.0.0.1:27017')
        # vacancy_db = client['vacancy_db']
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
        # for k,i in enumerate(y):
        #     y[k] = unicodedata.normalize('NFKD',str(i)).replace('<','').split(' div')[0]
        # for k,i in enumerate(y):
        #     if y[k]==' ':
        #         y.pop(k)
        # removing_list = []
        # for k, i in enumerate(y):
        #     if i=='Element':
        #         if k+1<len(y) and y[k+1:k+3]==['Element','Element']:
        #             removing_list.extend([k+1,k+2])
        #     else:
        #         save_item = k-1
        #         try:
        #             removing_list.remove(save_item)
        #         except:
        #             pass
        # removing_list = sorted(list(set(removing_list)))
        # salary_list = ' '.join(y).split('Element Element')
        # salary_list[0]=salary_list[0].replace('Element ','')
        # salary_list[-1]=salary_list[-1].replace(' Element','')
        # for k,i in enumerate(salary_list):
        #     salary_list[k] = i.split(' ')
        #     if salary_list[k][0]=='':
        #         salary_list[k].pop(0)
        #     salary_list[k] = ' '.join(salary_list[k])
        # for k,i in enumerate(salary_list):
        #     salary_list[k] = i.split(' ')
        #     if salary_list[k][-1]=='':
        #         salary_list[k].pop(-1)
        #     salary_list[k] = ' '.join(salary_list[k])
        # for k,salary in enumerate(salary_list):
        #     if salary[0:2]=='до':
        #         max_salary = ''.join(salary.split(' ')[:-1]).replace('до','')
        #         currency = salary.split(' ')[-1]
        #         min_salary = np.nan
        #     elif salary[0:2]=='от':
        #         min_salary = ''.join(salary.split(' ')[:-1]).replace('от','')
        #         currency = salary.split(' ')[-1]
        #         max_salary = np.nan
        #     elif '-' in salary:
        #         min_salary = ''.join(salary.split('-')[0].split(' '))
        #         currency = salary.split('-')[-1].split(' ')[-1]
        #         max_salary = ''.join(salary.split('-')[1].split(' ')[:-1])
        #     else:
        #         min_salary = np.nan
        #         max_salary = np.nan
        #         currency = ''
        #     vacancy_db.head_hunter.update_one({"vac_link":vac_link[k].split('?')[0]},\
        #                                       {"$set":{'vacancy_name':vac_name[k],\
        #                                                 'min_salary':min_salary,
        #                                                 'max_salary':max_salary,
        #                                                 'currency':currency,
        #                                                 'vac_link':vac_link[k].split('?')[0]
        #                                                 }},upsert=True)
        yield JobparserItem_hh(vac_name=vac_name,vac_link=vac_link,y=y)
            