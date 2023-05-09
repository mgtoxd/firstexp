import pandas as pd
from geopy.distance import geodesic

# 读取站点数据
sites = pd.read_csv('./edge-servers/site-optus-melbCBD.csv')

# 读取用户数据
users = pd.read_csv('./users/users-melbcbd-generated.csv')

# 创建一个字典来记录每个站点服务的用户数
user_counts = {site['SITE_ID']: 0 for i, site in sites.iterrows()}

# 找到每个用户最近的站点，并增加该站点的用户计数器
for i, user in users.iterrows():
    min_dist = float('inf')
    min_site_id = ''
    for j, site in sites.iterrows():
        dist = geodesic((user['Latitude'], user['Longitude']), (site['LATITUDE'], site['LONGITUDE'])).km
        if dist < min_dist:
            min_dist = dist
            min_site_id = site['SITE_ID']
    user_counts[min_site_id] += 1

print(user_counts)
# 创建一个新的 DataFrame，用于存储站点和其对应的用户数量
site_counts = pd.DataFrame({'SITE_ID': list(user_counts.keys()), 'USER_COUNT': list(user_counts.values())})

# 根据用户数量对站点进行排序
sorted_sites = sites.merge(site_counts, on='SITE_ID').sort_values(by=['USER_COUNT'], ascending=False)

# 选取20个均匀分布的站点
num_sites = len(sorted_sites)
interval = int(num_sites / 20)
selected_sites = sorted_sites.iloc[::interval]

# 输出每个站点服务的用户数
for site_id, count in user_counts.items():
    print(f"Site {site_id} serves {count} users")

# 输出选取的20个站点
print(selected_sites[['SITE_ID', 'USER_COUNT']])

# 创建一个空列表来保存选中的站点的 SITE_ID
selected_site_ids = []

# 按照用户数排序并选取20个站点
for i in range(20):
    site = sorted_sites.iloc[i]
    selected_site_ids.append(site['SITE_ID'])

# 输出选中的站点的 SITE_ID 列表
print(selected_site_ids)
