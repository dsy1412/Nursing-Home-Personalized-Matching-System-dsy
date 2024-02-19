import sqlite3

bed_num = []
name_num = []
money_num = []
con = sqlite3.connect("yantai.db")
cur = con.cursor()
sql = '''
     SELECT * FROM company'''
data = cur.execute(sql)
for items in data:
    name_num.append(items[0])
    bed_num.append(int(items[2].strip().replace('张', ' ')))
    num=(int((items[3].strip().split('-'))[0])+int((items[3].strip().split('-'))[1]))/2
    money_num.append(num)

print(bed_num)
print(name_num)
print(money_num)
cur.close()
con.close()
