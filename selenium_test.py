#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/8/18 下午5:24
# @Author   : avery.wang
# @File     : selenium_test.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome()
print(driver.title)

driver.get('https://movie.douban.com/explore')
sleep(1)


for num in range(0,3):
    sleep(1)
    driver.find_element_by_xpath(
        '//*[@class="tool"]/div/label[{}]'.format(num + 1)).click()

sleep(2)
driver.close()









