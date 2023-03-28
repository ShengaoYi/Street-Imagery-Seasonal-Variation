import random
import os
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon

root = r'E:\Paper\Street Imagery Seasonal Variation\data\test'

cities = os.listdir(root)

print(cities)

for city in cities:
    city_name = city.split('.')[0]

    # 读取shp文件并将其转换为geopandas的GeoDataFrame对象
    gdf = gpd.read_file(os.path.join(root, city))

    if isinstance(gdf.geometry[0], MultiPolygon):
        poly_list = list(gdf.geometry[0])
        polygon = poly_list[0]
    else:
        polygon = gdf.geometry[0]

    # 定义一个列表用于存储在polygon内的随机点
    points = []

    # 生成500个随机点，并将它们限制在polygon内
    while len(points) < 5000:
        # 生成随机点的坐标
        x = random.uniform(polygon.bounds[0], polygon.bounds[2])
        y = random.uniform(polygon.bounds[1], polygon.bounds[3])

        # 创建一个包含经纬度的元组，并将其添加到列表中
        point = (x, y)

        if polygon.contains(Point(point)):
            points.append(point)


    points_shp = [Point(p) for p in points]
    # 将随机点转换为geopandas的GeoDataFrame对象
    points_gdf = gpd.GeoDataFrame(geometry=points_shp)

    geopath = os.path.join(r'E:\Paper\Street Imagery Seasonal Variation\data\reselectgeojson', city_name + '.geojson')

    # 将随机点保存为GeoJSON文件
    points_gdf.to_file(geopath, driver='GeoJSON')

    # 将随机点保存为CSV文件
    csvpath = os.path.join(r'E:\Paper\Street Imagery Seasonal Variation\data\reselcetcsv', city_name + '_random_points.csv')
    with open(csvpath, 'w') as f:
        f.write('lon,lat\n')
        for point in points:
            f.write(f'{point[0]},{point[1]}\n')
