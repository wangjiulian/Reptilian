#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/8/19 下午8:29
# @Author   : avery.wang
# @File     : Onepiece_crawl.py

import re
import random
import queue
import requests

from time import sleep
from bs4 import BeautifulSoup
from threading import Thread


class OnePiece(object):
    def __init__(self):
        self.url = 'http://op.hanhande.com/shtml/op_wz/list_2602_{}.shtml'
        self.q = queue.Queue()
        self.picture_link = []



    def html_parse(self, num):

        try:
            url_make = self.url.format(num)
            html = requests.get(url_make,timeout=10)
            soup = BeautifulSoup(html.content,'lxml')
            url_tag = soup.find_all('ul',class_='spic pic1')
            soup1 = BeautifulSoup(str(url_tag[0]),'lxml')

            for counter, li_tag in enumerate(soup1.find_all('li')):
                soup2 = BeautifulSoup(str(li_tag), 'lxml')
                a_tag = soup2.find_all('a')
                href_list = re.findall(re.compile('href="(.+?)"'),str(a_tag))
                if len(href_list) !=0:
                    print('第' + str(num) + '页:-----第' + str(counter + 1)
                          +'个链接：' + href_list[0] + '------')
                    self.q.put(href_list[0])
                    sleep(random.randint(2,3))
                    if self.q.qsize() == 4:
                        break

        except:
            pass

    def picture_parse(self):
        try:
            sub_url = self.q.get()
            htm1 = requests.get(sub_url)

            s = BeautifulSoup(htm1.content,'lxml')
            div_t = s.find('div',class_='show')
            s1 = BeautifulSoup(str(div_t),'lxml')
            h2_t = s1.find('h2')
            title_str = h2_t.string
            index_1 = title_str.index('/')
            total_page = title_str[index_1 + 1:-1]

            if(int(total_page) == 1):
                self.picture_link_add(sub_url)
            else:
                sub_url_base = sub_url[:-6]
                for page in range(1, int(total_page) + 1):
                    sub_url_new = sub_url_base + '_' + str(page) + '.shtml'
                    self.picture_link_add(sub_url_new)
                    sleep(random.randint(2, 3))
        except:
            pass


    def picture_link_add(self,sub_url_new):
        try:
            html2 = requests.get(sub_url_new)
            if html2.status_code == 200:
                soup = BeautifulSoup(html2.content, 'lxml')
                div_tag = soup.find_all('div', id='pictureContent');
                soup1 = BeautifulSoup(str(div_tag[0]), 'lxml')
                for img_tag in soup1.find_all('img', src=re.compile('(.+?)')):
                    soup3 = BeautifulSoup(str(img_tag), 'lxml')
                    if soup3.img['src'] is not None:
                        self.picture_link.append(soup3.img['src'])
                        print(str('-----' + soup3.img['alt'] + '链接：') + str(soup3.img['src'] + '----'))
                        sleep(random.randint(2, 3))


            else:
                pass
        except:
            pass


    def picture_store(self):

        try:
            for couter, link in enumerate(self.picture_link):
                html3 = requests.get(link)
                picture_path = '/Work/Python/onepiec_picture/pic'+str(couter + 1) +'.jpg'
                with open(picture_path,'wb') as f:
                    f.write(html3.content)
                print('图片:'+link + '下载成功-----')
        except :
            pass

    def main(self):
        page_num = 2
        thread_0 = []
        for i in range(1,page_num):
            t = Thread(target=self.html_parse,args=(i,), name='Thread-0')
            thread_0.append(t)

        for i in range(len(thread_0)):
             thread_0[i].start()

        for i in range(len(thread_0)):
             thread_0[i].join()


        thread_1 = []

        for i in range(self.q.qsize()):
            t1 = Thread(target=self.picture_parse, args=(), name='Thread-1')
            thread_1.append(t1)

        for i in range(len(thread_1)):
            thread_1[i].start()

        for i in range(len(thread_1)):
            print('thread---' + str(i) +'开始')
            thread_1[i].join()

        self.picture_store()

        # thread_2 = []
        # for num in range(len(self.picture_link)):
        #     t2 = Thread(target=self.picture_store, args=(num,), name='Thread-2')
        #     thread_2.append(t2)
        #
        # for i in range(len(thread_2)):
        #     thread_2[i].start()
        #
        # for i in range(len(thread_2)):
        #     thread_2[i].join()



if __name__ == '__main__':
    spider = OnePiece()
    spider.main()











