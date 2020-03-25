# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os
from urllib.parse import urlparse


class LeruaParserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.lerua_db = client.lerua_db

    def process_item(self, item, spider):
        item_to_add={}
        item_to_add['name_of_product'] = item['product_name']
        item_to_add['price'] = item['product_price']
        item_to_add['unit'] = item['product_unit']
        item_to_add['currency'] = item['product_currency']
        item_to_add['description'] = item['description']
        try:
            item_to_add['www_path'] = item['product_photos'][0]['url']
            item_to_add['local_path'] = item['product_photos'][0]['path']
        except TypeError as e:
            item_to_add['www_path'] = ''
            item_to_add['local_path'] = ''
            print(e)
        collection = self.lerua_db[spider.name]
        collection.insert_one(item_to_add)
        return


class LeruaPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        global path_to_item
        path_to_item = '/'.join(item['link_to_item'].replace('https://','').split('/')[:-1])
        if item["product_photos"]:
            for img in item["product_photos"]:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        return path_to_item + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results:
            item['product_photos'] = [itm[1] for itm in results if itm[0]]
        return item
