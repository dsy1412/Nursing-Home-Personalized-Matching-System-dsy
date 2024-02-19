# coding=gbk
import requests
import re
import csv
import xlwt
if __name__ == '__main__':
    url = 'https://www.yanglao.com.cn/resthome/19115.html'  # 指定url
    # Ua伪装 将对应的请求载体 User-Agent 封装到一个字典中
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }
    # 处理url携带的参数 封装到字典中
    city = input("请输入城市：")
    # 发起请求 get方法会返回一个相应对象 且是携带参数的，动态拼接在url后面(第二个参数）d第三个参数UA伪装请求载体
    for item in range(2):

        response = requests.get(url=url, headers=headers)  # 发起请求 get方法会返回一个相应对象
        response.encoding = 'GBK'
        response.encoding = 'utf-8'
        page_text = response.text  # 获取响应数据，text返回的是字符串形式的响应数据
        # 解析数据
        obj = re.compile(
            r'<div class="inst-summary">.*?<h1> (?P<name>.*?) </h1>'
            r".*?<li>.*?<em>地址：</em>.*?(?P<adress>.*?).*?</li>"
            r".*?机构类型；</em>(?P<let>.*?)"
            r".*?机构性质：</em>(?P<mom>.*?)"
            r".*?床位数；</em>(?P<fom>.*?)"
            r".*?收住对象；</em>(?P<who>.*?)"
            r".*?收费区间；</em>(?P<dog>.*?)"
            , re.S)
        # 开始匹配
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
    # 新建excel文件
    myexcel = xlwt.Workbook()
    # 新建sheet页
    mysheet = myexcel.add_sheet("testsheet")
    with open(fileName, "r", encoding="utf-8") as csvfile:
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
