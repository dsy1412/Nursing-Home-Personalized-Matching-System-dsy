# coding=gbk
from flask import Flask, render_template,request
import requests
import re
import csv
import xlwt
import sqlite3

url = 'https://www.yanglao.com.cn/'  # 指定url
# Ua伪装 将对应的请求载体 User-Agent 封装到一个字典中
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}
# 处理url携带的参数 封装到字典中
city = input("请输入城市：")
global fileName2
fileName2 = city + '.csv'

# 发起请求 get方法会返回一个相应对象 且是携带参数的，动态拼接在url后面(第二个参数）d第三个参数UA伪装请求载体
child_href_list = []
for item in range(2):  # 循环为了使爬取养老院数据增加
    if item == 0:
        url = url + city
    else:
        url = url + "_2"  # （第二页是加了_2)

    response = requests.get(url=url, headers=headers)  # 发起请求 get方法会返回一个相应对象

    response.encoding = 'utf-8'
    page_text = response.text  # 获取响应数据，text返回的是字符串形式的响应数据
    # 解析数据此时爬取的各养老院标题链接 为下次url爬取铺垫
    obj = re.compile('<div class="info">.*?<a target="_blank".*?href="(?P<web>.*?)"', re.S)

    # 开始匹配
    result = obj.finditer(page_text)
    for it in result:  # 输入csv中 修改地址
        if item == 0:
            child_href = url.replace(f'{city}', f"{it.group('web').strip('/')}")
        else:
            child_href = url.replace(f'{city}_2', f"{it.group('web').strip('/')}")
        child_href_list.append(child_href)  # 把子页面地址保存
    print('over!1')
    response.close()
href2 = child_href_list
print(href2)
for href in href2:

    headers3 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
    }
    response2 = requests.get(url=href, headers=headers3)  # 发起请求 get方法会返回一个相应对象
    response2.encoding = 'utf-8'
    page_text2 = response2.text  # 获取响应数据，text返回的是字符串形式的响应数据 此时返回的是各子页面信息

    # fileName2 = city + '.csv'
    # print(fileName2)
    # result2 = obj2.finditer(page_text2)
    # result2 = re.findall(
    #     '<div class="inst-summary">.*?<h1>(?P<name>.*?)</h1>|'
    #     '<li><em>地.*?址：</em>(?P<address>.*?)</li>|'
    #     '<li><em>床.*?位：</em>(?P<chuangwei>.*?)</li>|'
    #     '<li><em>收.*?费：</em>(?P<money>.*?)</li>|'
    #     '<li><em>收住对象：</em>\s*(?P<object>.*?)</li>|'
    #     '<li><em>特色服务：</em>\s*(?P<service>.*?)</li>'
    #     , page_text2,re.S)
    try:
        name = re.findall('<div class="inst-summary">.*?<h1>(.*?)</h1>', page_text2, re.S)[0].strip().replace('&nbsp;',
                                                                                                              ' ')
        address = re.findall('<li><em>地.*?址：</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        chuangwei = re.findall('<li><em>床.*?位：</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        money = re.findall('<li><em>收.*?费：</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        object = re.findall('<li><em>收住对象：</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        service = re.findall('<li><em>特色服务：</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        phone = re.findall('>点击查看电话</button><.*?>(.*?)<', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        print(name, address, chuangwei, money, object, service, phone)
    except:
        print('出错')

    dbpath = city + '.db'
    # 保存数据库
    data = []
    datalist = []
    try:
        data.append(name)
        data.append(address)
        data.append(chuangwei)
        data.append(money)
        data.append(object)
        data.append(service)
        data.append(phone)
        datalist.append(data)
    except:
        print('chucuo3')


    def init_db(dbpath):
        sql = '''
                  create table company
                   (name test,
                   address test,
                   bed test,
                   money int,
                   style1 test,
                   style2 test,
                   phone int);
                 '''
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()


    if href == href2[0]:
        init_db(dbpath)


    def saveData(dbpath, datalist):

        conn = sqlite3.connect(dbpath)
        cur = conn.cursor()
        for data in datalist:
            for index in range(len(data)):
                sql2 = '''
                           insert into company(
                           name, address, bed, money, style1, style2, phone)
                          values('%s','%s','%s','%s','%s','%s','%s') ''' % (
                    data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            print(sql2)
            cur.execute(sql2)
            conn.commit()
        cur.close()
        conn.close()


    saveData(dbpath, datalist)

    # 创建csv文件以为Excel保存在表格中
    f = open(fileName2, mode="a+", encoding='utf-8')
    csvwriter = csv.writer(f)
    try:
        csvwriter.writerow([name, address, chuangwei, money, object, service, phone])
    except:
        print('chucuo4')
    f.close()
    print('over!2')
    response2.close()

    # 新建excel文件
myexcel = xlwt.Workbook()  # 创建workboook
# 新建sheet页
mysheet = myexcel.add_sheet("testsheet")  # 创建工作表
with open(fileName2, "r", encoding="utf-8") as csvfile:  # 写入数据
    # 读取文件信息
    reader = csv.reader(csvfile)
    # 通过循环获取单行信息
    i = 0
    for data in reader:
        for j in range(len(data)):
            mysheet.write(i, j, data[j])
        i = i + 1
        # 最后保存到excel
    fileName2 = city + '.xls'
    myexcel.save(fileName2)

dbpath = city + '.db'


def selectData(dbpath):
    sql5 = '''
     SELECT bed FROM company'''

    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql5)
    res = cursor.fetchall()
    lst = []
    for line in res:
        print("循环fetchall的值>>>", line)
        lst.append(line)

    conn.commit()
    conn.close()
    return lst


bed = selectData(dbpath)
e = bed
bed = [i[0] for i in e]
print(bed)


def selectData2(dbpath):
    sql6 = '''
     SELECT nam: FROM company'''

    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql6)
    res = cursor.fetchall()
    lst2 = []
    for line in res:
        print("循环fetchall的值>>>", line)
        lst2.append(line)

    conn.commit()
    conn.close()
    return lst2


name = selectData2(dbpath)
e = name
name = [i[0] for i in e]
print(name)












