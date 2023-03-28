import pandas as pd
import os

dir = r"E:\Paper\Street Imagery Seasonal Variation\data\new_pids"

cities = os.listdir(dir)


for city in cities:
    total = []
    pids = {}
    city_name = city.split('_')[0]
    file = os.path.join(dir, city)
    with open(file, 'r', encoding='utf-8') as f:
        next(f)
        for line in f:
            line_arr = line.strip().split(',')
            pid = line_arr[0]
            month = line_arr[-1]
            if pid not in pids.keys():
                pids[pid] = line
            else:
                if month != "None":
                    pids[pid] = line
                else:
                    continue

    fw = open(os.path.join(r'E:\Paper\Street Imagery Seasonal Variation\data\pid_deduplicated\recleaned', city_name + '_cleaned.csv'), 'w', encoding='utf-8')
    fw.write('pid,lat,lon,year,month\n')
    for k,v in pids.items():
        fw.write(v)
