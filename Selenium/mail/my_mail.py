# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from selenium.webdriver.common.by import By
from pymongo import MongoClient

client = MongoClient('127.0.0.1:27017')
db_mail = client.db_mail

def get_href_from_message(message_list):
    for k, i in enumerate(message_list):
        try:
            message_list[k]=i.get_attribute('href')
        except Exception as e:
            pass
            print(e)
    return message_list

driver = webdriver.Chrome('./chromedriver')
driver.get('https://mail.ru/')
assert 'Mail.ru' in driver.title

login_password = driver.find_element_by_id('mailbox:login')
login_password.send_keys('study.ai_172@mail.ru')
login_password.send_keys(keys.Keys.ENTER)
time.sleep(1)
login_password = driver.find_element_by_id('mailbox:password')
login_password.send_keys('NewPassword172')
login_password.send_keys(keys.Keys.ENTER)

assert WebDriverWait(driver, 30).until(
    ec.presence_of_element_located((By.XPATH,"//a[contains(@class,'js-letter-list-item')]"))
    )

message_list = driver.find_elements_by_xpath("//a[contains(@class,'js-letter-list-item')]")
message_list = get_href_from_message(message_list)
temp_message_list = []
while len(message_list)>len(temp_message_list):
    temp_message_list = message_list
    last_message = driver.find_element_by_xpath("//a[contains(@class,'js-letter-list-item')][last()]")
    last_message.send_keys(keys.Keys.CONTROL + keys.Keys.END)
    time.sleep(1)
    message_list = driver.find_elements_by_xpath("//a[contains(@class,'js-letter-list-item')]")
    message_list = get_href_from_message(message_list)
    message_list.extend(temp_message_list)
    message_list = list(set(message_list))

for i in message_list:
    a_message = {}
    driver.get(i)
    message_title = WebDriverWait(driver, 60).until(
        ec.presence_of_element_located((By.TAG_NAME,'h2'))
        )
    
    message_date = driver.find_element_by_css_selector('div.letter__date')
    message_author = driver.find_element_by_css_selector('span.letter-contact')
    message_html_body = driver.find_element_by_xpath("//div[@class='html-fishing']")
    print(message_title.text,message_date.text,message_author.text,message_author.get_attribute('title'),'\n','*'*50)
    a_message['message_title'] = message_title.text
    a_message['message_date'] = message_date.text
    a_message['message_author'] = message_author.text
    a_message['message_author_address'] = message_author.get_attribute('title')
    a_message['message_html_body'] = message_html_body.text
    db_mail.test_mail.insert_one(a_message)
x = len(message_list)
print('В результате работы программы собрано', x,'сообщений', sep=' ')

driver.quit()