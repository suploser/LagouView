# -*- coding: utf-8 -*-
#author: Mr.loser
#@
from selenium import webdriver
import time
import json
import os
import pandas as pd
import os
import re
import numpy as np
import matplotlib.pyplot as plt
# import jieba
from wordcloud import WordCloud,STOPWORDS
import matplotlib as mpl
from pyecharts import Geo
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.labelsize'] = 16.
plt.rcParams['xtick.labelsize'] = 14.
plt.rcParams['ytick.labelsize'] = 14.
plt.rcParams['legend.fontsize'] = 12.
plt.rcParams['figure.figsize'] = [15., 15.]
def get_cookies():
    brower = webdriver.Firefox()
    brower.get('https://passport.lagou.com/login/login.html')
    time.sleep(10)
    brower.find_element_by_css_selector('input[placeholder="请输入常用手机号/邮箱"]').send_keys('')
    brower.find_element_by_css_selector('input[placeholder="请输入密码"]').send_keys('')
    brower.find_element_by_css_selector('input.btn.btn_green.btn_active.btn_block.btn_lg').click()
    cookies = brower.get_cookies()
    cookies_dict = {}
    for cookie in cookies:
        cookies_dict [cookie['name']] = cookie['value']
    with open('cookies.json', 'w') as f:
        json.dump(cookies_dict, f)

    brower.close()
    pass

def get_data():

    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = os.path.join(csv_path, 'Lagou.csv')
    data = pd.read_csv(csv_path, header=None ,encoding='utf-8')
    return data


class ShowData(object):

    def __init__(self):
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        csv_path = os.path.join(csv_path, 'Lagou.csv')
        self.data = pd.read_csv(csv_path, header=None ,encoding='utf-8')
        self.geo = Geo('工资分布图(平均值)',  title_color='#000', title_pos='center', width=1200, height=600)

    def show_degree(self):
        self.data[2].value_counts().plot(kind='barh', rot=0)
        plt.show()

    def show_work_years(self):
        self.data[1].value_counts().plot(kind='bar', rot=0, color='b')
        plt.show()

    def show_job_address(self):
        self.data[4].value_counts().plot(kind='pie', autopct='%1.2f%%', explode=np.linspace(0, 0.15, len(self.data[4].value_counts())))
        plt.show()

    def show_job_name(self):
        final = ' '
        stopwords = set(STOPWORDS)
        # # 添加屏蔽词
        # stopwords.add('杭州')
        # stopwords.add('广州地区')
        font_path = '/home/user/.virtualenvs/article_spider/lib/python3.5/site-packages/matplotlib/mpl-data/fonts/ttf/SIMHEI.ttf'
        for n in  range(self.data.shape[0]):
            final = final+self.data[0][n]+'  '
            print(self.data[0][n])
        wc = WordCloud(font_path=font_path, stopwords=stopwords, background_color='white').generate(final)
        plt.imshow(wc)
        plt.axis('off')
        plt.show()

    def show_geo(self):
        data =list(map(lambda  x:(self.data[4][x], eval(re.split('k|K', self.data[5][x])[0])*1000), range(len(self.data))))
        data = pd.DataFrame(data)
        data = data.groupby(0).mean()
        # 索引改变,取值方式改变
        data = list(map(lambda x: (data.index[x], data[1].values[x]), range(len(data))))
        attr, value = self.geo.cast(data)
        #去掉空白字符
        city_list=[]
        for city in attr:
            city = city.strip()
            city_list.append(city)
        self.geo.add('', city_list, value, maptype='china',  type='effectScatter', border_color='#fff', symbol='pin',
                     symbol_size=20, geo_normal_color='#006edd', geo_emphasis_color='#0000ff')

        self.geo.render()

        pass


if __name__ == '__main__':
    s=ShowData()
    # s.show_job_address()
    # s.show_job_name()
    s.show_geo()
