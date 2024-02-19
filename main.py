from flask import Flask, render_template, request
import sqlite3
from xpinyin import Pinyin
import pandas as pd
import numpy as np
import math
from numpy import array
from operator import itemgetter, attrgetter

app = Flask(__name__)  # 初始化对象

#网站路径默认为返回首页html
@app.route('/')  # 注意路径与html的区别  路径在加/后随便写0靠用户输入  html是打开网页前就有的 ，提前存在
def shouye():
    return render_template("test/首页.html")

#网站路径/test/register 返回首页./test/register.html
@app.route('/test/register')
def register():
    return render_template("./test/register.html")

#网站路径/result7 返回./test/register.html
@app.route('/result7', methods=['POST', 'GET'])  # 接收表单的提交的路由，需要指定methods为post
def result7():
    if request.method == 'POST':
        #提取指定表单的返回值
        result = request.form
        result = result.to_dict()
        name = result.get('用户名称')
        key = result.get('用户密码')
        return render_template("./test/register.html", user_name=name, user_key=key)

#网站路径/test/用户信息展示 返回./test/用户信息展示.html
@app.route('/test/用户信息展示')  # 接收表单的提交的路由，需要指定methods为post
def result8():
    #从已有数据库中导出信息
    con = sqlite3.connect(f'./user.db')
    cur = con.cursor()
    sql = '''
                        SELECT * FROM company'''
    data = cur.execute(sql)

    return render_template("./test/用户信息展示.html", name=data)

#网站路径/test/用户信息展示 返回./test/用户信息展示.html
@app.route('/result9', methods=['POST', 'GET'])  # 接收表单的提交的路由，需要指定methods为post
def result9():
    if request.method == 'POST':
        # 提取指定表单的返回值
        result = request.form
        p = Pinyin()
        result = result.to_dict()
        name = str(result.get('用户名称'))
        key = str(result.get('用户密码'))
        print('777777777777777')
        print(name)
        print(key)
        conn = sqlite3.connect('user.db')
        # 根据用户输入的表单内容查询已有数据库user.db中的信息
        cur = conn.cursor()
        sql4 = 'select * from company where 用户名称 ="' + name + '" and 用户密码 ="' + key + '"'
        data = cur.execute(sql4)
        lst = []
        for items in data:
            print(items)
            lst.append(items)
        return render_template("./test/用户信息展示.html", name=lst)

#网站路径/test/register2 返回./test/register2.html
@app.route('/test/register2')
def register2():
    return render_template("./test/register2.html")

#网站路径/test/register3 返回首页./test/register3.html
@app.route('/test/register3')
def register3():
    return render_template("./test/register3.html")

#网站路径/result6 返回test/首页.html
@app.route('/result6', methods=['POST', 'GET'])  # 接收表单的提交的路由，需要指定methods为post
def result6():
    # 提取指定表单的返回值
    result = request.form
    p = Pinyin()
    result = result.to_dict()
    name = str(result.get('用户姓名'))
    key = str(result.get('用户密码'))
    return render_template("test/首页.html",name=name,key=key)

#网站路径/result5 返回test/首页.html
@app.route('/result5', methods=['POST', 'GET'])  # 接收表单的提交的路由，需要指定methods为post
def result5():
    if request.method == 'POST':
        # 提取指定表单的返回值
        result = request.form
        p = Pinyin()
        result = result.to_dict()
        name = result.get('blog_name')
        key = result.get('blog_email')

    return render_template("test/首页.html", user_name=name, user_key=key)


