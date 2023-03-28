# encoding: utf-8
# author: zhaotianhong
# contact: zhaoteanhong@gmail.com
# file: get_ids.py
# time: 2022/6/8 19:45


import os
import h3
import streetview
import threading
import time


def read_h3_xy(path):
    '''
    h3中心点，最好是10
    :param path: xy 是二和第三列
    :return:
    '''
    xys = []
    with open(path, 'r') as f:
        f.__next__()
        for line in f:
            line_arr = line[:-1].split(',')
            xy = [float(line_arr[0]), float(line_arr[1])]
            xys.append(xy)
    return xys


def point_around(xy):
    '''
    获取一个点周边pano_id
    :param xy:!! 特别注意，经度纬度的顺序:[纬度，经度]
    :return:
    '''

    info = streetview.panoids(str(xy[1]), str(xy[0]))
    return info


def save_mata(path, meta_data):
    '''
    追加保存mata数据信息
    :param meta_path:
    :param meta_data:
    :return:
    '''
    num = 0
    with open(path, 'a+') as fw:
        for m in meta_data:
            num += 1
            pid = m["panoid"]
            lat = m["lat"]
            lon = m["lon"]
            try:
                year = m["year"]
                month = m["month"]
            except:
                year = "None"
                month = "None"
            fw.write('%s,%s,%s,%s,%s\n' % (pid, lat, lon, year, month))
    return num


def filter(path_in, path_out):
    '''
    :param path_in: 输入的panorama id数据路径
    :param path_out: 输出路径
    :param level:
    :return:
    '''
    pids = []
    nums = 0
    with open(path_out, 'w') as fw:
        fw.write('pid,lat,lon,year,month\n')
        with open(path_in, 'r') as f:
            for line in f:
                nums += 1
                pid = line.split(',')[0]
                if pid in pids:
                    continue
                else:
                    fw.write(line)
                    pids.append(pid)
    print('filter', len(pids), nums)


def get_pano_2(xy, ALL_DATA, ALL_ID):
    '''
    获取两阶，获取到的点，在搜索一次，可以得到更多带有时间标签的
    :param xy:
    :param ALL_DATA:
    :return:
    '''
    e_times = 0
    try:
        meta_data1 = point_around(xy)
        for panoid in meta_data1:
            try:
                xy = [panoid['lon'],panoid['lat']]
                pid = panoid['panoid']
                if pid in ALL_ID:
                    continue
                else:
                    meta_data2 = point_around(xy)
                    ALL_DATA.extend(meta_data2)
                    ALL_ID.append(pid)
            except Exception as e:
                e_times += 1
    except Exception as e:
        e_times += 1

    print(xy, 'error', e_times)



def get_pano_1(xy, ALL_DATA):
    '''
    获取一阶，一个点周围
    :param xy_list: 所有需要索引的xy
    :param meta_path: 保存mata数据的路径，追加写入方式
    :return:
    '''
    try:
        meta_data = point_around(xy)
        ALL_DATA.append(meta_data)

    except Exception as e:
        print(e)


def run(xy_list, pid_raw_path):
    index = 0
    num_thread = 1
    get = 0

    ALL_DATA, ALL_ID = [], []
    threads = []

    for xy in xy_list:
        index += 1
        # if index == 2:
        #     break
        if index % num_thread == 0:
            t = threading.Thread(target=get_pano_2, args=(xy, ALL_DATA, ALL_ID))
            threads.append(t)
            for t in threads:
                t.setDaemon(True)
                t.start()
            time.sleep(0.2)
            t.join()
            num = save_mata(pid_raw_path, ALL_DATA)
            get += num
            threads = []
            ALL_DATA = []
            print('Done:',index, '/', len(xy_list),'got:', get)
        else:
            t = threading.Thread(target=get_pano_2, args=(xy, ALL_DATA, ALL_ID))
            threads.append(t)

from geopy.distance import geodesic

if __name__ == '__main__':
    # with open('./nyc_random_points.csv', 'r', encoding='utf-8') as f:
    #     next(f)
    #     i = 0
    #     for line in f:
    #         i += 1
    #         line_arr = line.strip().split(',')
    #         xy = [float(line_arr[0]), float(line_arr[1])]
    #         try:
    #             meta_data1 = point_around(xy)
    #             panoids_within_distance = []
    #             for pan in meta_data1:
    #                 pan_lat, pan_lon = pan['lat'], pan['lon']
    #                 dist = geodesic((xy[1], xy[0]), (pan_lat, pan_lon)).meters
    #                 panoids_within_distance.append(dist)
    #             if max(panoids_within_distance) > 120:
    #                 print(max(panoids_within_distance), len(panoids_within_distance), i)
    #         except:
    #             continue

    dir_xy = r'E:\Paper\Street Imagery Seasonal Variation\data\reselcetcsv'  # 城市坐标文件夹，注意命名"city name"+"_"+xy" 注意经纬度前后顺序
    dir_pid_raw = r'E:\Paper\Street Imagery Seasonal Variation\data\new_pids'  # 保存pid的文件夹

    for name in os.listdir(dir_xy):
        if '.DS' in name:
            continue
        name_city = name.split('_')[0]
        xy_path = os.path.join(dir_xy, name)
        pid_raw_path = os.path.join(dir_pid_raw, name_city + "_pid_raw.csv")

        with open(pid_raw_path, 'w', encoding='utf-8') as fw:
            fw.write('pid,lat,lon,year,month\n')

        xy_list = read_h3_xy(xy_path)
        run(xy_list, pid_raw_path)

        path_out = os.path.join(dir_pid_raw, name_city + "_pid_raw_deduplication.csv")
        filter(pid_raw_path, path_out)

        break


