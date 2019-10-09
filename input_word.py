"""
将字典输入数据库
"""
import re
import pymysql

# 连接数据库
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="debian-sys-maint",
                     password="RbqeSkfgdC1BP1Ta",
                     database="dict",
                     charset="utf8")
# 获取游标
cur = db.cursor()
pattern = r"(\S+)\s+(.*)"
sql = r"insert into words (word,meaning) values (%s,%s)"
try:
    # 读取文件
    with open("dict.txt") as f:
        # 循环读取每行的单词
        for item in f:
            # 匹配单词和意思
            words = re.findall(pattern, item)
            cur.execute(sql, [words[0][0], words[0][1]])
except Exception as e:
    db.rollback()
    print(e)

db.commit()
cur.close()
db.close()
