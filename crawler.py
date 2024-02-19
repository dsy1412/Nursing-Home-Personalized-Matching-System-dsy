# coding=gbk
from flask import Flask, render_template,request
import requests
import re
import csv
import xlwt
import sqlite3

url = 'https://www.yanglao.com.cn/'  # ָ��url
# Uaαװ ����Ӧ���������� User-Agent ��װ��һ���ֵ���
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}
# ����urlЯ���Ĳ��� ��װ���ֵ���
city = input("��������У�")
global fileName2
fileName2 = city + '.csv'

# �������� get�����᷵��һ����Ӧ���� ����Я�������ģ���̬ƴ����url����(�ڶ���������d����������UAαװ��������
child_href_list = []
for item in range(2):  # ѭ��Ϊ��ʹ��ȡ����Ժ��������
    if item == 0:
        url = url + city
    else:
        url = url + "_2"  # ���ڶ�ҳ�Ǽ���_2)

    response = requests.get(url=url, headers=headers)  # �������� get�����᷵��һ����Ӧ����

    response.encoding = 'utf-8'
    page_text = response.text  # ��ȡ��Ӧ���ݣ�text���ص����ַ�����ʽ����Ӧ����
    # �������ݴ�ʱ��ȡ�ĸ�����Ժ�������� Ϊ�´�url��ȡ�̵�
    obj = re.compile('<div class="info">.*?<a target="_blank".*?href="(?P<web>.*?)"', re.S)

    # ��ʼƥ��
    result = obj.finditer(page_text)
    for it in result:  # ����csv�� �޸ĵ�ַ
        if item == 0:
            child_href = url.replace(f'{city}', f"{it.group('web').strip('/')}")
        else:
            child_href = url.replace(f'{city}_2', f"{it.group('web').strip('/')}")
        child_href_list.append(child_href)  # ����ҳ���ַ����
    print('over!1')
    response.close()
href2 = child_href_list
print(href2)
for href in href2:

    headers3 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
    }
    response2 = requests.get(url=href, headers=headers3)  # �������� get�����᷵��һ����Ӧ����
    response2.encoding = 'utf-8'
    page_text2 = response2.text  # ��ȡ��Ӧ���ݣ�text���ص����ַ�����ʽ����Ӧ���� ��ʱ���ص��Ǹ���ҳ����Ϣ

    # fileName2 = city + '.csv'
    # print(fileName2)
    # result2 = obj2.finditer(page_text2)
    # result2 = re.findall(
    #     '<div class="inst-summary">.*?<h1>(?P<name>.*?)</h1>|'
    #     '<li><em>��.*?ַ��</em>(?P<address>.*?)</li>|'
    #     '<li><em>��.*?λ��</em>(?P<chuangwei>.*?)</li>|'
    #     '<li><em>��.*?�ѣ�</em>(?P<money>.*?)</li>|'
    #     '<li><em>��ס����</em>\s*(?P<object>.*?)</li>|'
    #     '<li><em>��ɫ����</em>\s*(?P<service>.*?)</li>'
    #     , page_text2,re.S)
    try:
        name = re.findall('<div class="inst-summary">.*?<h1>(.*?)</h1>', page_text2, re.S)[0].strip().replace('&nbsp;',
                                                                                                              ' ')
        address = re.findall('<li><em>��.*?ַ��</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        chuangwei = re.findall('<li><em>��.*?λ��</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        money = re.findall('<li><em>��.*?�ѣ�</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        object = re.findall('<li><em>��ס����</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        service = re.findall('<li><em>��ɫ����</em>(.*?)</li>', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        phone = re.findall('>����鿴�绰</button><.*?>(.*?)<', page_text2, re.S)[0].strip().replace('&nbsp;', ' ')
        print(name, address, chuangwei, money, object, service, phone)
    except:
        print('����')

    dbpath = city + '.db'
    # �������ݿ�
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

    # ����csv�ļ���ΪExcel�����ڱ����
    f = open(fileName2, mode="a+", encoding='utf-8')
    csvwriter = csv.writer(f)
    try:
        csvwriter.writerow([name, address, chuangwei, money, object, service, phone])
    except:
        print('chucuo4')
    f.close()
    print('over!2')
    response2.close()

    # �½�excel�ļ�
myexcel = xlwt.Workbook()  # ����workboook
# �½�sheetҳ
mysheet = myexcel.add_sheet("testsheet")  # ����������
with open(fileName2, "r", encoding="utf-8") as csvfile:  # д������
    # ��ȡ�ļ���Ϣ
    reader = csv.reader(csvfile)
    # ͨ��ѭ����ȡ������Ϣ
    i = 0
    for data in reader:
        for j in range(len(data)):
            mysheet.write(i, j, data[j])
        i = i + 1
        # ��󱣴浽excel
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
        print("ѭ��fetchall��ֵ>>>", line)
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
        print("ѭ��fetchall��ֵ>>>", line)
        lst2.append(line)

    conn.commit()
    conn.close()
    return lst2


name = selectData2(dbpath)
e = name
name = [i[0] for i in e]
print(name)












