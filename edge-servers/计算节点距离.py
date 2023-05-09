import pandas as pd
from geopy.distance import geodesic

# 读取数据
data = pd.read_csv('site-optus-melbCBD.csv')

# 选出前20个站点
top20 = data.head(20)

# 计算站点之间的距离
for i, row1 in top20.iterrows():
    for j, row2 in top20.iterrows():
        if i < j:
            dist = geodesic((row1['LATITUDE'], row1['LONGITUDE']), (row2['LATITUDE'], row2['LONGITUDE'])).km
            print(f"Distance between {row1['SITE_ID']} and {row2['SITE_ID']}: {dist:.2f} km")
