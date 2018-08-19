#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/8/19 下午3:52
# @Author   : avery.wang
# @File     : ZhiLianCrawl.py

import re
import pymysql
from time import  sleep
from urllib import (request,error,parse)
from bs4 import BeautifulSoup
from threading import Thread
import ssl


headers = {
    'Host': 'sou.zhaopin.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

}





job_loc_list = ['北京', '上海', '广州', '深圳', '天津', '武汉', '西安', '成都', '大连', '长春', '沈阳', '南京'
                '济南', '青岛', '杭州', '苏州', '无锡', '宁波', '重庆', '郑州', '长沙', '福州', '厦门', '哈尔滨'
                '石家庄', '合肥', '惠州']

class ZLSpider(object):

    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.url_base = 'https://sou.zhaopin.com?'
        self.conn = pymysql.connect('localhost','root','','python_master')
        self.cur = self.conn.cursor()
        self.html_pool = []
        self.parse_pool = []

    #接受工作名称关键字
    @property
    def job_name_cmd_get(self):
        return self._job_name

    @job_name_cmd_get.setter
    def job_name_cmd_get(self, job_name_input):
        if not isinstance(job_name_input,str):
            raise ValueError('请输入正确的关键词字符串')
        self._job_name = job_name_input

    #接受输入的工作地点
    @property
    def job_loc_cmd_get(self):
        return self._job_loc

    @job_loc_cmd_get.setter
    def job_loc_cmd_get(self, job_loc_input):
        if not isinstance(job_loc_input, str):
            raise ValueError('请输入正确的关键词字符串')

        if job_loc_input not in job_loc_list:
            print('请输入主要的城市')
        self._job_loc = job_loc_input

    def url_cook(self):
        url_crawl = self.url_base + 'jl=538' + '&kw='+ parse.quote(self._job_name) + '&kt=3' + '&p={}'
        return url_crawl

    def html_crawl(self, url_crawl):
        try:
            response = request.Request(url_crawl,headers=headers)
            html_requested = request.urlopen(response)
            html_decoded = html_requested.read().decode('utf-8')
            self.html_pool.append(html_decoded)
            print(html_decoded)
            sleep(3)
        except error.HTTPError as e:
            if hasattr(e,'code'):
                print(e.code)

        except error.URLError as e:
            if hasattr(e,'reason'):
                print(e.reason)


    def html_parse(self, html_decoded):

        job_fb = []
        job_name = []
        soup = BeautifulSoup(html_decoded,'lxml')
        soup.find('div', class_='listContent')
        print(soup.string)








    def job_info_store(self, job_info):

        for elem in job_info:
            print('111')

    def run(self):
        self.job_name_cmd_get = input('请输入工作名称')
        url_list = []
        html_thread_object = []

        #1-4页内容
        for x in range(1,2):
            url_list.append(self.url_cook().format(x))
            t = Thread(target=self.html_crawl, args=(url_list[x-1],), name='Crawl_Thread')
            html_thread_object.append(t)

        for elem in html_thread_object:
            elem.start()


        for elem in html_thread_object:
            elem.join()

        for num in range(0,len(self.html_pool)):
            self.html_parse(self.html_pool[num])
            print('------网页解析完毕------')
            self.job_info_store(self.parse_pool[num])
            print('------数据库存储完毕------')



if __name__ == '__main__':
    spider = ZLSpider()
    spider.run()
