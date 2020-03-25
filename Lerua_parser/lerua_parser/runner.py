#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# """
# Created on Tue Mar 24 12:19:39 2020

# @author: andrei
# """


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lerua_parser import settings
from lerua_parser.spiders.leruamerlin import LeruamerlinSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruamerlinSpider)
    process.start()
