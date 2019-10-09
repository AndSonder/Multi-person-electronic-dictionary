"""
数据库操作
"""
import pymysql
import hashlib

salt = b"*#06#"  # 加密专用盐


# 　加密处理函数
def encryption(passwd):
    # 对密码进行加密处理
    hash = hashlib.md5(salt)
    hash.update(passwd.encode())
    return hash.hexdigest()  # 获取存储密码


class DataBase:
    def __init__(self, host="localhost",
                 port=3306,
                 user="debian-sys-maint",
                 passwd="RbqeSkfgdC1BP1Ta",
                 database=None,
                 charset="utf8"
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_database()

    # 连接数据库
    def connect_database(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset,
                                  )

    # 创建游标
    def create_curour(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.db.close()

    # 登录
    def register(self, name, passwd):
        sql = r"select * from user where name='%s'" % name
        # 判断用户时候存在
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return False
        # 密码加密
        passwd = encryption(passwd)
        try:
            sql = r"insert into user (name,passwd) values (%s,%s)"
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(e)

    # 登录
    def login(self, name, passwd):
        passwd = encryption(passwd)
        sql = r"select * from user where name='%s'and passwd='%s'" % (name, passwd)
        # 判断用户是否存在
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False

    # 查单词
    def query(self, word):
        sql = "select meaning from words where word='%s'" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]


    # 存入查询记录
    def insert_history(self, name, word):
        sql = "insert into history (name,word) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
        except:
            self.db.rollback()

    #查询历史记录
    def history(self,name):
        sql = "select name,word,time from history where name = '%s' order by time desc limit 10"%name
        self.cur.execute(sql)
        return self.cur.fetchall()