#网站路径/result 返回./test/两个柱状图+雷达图+饼图.html
@app.route('/result', methods=['POST', 'GET'])  # 接收表单的提交的路由，需要指定methods为post
def result():
    if request.method == 'POST':
        # 提取指定表单的返回值
        result = request.form
        p = Pinyin()
        result = result.to_dict()
        print(result)
        mm = result['”地址“']
        user_name = result.get('用户名称')
        user_key = result.get('用户密码')
        print(user_name)
        laoren_name = result.get('”姓名“')
        age = result.get('”年龄“')
        xingbie = result.get('”性别“')
        #将用户输入的地址汉字转为拼音
        result2 = p.get_pinyin(mm, '')
        style1_num = []
        style1_num2 = []
        style1_num3 = []
        style1 = []
        con = sqlite3.connect(f'./养老院数据库/{result2}.db')
        cur = con.cursor()
        #提取数据库中指定信息到列表，方便后期传入网页变量
        sql3 = '''
               SELECT style2,count(style2) FROM company group by style1'''
        data = cur.execute(sql3)
        for items in data:
            style1.append(items[0].replace('\t', ' '))
            style1_num.append(items[1])
            import random
            style1_num2.append(items[1] * (round(random.uniform(0.5, 1), 2) + 1))
            style1_num3.append(items[1] * round(random.uniform(0.5, 1), 2))
        cur.close()
        con.close()

        bed_num = []
        name_num = []
        money_num = []
        con = sqlite3.connect(f'./养老院数据库/{result2}.db')
        cur = con.cursor()
        sql = '''
             SELECT * FROM company'''
        data = cur.execute(sql)
        style2_lz = []
        # 提取数据库中指定信息到列表，方便后期传入网页变量
        for items in data:
            style2_lz.append(items[4].replace('\t', ' ').split(' '))
            name_num.append(items[0])
            bed_num.append(int(items[2].strip().replace('张', ' ')))
            num = (int((items[3].strip().split('-'))[0]) + int((items[3].strip().split('-'))[1])) / 2
            money_num.append(num)
        bed_num1 = bed_num
        name_num1 = name_num
        money_num1 = money_num
        bed_num2 = sorted(bed_num1, reverse=True)
        money_num2 = sorted(money_num1)
        style2_lz2 = []
        for items in style2_lz:
            style2_lz2.append(len(items) - 1)
        print(style2_lz)
        print('--------------排序前的信息--------------------------')
        print(bed_num1)
        print(name_num1)
        print(money_num1)
        print('--------------排序后的床位数-----------------------')
        print(bed_num2)
        print()

        print('--------------------特色服务汇总-----------------------')
        print(style1_num)
        print(style1)
        print(style1_num2)
        print(style1_num3)
        print('--------------------特色服务占比------------------------')
        print()
        cur.close()
        con.close()

        name2 = []
        pf = []
        jiage = []
        chuangwei = []
        style_two = []
        con = sqlite3.connect(f'./养老院数据库/{result2}.db')
        cur = con.cursor()
        # 提取数据库中指定信息到列表，方便后期传入网页变量
        sql3 = '''
                        SELECT * FROM COMPANY ORDER BY phone DESC;'''
        data = cur.execute(sql3)
        for items in data:
            pf.append(items[6])
            name2.append(items[0])
            chuangwei.append(int(items[2].strip().replace('张', ' ')))
            jiage.append((int((items[3].strip().split('-'))[0]) + int((items[3].strip().split('-'))[1])) / 2)
        print('-------------------------根据评分打印指定行内容------------------')
        pingfen = pf[:6]
        print(pingfen)
        name2 = name2[:5]
        print(name2)
        chuangwei = chuangwei[:5]
        jiage = jiage[:5]
        print(chuangwei)
        print(jiage)
        print('-------------------------根据评分打印指定行内容结束------------------')
        print()
        cur.close()
        con.close()

        print('-------------------------收住人群------------------------------')
        style_one = []
        con = sqlite3.connect(f'./养老院数据库/{result2}.db')
        cur = con.cursor()
        sql3 = '''
                               SELECT * FROM COMPANY ORDER BY style1 DESC;'''
        data = cur.execute(sql3)
        for items in data:
            style_one.append(items[4].split(' '))
        print(style_one)
        style_num3 = []
        for items in style_one:
            style_num3.append(len(items) - 1)

        zili = [0, 0, 0, 0, 0]
        for item in style_one:
            print(item)
            if len(item) == 1:
                zili[0] += 1
            elif len(item) == 2:
                zili[2] += 1
            elif len(item) == 3:
                zili[0] += 1
                zili[1] += 1
                zili[2] += 1
            elif len(item) == 4:
                zili[1] += 1
                zili[2] += 1
                zili[3] += 1
                zili[0] += 1
            elif len(item) == 5:
                zili[1] += 1
                zili[0] += 1
                zili[4] += 1
        print(zili)
        cur.close()
        con.close()
        print(money_num2)
        print(bed_num2)
        print(style_num3)
        print(style2_lz2)
        print('-------------------------收住人群特定内容查询结束------------------------------')
        print()


        # 权重求解算法：
        # 1.读取数据
        df = pd.read_csv('score.csv', encoding='utf-8')
        # 2数据预处理 ,去除空值的记录
        df.dropna()

        # 定义熵值法函数
        def cal_weight(x):
            '''熵值法计算变量的权重'''
            # 标准化
            x = x.apply(lambda x: ((x - np.min(x)) / (np.max(x) - np.min(x))))
            # 求k
            rows = x.index.size  # 行
            cols = x.columns.size  # 列
            k = 1.0 / math.log(rows)

            lnf = [[None] * cols for i in range(rows)]

            # 矩阵计算--
            # 信息熵
            # p=array(p)
            x = array(x)
            lnf = [[None] * cols for i in range(rows)]
            lnf = array(lnf)
            for i in range(0, rows):
                for j in range(0, cols):
                    if x[i][j] == 0:
                        lnfij = 0.0
                    else:
                        p = x[i][j] / x.sum(axis=0)[j]
                        lnfij = math.log(p) * p * (-k)
                    lnf[i][j] = lnfij
            lnf = pd.DataFrame(lnf)
            E = lnf

            # 计算冗余度
            d = 1 - E.sum(axis=0)
            # 计算各指标的权重
            w = [[None] * 1 for i in range(cols)]
            for j in range(0, cols):
                wj = d[j] / sum(d)
                w[j] = wj
                # 计算各样本的综合得分,用最原始的数据

            w = pd.DataFrame(w)
            return w

        w = cal_weight(df)  # 调用cal_weight
        w.index = df.columns
        w.columns = ['weight']
        print(w)
        print()
        lst = []
        lst.append(round(w['weight'].loc['价格'], 3))
        lst.append(round(w['weight'].loc['床位'], 3))
        lst.append(round(w['weight'].loc['收住人群'], 3))
        lst.append(round(w['weight'].loc['特色服务'], 3))
        lst.append(round(w['weight'].loc['评分'], 3))
        print(lst)
        print('运行完成!')
        return render_template("./test/两个柱状图+雷达图+饼图.html", user_name=user_name, user_key=user_key,
                               laoren_name=laoren_name, age=age, xingbie=xingbie, result=result, result2=result2,
                               bed=bed_num1, name=name_num1, money_px=money_num2, bed_px=bed_num2, money=money_num1,
                               style1_num=style1_num, style1=style1, style1_num2=style1_num2, style1_num3=style1_num3,
                               pingfen=pingfen, lst=lst, name2=name2, jiage=jiage, chuangwei=chuangwei, zili=zili)


