# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class MysoldspiderPipeline(object):
    def process_item(self, item, spider):
        f = open('D:\Workspace\PythonML\mySoldSpider\lianjia_sold.csv','a+',newline ='')
        write = csv.writer(f)
#        write.writerow((item['residence'],item['roomNum'],item['roomStructure'],
#                        item['area'],item['level'],item['orientation'],item['buildingType'],
#                        item['buildingStructure'],item['furnished'],item['ratioPerLevel'],
#                        item['lift'],item['propertyRights'],item['timeForSale'],
#                        item['timeBeforeLastTrade'],item['timeOfLastTrade'],
#                        item['tradeType'],item['houseUsage'],item['price'],
#                        item['average_price'],item['link'],item['district'],
#                        item['town'],item['location']))
        
        write.writerow((item['residence'],item['roomNum'],item['roomStructure'],
                        item['area'],item['level'],item['orientation'],item['buildingType'],
                        item['buildingStructure'],item['furnished'] ,item['ratioPerLevel'],
                        item['lift'],item['propertyRights'],item['timeForSale'],
                        item['tradeType'],item['houseUsage'],item['buildTime'],
                        item['price'],item['deal_price'],item['deal_average_price'],
                        item['time_on_web'],item['price_change_times'],item['look_times'],
                        item['link'],item['district'],item['town']))
        
        
        #write.writerow(([item['residence']]))
        return item
