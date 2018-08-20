# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from spiders.anjuke_scrapy_crawl.anjuke_scrapy_crawl.items import AnjukeItem


class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['beijing.anjuke.com']
    start_urls = ['https://beijing.anjuke.com/sale/']

    def parse(self, response):
        #验证码处理部分
        pass
        # next page link
        next_url = response.xpath('//*[@class="multi-page"]/a/@href').extract()[0]
        print('*********' + str(next_url) + '**********')
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)

        # 爬取每一页的所有房屋链接
        num = len(response.xpath('//*[@id="houselist-mod-new"]/li').extract())
        for i in range(1, num + 1):
            url = response.xpath('//*[@id="houselist-mod-new"]/li[{}]/div[2]/div/a/@href'.format(num)).extract()[0]
            yield scrapy.Request(url=url, callback=self.parse_detail)


    def parse_detail(self, response):
        houseinfo = response.xpath('//*[@class="houseInfo-wrap"]')
        if houseinfo:
            l = ItemLoader(AnjukeItem(), houseinfo)
            l.add_xpath('mode', '//div/div[2]/dl[1]/dd/text()')
            l.add_xpath('area', '//div/div[2]/dl[2]/dd/text()')
            l.add_xpath('floor', '//div/div[2]/dl[4]/dd/text()')
            l.add_xpath('age', '//div/div[1]/dl[3]/dd/text()')
            l.add_xpath('price', '//div/div[3]/dl[2]/dd/text()')
            l.add_xpath('location', '//div/div[1]/dl[1]/dd/a/text()')
            l.add_xpath('district', '//div/div[1]/dl[2]/dd/p/a[1]/text()')
            yield  l.load_item()














