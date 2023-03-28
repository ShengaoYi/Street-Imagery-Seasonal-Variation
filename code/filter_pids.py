# -*- coding: utf-8 -*-
'''
@Time    : 2023/3/21 17:11
@Author  : Ericyi
@File    : filter_pids.py

Filter the pids file according to year hexid

'''

import os
import pandas as pd

dir = r'E:\Paper\Street Imagery Seasonal Variation\data\Final_results'

target_dir = r'E:\Paper\Street Imagery Seasonal Variation\data\Final_results_filtered'

cities = os.listdir(dir)

start_year = 2016
# & (df['year'] < start_year + 5)
def filter_year(df):
    condition = (df['year'] >= start_year)
    filtered_df = df.loc[condition]
    return filtered_df

def sta_seasonal(city):
    file = os.path.join(dir, city + '.csv')
    df = pd.read_csv(file)

    result = df.groupby(['year', 'season']).size().reset_index(name='count')

    # 按年份顺序排列输出
    result = result.sort_values(by=['year', 'season'])

    print(result)
    return df

city_name = 'Amsterdam'

df = sta_seasonal(city_name)

target_path = os.path.join(target_dir, city_name + '_filtered.csv')

data = filter_year(df)

data.to_csv(target_path, index=False)



