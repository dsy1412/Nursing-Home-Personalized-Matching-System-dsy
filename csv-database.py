import sqlite3
import csv
import os
import re


def create_database(db_file):
    print(f"Creating database: {db_file}")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS elderly_care_centers (
            name TEXT,
            location TEXT,
            institution_type TEXT,
            responsible_person TEXT,
            opening_date TEXT,
            area_land INTEGER,
            building_area INTEGER,
            beds_number INTEGER,
            care_types TEXT,
            contact_person TEXT,
            address TEXT
        );
    ''')
    conn.commit()
    conn.close()
    print("Database created successfully.")


def parse_row(row):
    # 提取冒号之后的汉字内容对于 location
    location = row[1].split('：')[-1].strip() if '：' in row[1] else ''

    # 移除“机构性质：”和“负责人：”文本，如果它们不存在，则设置为空字符串
    institution_type = ' '.join(re.split(r'\s+', row[2].replace('机构性质：', '').strip())) if '机构性质：' in row[
        2] else ''
    responsible_person = row[3].replace('负  责  人：', '').strip() if '负  责  人：' in row[3] else ''
    opening_date = row[4].replace('开业时间：', '').strip() if '开业时间：' in row[4] else ''
    area_land = row[5].replace('占地面积：', '').strip() if '占地面积：' in row[5] else ''
    building_area = row[6].replace('建筑面积：', '').strip() if '建筑面积：' in row[6] else ''
    beds_number = re.sub(r'床位数：|\s+张', '', row[7]).strip() if '床位数：' in row[7] else ''
    care_types = row[8].replace('特色服务：', '').strip() if '特色服务：' in row[8] else ''
    contact_person = row[9].replace('联  系  人：', '').strip() if '联  系  人：' in row[9] else ''
    address = row[10].replace('地        址：', '').strip() if '地        址：' in row[10] else ''

    # 对其他列进行类似处理，确保所有列都经过检查和处理
    # ...

    # 更新原始数据行
    row[1] = location
    row[2] = institution_type
    row[3] = responsible_person
    row[4] = opening_date
    row[5] = area_land
    row[6] = building_area
    row[7] = beds_number
    row[8] = care_types
    row[9] = contact_person
    row[10] = address

    # 对其他列进行同样的更新
    # ...

    return row


def insert_data_from_csv(db_file, csv_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 假设第一行是列标题并跳过
        for original_row in reader:
            formatted_row = parse_row(list(original_row))  # 格式化行数据
            cursor.execute('''
                INSERT INTO elderly_care_centers (
                    name, location, institution_type, responsible_person,
                    opening_date, area_land, building_area, beds_number,
                    care_types, contact_person, address
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', formatted_row)  # 使用格式化后的数据

    conn.commit()
    conn.close()
    print(f"Data inserted successfully from: {csv_file}")


def process_all_csv_files(db_file, folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, filename)
            insert_data_from_csv(db_file, csv_file_path)


# 你的数据库文件和包含CSV文件的文件夹路径
db_file = 'elderly_care_centers.db'
folder_path = 'csv_file'

create_database(db_file)  # 创建数据库和表
process_all_csv_files(db_file, folder_path)
