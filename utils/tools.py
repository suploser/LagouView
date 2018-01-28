# -*- coding: utf-8 -*-
#author: Mr.loser
#
from selenium import webdriver
import time
import json
def get_cookies():
    brower = webdriver.Firefox()
    brower.get('https://passport.lagou.com/login/login.html')
    time.sleep(10)
    brower.find_element_by_css_selector('input[placeholder="请输入常用手机号/邮箱"]').send_keys('18728899376')
    brower.find_element_by_css_selector('input[placeholder="请输入密码"]').send_keys('1321131987')
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
    import pandas as pd
    import os
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = os.path.join(csv_path, 'Lagou.csv')
    data = pd.read_csv(csv_path, header=None ,encoding='utf-8')
    return data
if __name__=='__main__':
    data = get_data()
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import jieba
    from wordcloud import WordCloud
    import matplotlib as mpl
    # mpl.use('TkAgg')
    from pyecharts import Geo

    mpl.rcParams['font.sans-serif'] = ['SimHei']

    plt.rcParams['axes.labelsize'] = 16.
    plt.rcParams['xtick.labelsize'] = 14.
    plt.rcParams['ytick.labelsize'] = 14.
    plt.rcParams['legend.fontsize'] = 12.
    plt.rcParams['figure.figsize'] = [15., 15.]

    data[2].value_counts().plot(kind='barh', rot=0)
    plt.show()