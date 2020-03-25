# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import unicodedata
import numpy as np


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.vacancy_db = client.vacancy_db
    def process_item(self, item, spider):
        ##### HH
        if spider.name == 'hhru':
            collection = self.vacancy_db[spider.name]
            salary = unicodedata.normalize('NFKD',''.join(item['salary'])).replace(' до вычета налогов','').replace(' на руки','')
            if ('до' in str(salary)) and ('от' in str(salary)):
                min_salary = ''.join(str(salary).split(' до ')[0]).replace('от ','')
                currency = str(salary).split(' ')[-1]
                max_salary = ''.join(str(salary).split(' до ')[1].split(' ')[0:2])
            elif str(salary)[0:2]=='до':
                max_salary = ''.join(str(salary).split(' ')[:-1]).replace('до','')
                currency = str(salary).split(' ')[-1]
                min_salary = np.nan
            elif str(salary)[0:2]=='от':
                min_salary = ''.join(str(salary).split(' ')[:-1]).replace('от','')
                currency = str(salary).split(' ')[-1]
                max_salary = np.nan
            elif '-' in str(salary):
                min_salary = ''.join(str(salary).split('-')[0].split(' '))
                currency = str(salary).split('-')[-1].split(' ')[-1]
                max_salary = ''.join(str(salary).split('-')[1].split(' ')[:-1])
            else:
                min_salary = np.nan
                max_salary = np.nan
                currency = ''
            link = item['vac_url']
            name = item['vac_name']
            iitem = {'link':link[0],
                     'name':name[0],
                     'max_salary':max_salary,
                     'min_salary':min_salary,
                     'currency':currency}
            collection.insert_one(iitem)
        ##### SJ
        if spider.name == 'sjru':
            currency = item['currency'][0]
            salary = unicodedata.normalize('NFKD',' '.join(item['salary'])).replace('   ',' ').replace('  ',' ')
            if str(salary)[0:3]=='до ':
                max_salary = unicodedata.normalize('NFKD',item['salary'][2])
                min_salary = np.nan
            elif str(salary)[0:3]=='от ':
                min_salary = unicodedata.normalize('NFKD',item['salary'][2])
                max_salary = np.nan
            elif '—' in str(salary):
                min_salary = str(salary).split('—')[0]
                max_salary = str(salary).split('—')[1]
            elif str(salary)[0:10]=='По договор':
                min_salary = np.nan
                max_salary = np.nan
                currency = ''
            elif len(str(salary).split(' ')) >= 4:
                min_salary = ''.join(str(salary).split(' ')[0:2])
                max_salary = ''.join(str(salary).split(' ')[2:])
            else:
                min_salary = ''
                max_salary = ''
                currency = ''
            link = item['vac_url'][0]
            name = item['name'][0]
            iitem = {'link':link,
                     'name':name,
                     'max_salary':max_salary,
                     'min_salary':min_salary,
                     'currency':currency}
            collection = self.vacancy_db[spider.name]
            collection.insert_one(iitem)
        return item    
    