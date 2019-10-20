# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MysoldspiderItem(scrapy.Item):
    residence= scrapy.Field()
    roomNum= scrapy.Field()
    roomStructure= scrapy.Field()
    area= scrapy.Field()
    level= scrapy.Field()
    orientation= scrapy.Field()
    buildingType= scrapy.Field()
    buildingStructure= scrapy.Field()
    furnished= scrapy.Field()
    ratioPerLevel= scrapy.Field()
    lift= scrapy.Field()
    propertyRights= scrapy.Field()
    timeForSale= scrapy.Field()
    timeBeforeLastTrade= scrapy.Field()
    timeOfLastTrade= scrapy.Field()
    tradeType= scrapy.Field()
    houseUsage= scrapy.Field()
    price= scrapy.Field()
    average_price= scrapy.Field()
    link= scrapy.Field()
    district= scrapy.Field()
    town= scrapy.Field()
    location= scrapy.Field()
    buildTime= scrapy.Field()
    deal_price= scrapy.Field()
    deal_average_price= scrapy.Field()
    time_on_web= scrapy.Field()
    price_change_times= scrapy.Field()
    look_times= scrapy.Field()
    
