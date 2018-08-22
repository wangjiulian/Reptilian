
import urllib
from selenium import webdriver
import queue


class Anjuke_Spider(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.q = queue.Queue()
        self.url = 'https://beijing.anjuke.com/sale/'


    def crawl_all_detail(self):
        self.driver.get(self.url)
        next_url = self.driver.find_element_by_xpath('//*[@class="multi-page"]/a[7]').get_attribute('href')
        num = len(self.driver.find_elements_by_xpath('//*[@id="houselist-mod-new"]/li'))















    def run(self):
        #获取所有详情地址
        self.crawl_all_detail()





if __name__ == '__main__':
    spider = Anjuke_Spider()
    spider.run()
