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
            for k,i in enumerate(item['y']):
                item['y'][k] = unicodedata.normalize('NFKD',str(i)).replace('<','').split(' div')[0]
            for k,i in enumerate(item['y']):
                if item['y'][k]==' ':
                    item['y'].pop(k)
            removing_list = []
            for k, i in enumerate(item['y']):
                if i=='Element':
                    if k+1<len(item['y']) and item['y'][k+1:k+3]==['Element','Element']:
                        removing_list.extend([k+1,k+2])
                else:
                    save_item = k-1
                    try:
                        removing_list.remove(save_item)
                    except:
                        pass
            removing_list = sorted(list(set(removing_list)))
            salary_list = ' '.join(item['y']).split('Element Element')
            salary_list[0]=salary_list[0].replace('Element ','')
            salary_list[-1]=salary_list[-1].replace(' Element','')
            for k,i in enumerate(salary_list):
                salary_list[k] = i.split(' ')
                if salary_list[k][0]=='':
                    salary_list[k].pop(0)
                salary_list[k] = ' '.join(salary_list[k])
            for k,i in enumerate(salary_list):
                salary_list[k] = i.split(' ')
                if salary_list[k][-1]=='':
                    salary_list[k].pop(-1)
                salary_list[k] = ' '.join(salary_list[k])
            for k,salary in enumerate(salary_list):
                if salary[0:2]=='до':
                    max_salary = ''.join(salary.split(' ')[:-1]).replace('до','')
                    currency = salary.split(' ')[-1]
                    min_salary = np.nan
                elif salary[0:2]=='от':
                    min_salary = ''.join(salary.split(' ')[:-1]).replace('от','')
                    currency = salary.split(' ')[-1]
                    max_salary = np.nan
                elif '-' in salary:
                    min_salary = ''.join(salary.split('-')[0].split(' '))
                    currency = salary.split('-')[-1].split(' ')[-1]
                    max_salary = ''.join(salary.split('-')[1].split(' ')[:-1])
                else:
                    min_salary = np.nan
                    max_salary = np.nan
                    currency = ''
                link = item['vac_link'][k].split('?')[0]
                name = item['vac_name'][k]
                iitem = {'link':link,
                         'name':name,
                         'max_salary':max_salary,
                         'min_salary':min_salary,
                         'currency':currency}
                collection = self.vacancy_db[spider.name]
                collection.insert_one(iitem)
        ##### HH
        if spider.name == 'sjru':
            currency = item['currency']
            if item['salary'][0]=='до':
                max_salary = item['salary'][2]
                min_salary = np.nan
            elif item['salary'][0]=='от':
                min_salary = item['salary'][2]
                max_salary = np.nan
            elif '—' in ''.join(item['salary']):
                min_salary = ''.join(item['salary']).split('—')[0]
                max_salary = ''.join(item['salary']).split('—')[1]
            elif str(item['salary'][0])[0:10]=='По договор':
                min_salary = np.nan
                max_salary = np.nan
                currency = ''
            elif len(item['salary'])>=2:
                min_salary =''.join(item['salary'][0])
                max_salary = ''.join(item['salary'][1])
            else:
                min_salary = item['salary'][0]
                max_salary = item['salary'][0]
            link = item['link']
            name = item['name']
            iitem = {'link':link,
                     'name':name,
                     'max_salary':max_salary,
                     'min_salary':min_salary,
                     'currency':currency}
        
            collection = self.vacancy_db[spider.name]
            collection.insert_one(iitem)
        return item    
    