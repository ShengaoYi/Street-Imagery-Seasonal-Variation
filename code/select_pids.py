# -*- coding: utf-8 -*-
'''
@Time    : 2023/3/22 21:01
@Author  : Ericyi
@File    : select_pids.py

select 20-30 pids per hex and per season

'''
import os
import random
import pandas as pd

dir = r'E:\Paper\Street Imagery Seasonal Variation\data\Final_results_filtered'

target_dir = r'E:\Paper\Street Imagery Seasonal Variation\data\Final_results_selected_hex7'

cities = os.listdir(dir)

fw = open(os.path.join(target_dir, 'result.txt'), 'a')

fw.write('city,total_hex,selected_hex\n')

for city in cities:
    city_name = city.split('_')[0]
    file = os.path.join(dir, city)
    df = pd.read_csv(file)

    total_hex = df["hex_id_7"].nunique()

    grouped = df.groupby("hex_id_7")

    result_df = pd.DataFrame(columns=df.columns)

    count = 0

    for hexid, group in grouped:
        # 计算各季节的数据行数
        season_counts = group['season'].value_counts()

        if all(season_counts >= 25) and len(season_counts) == 4:
            # 各季节的数据行数都满足条件，随机选择数据行
            for season in group['season'].unique():
                season_data = group[group['season'] == season]
                selected_data = season_data.sample(25)
                result_df = pd.concat([result_df, selected_data])
            count += 1

    target_path = os.path.join(target_dir, city_name + '_hex7.csv')

    print(city_name)

    result_df.to_csv(target_path, index=False)

    s = city_name + ',' + str(total_hex) + ',' + str(count) + '\n'

    fw.write(s)




