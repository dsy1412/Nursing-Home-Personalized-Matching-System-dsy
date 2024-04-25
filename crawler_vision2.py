# 引入必要的库
import requests
from bs4 import BeautifulSoup
import sqlite3
import csv
import xlwt
import os

# 定义文件夹路径
csv_folder = 'Nursing-Home-Personalized-Matching-System-dsy\csv_file'

# 确保文件夹存在
os.makedirs(csv_folder, exist_ok=True)

# 配置User-Agent，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}


def init_db(city):
    # 确保database文件夹存在
    db_folder = 'Nursing-Home-Personalized-Matching-System-dsy\database'
    os.makedirs(db_folder, exist_ok=True)

    # 创建或打开数据库
    db_path = os.path.join(db_folder, f'{city}.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nursing_home (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            type_info TEXT,
            feature_1 TEXT,
            feature_2 TEXT,
            feature_3 TEXT,
            feature_4 TEXT,
            feature_5 TEXT,
            feature_6 TEXT,
            bed_number TEXT,
            price_range TEXT
        );
    ''')
    conn.commit()
    conn.close()
    return db_path  # 返回数据库文件路径


def scrape(city):
    base_url = f'https://www.yanglao.com.cn/{city}'
    max_pages = 1  # 设置最大页面数
    page_num = 1  # 初始页面
    links = []  # 存储所有找到的链接

    while page_num <= max_pages:
        if page_num > 1:
            current_url = f"{base_url}_{page_num}"  # 构建当前页的URL
        else:
            current_url = base_url  # 第一页的URL

        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            print(f"访问第{page_num}页失败，状态码：{response.status_code}")
            break  # 如果页面请求失败或不存在，输出错误并退出循环

        soup = BeautifulSoup(response.content, 'html.parser')
        nursing_homes = soup.select("#yw0 > ul > li > div > h4 > a")
        if not nursing_homes:
            print(f"第{page_num}页没有找到养老院链接，提前终止。")
            break  # 如果没有找到养老院链接，假定已达到无更多数据的页面，退出循环

        new_links = [home['href'] for home in nursing_homes]
        links.extend(new_links)  # 添加新发现的链接到列表
        page_num += 1  # 准备访问下一页

    # 初始化数据库
    db_path = init_db(city)

    # 遍历每个养老院链接，爬取并存储数据
    for link in links:
        full_link = f"https://www.yanglao.com.cn{link}" if not link.startswith('http') else link
        data = parse_nursing_home_page(full_link)
        save_to_db(city, data)
        save_to_csv(city, data)

    print(f"数据爬取完毕，共爬取了{page_num - 1}页。")


def parse_nursing_home_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 提取养老院名称
    name = soup.select_one("div.inst-summary > h1")
    name = name.text.strip() if name else '名称未找到'

    # 提取地址
    address = soup.select_one("div.base-info > div > ul > li:nth-child(1)")
    address = address.text.strip() if address else '地址未找到'

    # 分别提取其他信息
    type_info = soup.select_one("div.inst-detail > div.panel > div.base-info > div > ul > li:nth-child(3)")
    type_info = type_info.text.strip() if type_info else '类型信息未找到'

    feature_1 = soup.select_one("div.inst-detail > div.panel > div.base-info > div > ul > li:nth-child(4) ")
    feature_1 = feature_1.text.strip() if feature_1 else '特征1未找到'

    feature_2 = soup.select_one("div.inst-detail > div.panel > div.base-info > div > ul > li:nth-child(5) ")
    feature_2 = feature_2.text.strip() if feature_2 else '特征2未找到'

    feature_3 = soup.select_one("div.inst-detail > div.panel > div.base-info > div > ul > li:nth-child(6) ")
    feature_3 = feature_3.text.strip() if feature_3 else '特征3未找到'

    feature_4 = soup.select_one("div.inst-detail > div.panel > div.base-info > div > ul > li:nth-child(7) ")
    feature_4 = feature_4.text.strip() if feature_4 else '特征4未找到'

    feature_5 = soup.select_one("div.inst-detail > div.panel > div.base-info > div > ul > li:nth-child(8) ")
    feature_5 = feature_5.text.strip() if feature_5 else '特征5未找到'

    feature_6 = soup.select_one("div.inst-detail > div.panel > div.base-info > div > ul > li:nth-child(9) ")
    feature_6 = feature_6.text.strip() if feature_6 else '特征6未找到'

    bed_number = soup.select_one("#boxWrap > div > ul > li:nth-child(1) ")
    bed_number = bed_number.text.strip() if bed_number else '床位数量未找到'

    price_range = soup.select_one("#boxWrap > div > ul > li:nth-child(2) ")
    price_range = price_range.text.strip() if price_range else '价格范围未找到'

    return {
        'name': name,
        'address': address,
        'type_info': type_info,
        'feature_1': feature_1,
        'feature_2': feature_2,
        'feature_3': feature_3,
        'feature_4': feature_4,
        'feature_5': feature_5,
        'feature_6': feature_6,
        'bed_number': bed_number,
        'price_range': price_range
    }


def save_to_db(city, data):
    # 从city参数构建数据库文件路径
    db_path = os.path.join('Nursing-Home-Personalized-Matching-System-dsy\database', f'{city}.db')

    # 插入数据
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nursing_home (
            name, address, type_info, feature_1, feature_2, feature_3, 
            feature_4, feature_5, feature_6, bed_number, price_range
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', (
        data['name'], data['address'], data['type_info'], data['feature_1'], data['feature_2'],
        data['feature_3'], data['feature_4'], data['feature_5'], data['feature_6'],
        data['bed_number'], data['price_range']
    ))
    conn.commit()
    conn.close()


'''
def save_to_db(db_path, data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute
        INSERT INTO nursing_home (name, institution_nature, person_in_charge, opening_date, area, bed_number, resident_type, price_range, contact_person, address) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    , (data['name'], data['institution_nature'], data['person_in_charge'], data['opening_date'], data['area'], data['bed_number'], data['resident_type'], data['price_range'], data['contact_person'], data['address']))
    conn.commit()
    conn.close()
    '''


def save_to_csv(city, data):
    file_path = os.path.join(csv_folder, f'{city}.csv')  # 更新CSV文件的路径
    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            [data['name'], data['address'], data['type_info'], data['feature_1'], data['feature_2'], data['feature_3'],
             data['feature_4'], data['feature_5'], data['feature_6'], data['bed_number'], data['price_range']])


# 省份拼音列表
# provinces_pinyin = [
#     'beijing', 'shanghai', 'tianjin', 'chongqing', 'hebei', 'henan',
#     'yunnan', 'liaoning', 'heilongjiang', 'hunan', 'anhui', 'shandong',
#     'xinjiang', 'jiangsu', 'zhejiang', 'jiangxi', 'hubei', 'guangxi',
#     'gansu', 'shanxi', 'neimenggu', 'shanxi', 'jilin', 'fujian', 'guizhou',
#     'guangdong', 'qinghai', 'xizang', 'sichuan', 'ningxia', 'hainan',
#     'taiwan', 'xianggang', 'aomen'
# ]
provinces_pinyin = [
    'neimenggu', 'shanxi', 'jilin', 'fujian', 'guizhou',
    'guangdong', 'qinghai', 'xizang', 'sichuan', 'ningxia', 'hainan',
    'taiwan', 'xianggang', 'aomen'
]

# 其余的函数保持不变...

if __name__ == '__main__':
    # 对于每一个省份拼音执行爬取
    for province in provinces_pinyin:
        print(f"正在爬取 {province} 的数据...")
        scrape(province)
    print("所有省份数据爬取完毕。")
