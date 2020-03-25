# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lerua_parser.items import LeruaParserItem
from scrapy.loader import ItemLoader

class LeruamerlinSpider(scrapy.Spider):
    name = 'leruamerlin'
    allowed_domains = ['leroymerlin.ru']
    search_query = None
    ### ДЛЯ ПРОИЗВОЛЬНОГО ПОИСКА ПО САЙТУ РАСКОММЕНТИРУЙТЕ СТРОКУ НИЖЕ    
    search_query = input('Введите строку для поиска товаров на сайте https://leroymerlin.ru/:\n')
    if search_query:
        start_urls = [f'https://leroymerlin.ru/search/?q={search_query}']
    else:
        start_urls = ['https://leroymerlin.ru/catalogue/shtukaturki/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        links = response.xpath("//a[@class='link-wrapper']/@href").extract()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for i in links:
            yield response.follow(i, callback=self.parse_links)

    def parse_links(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaParserItem(), response=response)
        loader.add_xpath('product_photos', "//source[@media='only screen and (min-width: 768px)']/@srcset")
        loader.add_xpath('product_name', "//h1[@class='header-2']/text()")
        loader.add_xpath('product_price', "//uc-pdp-price-view[@slot='primary-price']//span[@slot='price']/text()")
        loader.add_xpath('product_currency', "//uc-pdp-price-view[@slot='primary-price']//span[@slot='currency']/text()")
        loader.add_xpath('product_unit', "//uc-pdp-price-view[@slot='primary-price']//span[@slot='unit']/text()")
        loader.add_xpath('description', "///uc-pdp-section-vlimited//p/text()")
        loader.add_value('link_to_item', response.url)
        yield loader.load_item()
        
