# -*- coding: utf-8 -*-
'''
@Time    : 2023/3/20 22:55
@Author  : Ericyi
@File    : attach_h3.py

Attach hex id to pids files
'''

import os
import h3
import numpy as np
import pandas as pd

def get_season(month):
    if month in ["3", "4", "5"]:
        return "spring"
    elif month in ["6", "7", "8"]:
        return "summer"
    elif month in ["9", "10", "11"]:
        return "autumn"
    elif month in ["12", "1", "2"]:
        return "winter"
    else:
        return "None"

dir = r'E:\Paper\Street Imagery Seasonal Variation\data\Final_results_raw'

target_dir = r'E:\Paper\Street Imagery Seasonal Variation\data\Final_results'

cities = os.listdir(dir)

for city in cities:
    city_name = city.split('_')[0]
    file = os.path.join(dir, city)
    data = pd.read_csv(file)

    data["hex_id_7"] = data.apply(lambda row: h3.geo_to_h3(row["lat"], row["lon"], 7), axis=1)
    data["hex_id_8"] = data.apply(lambda row: h3.geo_to_h3(row["lat"], row["lon"], 8), axis=1)
    data["hex_id_9"] = data.apply(lambda row: h3.geo_to_h3(row["lat"], row["lon"], 9), axis=1)
    data["hex_id_10"] = data.apply(lambda row: h3.geo_to_h3(row["lat"], row["lon"], 10), axis=1)

    data.sort_values("hex_id_10", inplace=True)

    data = data.replace("None", np.nan)

    # 使用 dropna() 方法去掉包含 NaN 值的行
    data = data.dropna(subset=['month'])

    data["season"] = data["month"].apply(get_season)

    target_path = os.path.join(target_dir, city_name + '.csv')

    data.to_csv(target_path, index=False)




