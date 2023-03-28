# Count the number of pictures by season

import pandas as pd
import os


dir = r"E:\Paper\Street Imagery Seasonal Variation\data\pid_deduplicated\Final_results"

cities = os.listdir(dir)

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

# 对每个记录的月份，计算它所在季节中的记录数

fw = open(os.path.join(r'E:\Paper\Street Imagery Seasonal Variation\data\pid_deduplicated\SVI_statistics.csv'), 'w', encoding='utf-8')

fw.write('City, Lon, Lat, Total, Spring, Summer, Autumn, Winter, None\n')

city_dict = {}

with open(r'E:\Paper\Street Imagery Seasonal Variation\data\pre_data\city.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line_arr = line.strip().split(',')
        city = line_arr[0]
        if len(line_arr) == 4:
            city_dict[city] = [line_arr[1].strip(), line_arr[2]]
        else:
            city_dict[city] = [line_arr[2].strip(), line_arr[1]]

for city in cities:
    city_name = city.split('_')[0]
    file = os.path.join(dir, city)
    data = pd.read_csv(file)

    data["season"] = data["month"].apply(get_season)
    counts = data.groupby("season").size()


    s = city_name + ',' + city_dict[city_name][0] + ',' + city_dict[city_name][1] + ',' + str(sum(counts)) + ',' + str(counts['spring']) + ',' + str(counts['summer']) + ',' + str(counts['autumn']) + ',' + str(counts['winter']) + ',' + str(counts['None']) + '\n'

    fw.write(s)
