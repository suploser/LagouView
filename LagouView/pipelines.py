# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import os
class LagouviewPipeline(object):
    def process_item(self, item, spider):
        data = [[item['job_name'], item['work_years'], item['degree'], item['job_type'], item['job_address'], item['salary'], item['welfare'], item['company']]]
        data = pd.DataFrame(data)
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
        csv_path = os.path.join(csv_path, 'Lagou.csv')
        data.to_csv(csv_path, header=False, index=False, mode='a+')
        return item
