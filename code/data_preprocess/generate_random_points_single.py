import random
import os
import shutil
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon

random.seed(123)

root = r'E:\Paper\Street Imagery Seasonal Variation\data\Multipoly'

city_name = 'Roi de Janeiro'
    # 读取shp文件并将其转换为geopandas的GeoDataFrame对象
gdf = gpd.read_file(os.path.join(root, 'Roi de Janeiro.geojson'))

print(gdf)


# poly_list = gdf.geometry[0]

polygon1 = gdf.geometry[0]
polygon2 = gdf.geometry[1]

print(polygon1)
print(polygon2)


points_in_poly1 = []
points_in_poly2 = []

while len(points_in_poly1) + len(points_in_poly2) < 30000:
    # 随机生成一个点
    x = random.uniform(gdf.bounds.minx, gdf.bounds.maxx)
    y = random.uniform(gdf.bounds.miny, gdf.bounds.maxy)
    point = (x, y)
    print(point)

    # 检查点属于哪个polygon

    if polygon1.contains(Point(point)):
        points_in_poly1.append(point)
    elif polygon2.contains(Point(point)):
        points_in_poly2.append(point)
    else:
        pass



points_in_poly1.extend(points_in_poly2)
print(points_in_poly1)
    # points_shp = [Point(p) for p in points_in_poly1]
    # # 将随机点转换为geopandas的GeoDataFrame对象
    # points_gdf = gpd.GeoDataFrame(geometry=points_shp)
    #
    # # 将随机点保存为GeoJSON文件
    # geopath = os.path.join(r'E:\Paper\Street Imagery Seasonal Variation\data\geojson', city_name + '.geojson')
    # points_gdf.to_file(geopath, driver='GeoJSON')
    #
    # # 将随机点保存为CSV文件
    # csvpath = os.path.join(r'E:\Paper\Street Imagery Seasonal Variation\data\csv', city_name + '_random_points.csv')
    # with open(csvpath, 'w') as f:
    #     f.write('lon,lat\n')
    #     for point in points_in_poly1:
    #         f.write(f'{point[0]},{point[1]}\n')

