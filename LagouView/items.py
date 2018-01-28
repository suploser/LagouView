# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def remove_splah(value):
    return value.replace('/','')


class LagouViewItem(scrapy.Item):
    # 岗位
    job_name = scrapy.Field()
    # 工作年限
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splah)
    )
    # 学历
    degree = scrapy.Field(
        input_processor=MapCompose(remove_splah)
    )
    # 工作类型
    job_type = scrapy.Field()
    # 工作地点
    job_address = scrapy.Field(
        input_processor=MapCompose(remove_splah)
    )
    #工资
    salary = scrapy.Field()
    #公司福利
    welfare = scrapy.Field()
    #公司名
    company = scrapy.Field(
        input_processor=MapCompose(remove_splah)
    )


