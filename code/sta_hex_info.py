# -*- coding: utf-8 -*-
'''
@Time    : 2023/3/21 20:56
@Author  : Ericyi
@File    : sta_hex_info.py

'''
import os
import pandas as pd

filtered_dir = r'E:\Paper\Street Imagery Seasonal Variation\data\Final_results_filtered'

dir = r'E:\Paper\Street Imagery Seasonal Variation\data\Final_results'

city = r'Amsterdam'

file = os.path.join(dir, city + '.csv')

filter_file = os.path.join(filtered_dir, city + '_filtered.csv')

df = pd.read_csv(file)

counts = df["hex_id_10"].nunique()

filter_df = pd.read_csv(filter_file)

filter_counts = filter_df.groupby("season")["hex_id_10"].nunique()

print(counts)
print(filter_counts)