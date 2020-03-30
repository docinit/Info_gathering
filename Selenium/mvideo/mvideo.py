# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient


def data_to_database(i):
    item = {}
    item['Category'] = json.loads(i.get_attribute('data-product-info'))['productCategoryName']    
    item['Vendor'] = json.loads(i.get_attribute('data-product-info'))['productVendorName']
    item['Name'] = json.loads(i.get_attribute('data-product-info'))['productName']
    item['Price'] = json.loads(i.get_attribute('data-product-info'))['productPriceLocal']
    db_shops.mvideo.insert_one(item)
    return


client = MongoClient('127.0.0.1:27017')
db_shops = client.db_shops

driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
driver.get('https://mvideo.ru')

html = driver.find_element_by_tag_name('html')
html.send_keys(Keys.PAGE_DOWN)

best_sellers_list = WebDriverWait(driver, 20).until(
    ec.presence_of_element_located((By.CSS_SELECTOR, 'div.sel-hits-block'))
    )
best_sellers_list = driver.find_element_by_css_selector('div.sel-hits-block')
goods_names = best_sellers_list.find_elements_by_css_selector('a.sel-product-tile-title')

next_button = best_sellers_list.find_element_by_css_selector('a.sel-hits-button-next')

while next_button:
    if next_button.get_attribute('class')=='next-btn sel-hits-button-next disabled':
        for i in goods_names[0:4]:
            data_to_database(i)
        break
    else:
        for i in goods_names[0:4]:
            data_to_database(i)
        next_button.click()
        time.sleep(5)
        best_sellers_list = driver.find_element_by_css_selector('div.sel-hits-block')
        next_button = best_sellers_list.find_element_by_css_selector('a.sel-hits-button-next')
        goods_names = best_sellers_list.find_elements_by_css_selector('a.sel-product-tile-title')

driver.close()