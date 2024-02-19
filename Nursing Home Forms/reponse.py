# coding=gbk
import requests
import re
import csv
import xlwt
if __name__ == '__main__':
    url = 'https://www.yanglao.com.cn/resthome/19115.html'  # ָ��url
    # Uaαװ ����Ӧ���������� User-Agent ��װ��һ���ֵ���
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }
    # ����urlЯ���Ĳ��� ��װ���ֵ���
    city = input("��������У�")
    # �������� get�����᷵��һ����Ӧ���� ����Я�������ģ���̬ƴ����url����(�ڶ���������d����������UAαװ��������
    for item in range(2):

        response = requests.get(url=url, headers=headers)  # �������� get�����᷵��һ����Ӧ����
        response.encoding = 'GBK'
        response.encoding = 'utf-8'
        page_text = response.text  # ��ȡ��Ӧ���ݣ�text���ص����ַ�����ʽ����Ӧ����
        # ��������
        obj = re.compile(
            r'<div class="inst-summary">.*?<h1> (?P<name>.*?) </h1>'
            r".*?<li>.*?<em>��ַ��</em>.*?(?P<adress>.*?).*?</li>"
            r".*?�������ͣ�</em>(?P<let>.*?)"
            r".*?�������ʣ�</em>(?P<mom>.*?)"
            r".*?��λ����</em>(?P<fom>.*?)"
            r".*?��ס����</em>(?P<who>.*?)"
            r".*?�շ����䣻</em>(?P<dog>.*?)"
            , re.S)
        # ��ʼƥ��
        fileName = city + '.csv'
        result = obj.finditer(page_text)
        print(result)
        f = open(fileName, mode="w", encoding='utf-8')
        csvwriter = csv.writer(f)
        for it in result:
            dic = it.groupdict()
            csvwriter.writerow(dic.values())
        f.close()
        response.close()
        print('over!')
    # �½�excel�ļ�
    myexcel = xlwt.Workbook()
    # �½�sheetҳ
    mysheet = myexcel.add_sheet("testsheet")
    with open(fileName, "r", encoding="utf-8") as csvfile:
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