#网站路径/result2 返回./test/排序后的结果.html
@app.route('/result2', methods=['POST', 'GET'])  # 接收表单的提交的路由，需要指定methods为post
def result2():
    if request.method == 'POST':
        print('----------------------开始-----------------------')
        result = request.form
        result = result.to_dict()
        print(result)
        # 提取指定表单的返回值
        name = result.get('所在地区')
        user_name = result.get('用户名称')
        user_key = result.get('用户密码')
        laoren_name = result.get('姓名')
        age = result.get('年龄')
        xingbie = result.get('性别')

        p = Pinyin()
        result2 = p.get_pinyin(name, '')
        print(name)
        style_two = []
        name_style2 = []
        con = sqlite3.connect(f'./养老院数据库/{result2}.db')
        cur = con.cursor()
        # 提取数据库中指定信息到列表，方便后期传入网页变量
        sql3 = '''
                                               SELECT * FROM COMPANY ORDER BY style2 DESC;'''
        data = cur.execute(sql3)
        for items in data:
            style_two.append(items[4].split(' '))
            name_style2.append(items[0])
        cur.close()
        con.close()

        bed_num = []
        name_num = []
        money_num = []
        money_normal = []
        style_one2 = []
        style_two2 = []
        pingfen = []
        web = []
        con = sqlite3.connect(f'./养老院数据库/{result2}.db')
        cur = con.cursor()
        # 提取数据库中指定信息到列表，方便后期传入网页变量
        sql = '''
                    SELECT * FROM company'''
        data = cur.execute(sql)
        for items in data:
            name_num.append(items[0])
            web.append(items[7])
            bed_num.append(int(items[2].strip().replace('张', ' ')))
            money_normal.append(items[3])
            num = (int(float((items[3].strip().split('-'))[0]) + int((items[3].strip().split('-'))[1]))) / 2
            money_num.append(num)
            style_one2.append(items[4].split(' '))
            pingfen.append(items[6])
            style_two2.append(items[5].replace('\t', ' ').split(' '))
        print('----------------------------style2-------------------------')
        print(style_one2)
        style_num32 = []
        for i in style_one2:
            style_num32.append(len(i) - 1)
        #进行排序
        print(style_two2)
        style_two322 = []
        for i in style_two2:
            style_two322.append(len(i) - 1)
        bed_num1 = bed_num
        money_num1 = money_num
        money_dict = dict(zip(money_num1, money_normal))
        bed_num2 = sorted(bed_num1, reverse=True)
        money_num2 = sorted(money_num1, reverse=True)
        print('--------------------------hahahhahaha================')
        print(name_num)
        print(bed_num)
        print(money_num)
        print(style_num32)
        print(style_two322)
        print(pingfen)
        print('---------------------结束-----------------------------')

        name_px_bed = []
        money_px_bed = []
        web_px_bed = []
        for i in bed_num2[:10]:
            i = str(i) + '张'
            # 提取数据库中指定信息到列表，方便后期传入网页变量
            sql = 'select * from company where bed ="' + i + '"'
            data = cur.execute(sql)
            for item in data:
                name_px_bed.append(item[0])
                web_px_bed.append(item[7])
                num = (int((item[3].strip().split('-'))[0]) + int((item[3].strip().split('-'))[1])) / 2
                money_px_bed.append(num)
        print('--------------------------')

        name_px_money = []
        bed_px_money = []
        web_px_money = []
        print(money_dict)
        for i in money_num2[:10]:
            money_normal2 = str(money_dict.get(i))
            # 提取数据库中指定信息到列表，方便后期传入网页变量
            sql = 'select * from company where money ="' + money_normal2 + '"'
            data = cur.execute(sql)
            for item in data:
                name_px_money.append(item[0])
                web_px_money.append(item[7])
                bed_px_money.append(int(item[2].strip().replace('张', ' ')))
        print('*' * 50)
        print(bed_px_money)
        print(money_num2)
        print(name_px_money)
        money_bed_dict = dict(zip(bed_px_money, name_px_money))
        bed_px_money2 = sorted(bed_num1, reverse=True)

        name_px_style = []
        bed_px_style = []
        web_px_style = []
        # 提取数据库中指定信息到列表，方便后期传入网页变量
        sql3 = '''
                                                       SELECT * FROM COMPANY ORDER BY style2 DESC;'''
        data = cur.execute(sql3)
        for items in data:
            style_two.append(items[4].split(' '))
            name_style2.append(items[0])
        #将两列表组成列表，方便后面提取键值
        style_dict = dict(zip(name_style2, style_two))

        style_num = []
        money_px_style = []
        for item in style_two:
            style_num.append(len(item))
        # 将两列表组成列表，方便后面提取键值
        style_dict2 = dict(zip(style_num, style_two))
        print(style_dict)
        print(style_dict2)
        style_num = sorted(style_num, reverse=True)

        print('----------')
        style_num = list(set(style_num))
        for i in style_num[:10]:
            j = style_dict2.get(i)
            #根据键值返回关键字
            def get_key(val):
                for key, value in style_dict.items():
                    if val == value:
                        return key

                return "There is no such Key"

            money_normal2 = get_key(j)
            print(money_normal2)
            # 提取数据库中指定信息到列表，方便后期传入网页变量
            sql = 'select * from company where name ="' + money_normal2 + '"'
            data = cur.execute(sql)
            for item in data:
                web_px_style.append(item[7])
                name_px_style.append(item[0])
                bed_px_style.append(int(item[2].strip().replace('张', ' ')))
                money_px_style.append((int((item[3].strip().split('-'))[0]) + int((item[3].strip().split('-'))[1])) / 2)
        print(name_px_style)
        print(bed_px_style)
        print(money_px_style)

        cur.close()
        con.close()

        lst1 = name_num
        lst2 = money_num
        lst3 = bed_num
        lst4 = style_num32
        lst5 = style_two322
        lst6 = pingfen
        lst7 = web
        lst_lst = []
        # 提取数据库中指定信息到列表，方便后期传入网页变量
        try:
            quanzhong1 = result.get("权重一")
            quanzhong2 = result.get("权重二")
            quanzhong3 = result.get("权重三")
            quanzhong4 = result.get("权重四")
            quanzhong5 = result.get("权重五")
            quanzhong_lst = f'{quanzhong1}、{quanzhong2}、{quanzhong3}、{quanzhong4}、{quanzhong5}'
        except:
            print()

        for i in range(len(lst1)):
            lst_all = (lst1[i], lst2[i], lst3[i], lst4[i], lst5[i], lst6[i], lst7[i])
            lst_lst.append(lst_all)
        # 根据用户表单不同内容 传入界面不同值
        if result.get("床位数") != None:
            print('biaodancunzai--1')

            return render_template("./test/排序后的结果.html", web=web_px_bed, name='床位数降序', user_name=user_name,
                                   user_key=user_key, laoren_name=laoren_name, age=age, xingbie=xingbie,
                                   name2=name_px_bed, bed=bed_num2, money=money_px_bed)
        elif result.get("特色服务涵盖") != None:
            print('biaodancunzai--1')
            return render_template("./test/排序后的结果.html", web=web_px_style, name='特色服务降序', user_name=user_name,
                                   user_key=user_key, laoren_name=laoren_name, age=age, xingbie=xingbie,
                                   name2=name_px_style, bed=bed_px_style, money=money_px_style)
        elif result.get("价格") != None:
            print('biaodancunzai--3')
            return render_template("./test/排序后的结果.html", web=web_px_money, name='价格降序', user_name=user_name,
                                   user_key=user_key, laoren_name=laoren_name, age=age, xingbie=xingbie,
                                   name2=name_px_money, money=money_num2, bed=bed_px_money)
        elif result.get("权重一") == '价格' and result.get("权重二") == '床位':
            s = sorted(lst_lst, key=itemgetter(2), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(1), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '价格' and result.get("权重二") == '收住人群':
            s = sorted(lst_lst, key=itemgetter(3), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(1), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            bed_px_money_bed = []
            web_t = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", web=web_t, result2=result2, user_name=user_name,
                                   user_key=user_key, laoren_name=laoren_name, age=age, xingbie=xingbie,
                                   name=quanzhong_lst, name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed)
        elif result.get("权重一") == '价格' and result.get("权重二") == '特色服务':
            s = sorted(lst_lst, key=itemgetter(4), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(1), reverse=True)
            print(ss)
            ss = ss[:10]
            web_t = []
            name_px_money_bed = []
            money_1 = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", web=web_t, result2=result2, user_name=user_name,
                                   user_key=user_key, laoren_name=laoren_name, age=age, xingbie=xingbie,
                                   name=quanzhong_lst, name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed)
        elif result.get("权重一") == '价格' and result.get("权重二") == '评分':
            s = sorted(lst_lst, key=itemgetter(5), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(1), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", web=web_t, result2=result2, user_name=user_name,
                                   user_key=user_key, laoren_name=laoren_name, age=age, xingbie=xingbie,
                                   name=quanzhong_lst, name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed)
        elif result.get("权重一") == '床位' and result.get("权重二") == '价格':
            s = sorted(lst_lst, key=itemgetter(1), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(2), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_chj = []
            money_chj = []
            web_t = []
            bed_px_money_chj = []
            for i in ss:
                name_px_money_chj.append(i[0])
                money_chj.append(i[1])
                bed_px_money_chj.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", web=web_t, result2=result2, user_name=user_name,
                                   user_key=user_key, laoren_name=laoren_name, age=age, xingbie=xingbie,
                                   name=quanzhong_lst, name2=name_px_money_chj, money=money_chj, bed=bed_px_money_chj)
        elif result.get("权重一") == '床位' and result.get("权重二") == '收住人群':
            s = sorted(lst_lst, key=itemgetter(3), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(2), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_shz = []
            money_shz = []
            web_t = []
            bed_px_money_shz = []
            for i in ss:
                name_px_money_shz.append(i[0])
                money_shz.append(i[1])
                bed_px_money_shz.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, web=web_t, name=quanzhong_lst,
                                   name2=name_px_money_shz, money=money_shz, bed=bed_px_money_shz)
        elif result.get("权重一") == '床位' and result.get("权重二") == '特色服务':
            s = sorted(lst_lst, key=itemgetter(4), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(2), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_shz = []
            money_shz = []
            web_t = []
            bed_px_money_shz = []
            for i in ss:
                name_px_money_shz.append(i[0])
                money_shz.append(i[1])
                bed_px_money_shz.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, web=web_t, name=quanzhong_lst,
                                   name2=name_px_money_shz, money=money_shz, bed=bed_px_money_shz)
        elif result.get("权重一") == '床位' and result.get("权重二") == '评分':
            s = sorted(lst_lst, key=itemgetter(5), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(2), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_shz = []
            money_shz = []
            web_t = []
            bed_px_money_shz = []
            for i in ss:
                name_px_money_shz.append(i[0])
                money_shz.append(i[1])
                bed_px_money_shz.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_shz, money=money_shz, bed=bed_px_money_shz, web=web_t)
        elif result.get("权重一") == '收住人群' and result.get("权重二") == '价格':
            s = sorted(lst_lst, key=itemgetter(1), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(3), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '收住人群' and result.get("权重二") == '床位':
            s = sorted(lst_lst, key=itemgetter(2), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(3), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '收住人群' and result.get("权重二") == '特色服务':
            s = sorted(lst_lst, key=itemgetter(4), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(3), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '收住人群' and result.get("权重二") == '评分':
            s = sorted(lst_lst, key=itemgetter(5), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(3), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                web_t = []
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '特色服务' and result.get("权重二") == '价格':
            s = sorted(lst_lst, key=itemgetter(1), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(4), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            bed_px_money_bed = []
            web_t = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '特色服务' and result.get("权重二") == '床位':
            s = sorted(lst_lst, key=itemgetter(2), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(4), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '特色服务' and result.get("权重二") == '收住人数':
            s = sorted(lst_lst, key=itemgetter(3), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(4), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '特色服务' and result.get("权重二") == '评分':
            s = sorted(lst_lst, key=itemgetter(5), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(4), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '评分' and result.get("权重二") == '价格':
            s = sorted(lst_lst, key=itemgetter(1), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(5), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '评分' and result.get("权重二") == '收住人群':
            s = sorted(lst_lst, key=itemgetter(3), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(5), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '评分' and result.get("权重二") == '特色服务':
            s = sorted(lst_lst, key=itemgetter(4), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(5), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            bed_px_money_bed = []
            web_t = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("权重一") == '评分' and result.get("权重二") == '床位':
            s = sorted(lst_lst, key=itemgetter(2), reverse=True)
            print('----排序后=-')
            ss = sorted(s, key=itemgetter(5), reverse=True)
            print(ss)
            ss = ss[:10]
            name_px_money_bed = []
            money_1 = []
            web_t = []
            bed_px_money_bed = []
            for i in ss:
                name_px_money_bed.append(i[0])
                money_1.append(i[1])
                bed_px_money_bed.append(i[2])
                web_t.append((i[6]))
            return render_template("./test/排序后的结果.html", result2=result2, user_name=user_name, user_key=user_key,
                                   laoren_name=laoren_name, age=age, xingbie=xingbie, name=quanzhong_lst,
                                   name2=name_px_money_bed, money=money_1,
                                   bed=bed_px_money_bed, web=web_t)
        elif result.get("文件") !=None:
            return render_template("./test/排序后的结果.html", web=web_px_money, name='文件提交', user_name=user_name,
                                   user_key=user_key, laoren_name=laoren_name, age=age, xingbie=xingbie,
                                   name2=name_px_money, money=money_num2, bed=bed_px_money)

#网站路径/result3 返回./test/内联框架_详细信息.html
@app.route('/result3', methods=['POST', 'GET'])  # 接收表单的提交的路由，需要指定methods为post
def result3():
    # 此时将用户输入的表单内筒保存
    if request.method == 'POST':
        # 提取指定表单的返回值
        result = request.form
        result = result.to_dict()
        print(result)
        result = request.form
        web = result.get('具体')
        px_way = result.get('排序方式')
        yanglao_name = result.get('具体2')
        user_name = result.get('用户名称')
        user_key = result.get('用户密码')
        laoren_name = result.get('姓名')
        age = result.get('年龄')
        xingbie = result.get('性别')

        return render_template("./test/内联框架_详细信息.html", user_name=user_name, user_key=user_key, laoren_name=laoren_name,
                               age=age, xingbie=xingbie, web=web, px_way=px_way, name=yanglao_name)

#网站路径/result4 返回./test/首页.html
@app.route('/result4', methods=['POST', 'GET'])  # 接收表单的提交的路由，需要指定methods为post
def result4():
    # 此时将用户输入的表单内筒保存
    if request.method == 'POST':
        conn = sqlite3.connect('user.db')
        cur = conn.cursor()
        result = request.form
        result = result.to_dict()
        # 提取指定表单的返回值
        px_way = result.get('排序方式')
        yanglao_name = result.get('养老院名称')
        user_name = result.get('用户名称')
        user_key = result.get('用户密码')
        laoren_name = result.get('姓名')
        age = result.get('年龄')
        xingbie = result.get('性别')

        pd = result.get("是否收藏")
        print('5555555555555555555555555555555555555')

        print(type(yanglao_name))
        print(type(px_way))
        px_way = f'{px_way}'
        print(pd)
        print(yanglao_name)
        print(px_way)
        data = []
        datalist = []
        data.append(user_name)
        data.append(user_key)
        data.append(laoren_name)
        data.append(age)
        data.append(xingbie)
        data.append(px_way)
        data.append(yanglao_name)
        print(data)
        datalist.append(data)
        # 提取数据库中指定信息到列表，方便后期传入网页变量
        for data in datalist:
            sql2 = '''
                                     insert into company(
                                     用户名称,用户密码,姓名,年龄,性别,排序方式,养老院)
                                    values('%s','%s','%s','%s','%s','%s','%s') ''' % (
                data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            cur.execute(sql2)
            conn.commit()
        cur.close()
        conn.close()
        return render_template("./test/首页.html",user_key=user_key,user_name=user_name)


if __name__ == '__main__':
    app.run(debug=True)  # 启动服务器
