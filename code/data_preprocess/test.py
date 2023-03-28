# -*- coding: utf-8 -*-
'''
@Time    : 2023/3/21 18:38
@Author  : Ericyi
@File    : test.py

'''
import os
import pandas as pd

dir = r'E:\Paper\Street Imagery Seasonal Variation\data\Final_results'

cities = os.listdir(dir)

for city in cities:
    city_name = city.split('_')[0]
    file = os.path.join(dir, city)
    df = pd.read_csv(file)

    result = df.groupby(['year', 'season']).size().reset_index(name='count')

    # 按年份顺序排列输出
    result = result.sort_values(by=['year', 'season'])

    print(result)

    break
