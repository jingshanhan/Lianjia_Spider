# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 22:15:07 2019

@author: Administrator
"""
import scrapy
import requests
import re
import time
from urllib.parse import urljoin
from lxml import etree
import random
from mySoldSpider.items import MysoldspiderItem
import ast


class Sold_Spider(scrapy.Spider):
    name = "my_Sold_LianjiaSpider"
    allowed_domains = ["sh.lianjia.com"]
    start_urls = "https://sh.lianjia.com/chengjiao/"
    
    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0'
        headers = {'User-Agent': user_agent}
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET',callback=self.parse)
        
    def parse(self, response):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0'
        headers = {'User-Agent': user_agent}
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)
        area_list = selector.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a')
        for area in area_list:
            try:
                area_pinyin = area.xpath('@href').pop().split('/')[2]
                area_url = 'http://sh.lianjia.com/chengjiao/{}/'.format(area_pinyin)
                print(area_url)
                yield scrapy.Request(url=area_url, headers=headers, callback = self.my_town_parse)
            except Exception:
                pass
    
    def my_town_parse(self,response):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0'
        headers = {'User-Agent': user_agent}
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)
        town_list = selector.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a')
        
        for town in town_list:
            try:
                town_pinyin = town.xpath('@href').pop().split('/')[2]
                town_url = 'http://sh.lianjia.com/chengjiao/{}/'.format(town_pinyin)
                print(town_url)
                yield scrapy.Request(url=town_url, headers=headers, callback = self.my_page_parse)
            except Exception:
                pass           
    
    def my_page_parse(self,response):        
        
        town_name = 'unknown'
        town_list = response.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a')
        for town in town_list:
            if town.xpath('@class').get() is not None:
                town_name = town.xpath('@href').get().split('/')[2]
        
        num_of_house_on_sale = int(response.xpath('/html/body/div[5]/div[1]/div[2]/div[1]/span/text()').get())
        if num_of_house_on_sale !=0:
            try:
                page_data = ast.literal_eval(response.xpath('/html/body/div[5]/div[1]/div[5]/div[2]/div/@page-data').get())   
                total_page = page_data['totalPage']
                current_page = page_data['curPage']
                
                house_list = response.xpath('/html/body/div[5]/div[1]/ul/li')
                
                for house in house_list:
                    time.sleep(random.randint(1,10)/20)
                    house_link =  house.xpath('div/div[1]/a/@href').get()
                    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0'
                    headers = {'User-Agent': user_agent}
                    
                    yield scrapy.Request(url=house_link, headers=headers,callback=self.my_house_detail)
            except Exception:
                pass
                                
            if total_page != current_page:
                next_page_url = 'http://sh.lianjia.com/chengjiao/{}/pg{}/'.format(town_name,current_page+1)
                try:
                    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0'
                    headers = {'User-Agent': user_agent}
                    time.sleep(random.randint(1,10)/20)
                    yield scrapy.Request(next_page_url, headers=headers, callback=self.my_page_parse)
                except Exception:
                    pass    
#    
    def my_house_detail(self,response):
        try:
            item = MysoldspiderItem()
            
            item['residence'] = response.xpath('/html/body/section[1]/div[1]/a[5]/text()').get()
            #item['title'] = house.xpath('div[1]/div[1]/a/text()').get()
            item['roomNum'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[1]/text()').get()
            item['roomStructure'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[4]/text()').get()
            item['area'] =  response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[3]/text()').get()
            item['level'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[2]/text()').get()
            item['orientation'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[7]/text()').get()
            item['buildingType'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[6]/text()').get()
            item['buildingStructure'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[10]/text()').get()
            item['furnished'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[9]/text()').get()
            item['ratioPerLevel'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[12]/text()').get()
            item['lift'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[14]/text()').get()
            item['propertyRights'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[13]/text()').get()
            item['timeForSale'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[3]/text()').get()
            #item['timeBeforeLastTrade'] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[5]/span[2]/text()').get()
            #item['timeOfLastTrade'] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[3]/span[2]/text()').get()
            item['tradeType'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[2]/text()').get()
            
            item['houseUsage'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[4]/text()').get() 
            item['buildTime'] = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[8]/text()').get()
            item['price'] =  response.xpath('/html/body/section[1]/div[2]/div[2]/div[3]/span[1]/label/text()').get()
            item['deal_price']=  response.xpath('/html/body/section[1]/div[2]/div[2]/div[1]/span/i/text()').get()
            item['deal_average_price'] =  response.xpath('/html/body/section[1]/div[2]/div[2]/div[1]/b/text()').get()
            item['time_on_web'] = response.xpath('/html/body/section[1]/div[2]/div[2]/div[3]/span[2]/label/text()').get()
            item['price_change_times'] = response.xpath('/html/body/section[1]/div[2]/div[2]/div[3]/span[3]/label/text()').get()
            item['look_times'] = response.xpath('/html/body/section[1]/div[2]/div[2]/div[3]/span[4]/label/text()').get()
            
            item['link'] = response.url
            item['district'] = response.xpath('/html/body/section[1]/div[1]/a[3]/text()').get()
            item['town'] = response.xpath('/html/body/section[1]/div[1]/a[4]/text()').get()
            #item['location'] = response.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/span[2]/text()[2]').get()[1:]
            
            yield item
        except Exception:
            pass
#        
