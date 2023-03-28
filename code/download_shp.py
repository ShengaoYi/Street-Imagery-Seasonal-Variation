# encoding: utf-8
# author: zhaotianhong
# contact: zhaotianhong2016@email.szu.edu.cn

# 下载边界
import osmnx as ox
import geopandas as gpd
import os


# save_dir = 'data'
place_name_search = "Helsinki"
# name_save = 'Helsinki'
#
# dir_city = os.path.join(save_dir, name_save)
#
# if not os.path.exists(dir_city):
#     os.makedirs(dir_city)

area = ox.geocode_to_gdf(place_name_search)
print(area)
# shp_path = os.path.join(dir_city, name_save + ".geojson")
# area.to_file(shp_path, driver='GeoJSON')

# graph = ox.graph_from_place(place_name_search, network_type='drive')
# ox.save_graph_shapefile(graph, filepath=dir_city)



