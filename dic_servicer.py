"""
电子词典服务端
业务逻辑的处理
模型：多进程 tcp并发
"""
from operation_db import DataBase
from socket import *
from multiprocessing import Process
import signal, sys
from time import sleep

# 全局变量
ADDR = ("0.0.0.0", 8888)
# 连接数据库
db = DataBase(database="dict")
# 查询历史记录
def do_history(connfd,data):
    name = data.split(" ")[1]
    r = db.history(name)
    if not r:
        connfd.send(b"Fail")
        return
    connfd.send(b"OK")
    for i in r:
        msg = "%s %-16s %s"%i
        sleep(0.1)
        connfd.send(msg.encode())
    sleep(0.1)
    # 发送结束的标志
    connfd.send(b"##")

# 查单词
def do_query(connfd, data):
    temp = data.split(" ")
    name = temp[1]
    word = temp[2]
    mean = db.query( word)
    db.insert_history(name,word)
    if mean:
        msg ="%s : %s"% (word, mean)
    else:
        msg = "没有该单词"
    connfd.send(msg.encode())


# 登录
def do_login(connfd, data):
    temp = data.split(" ")
    name = temp[1]
    passwd = temp[2]
    result = db.login(name, passwd)
    if result:
        connfd.send(b"OK")
    else:
        connfd.send(b"Flase")


# 注册
def do_register(connfd, data):
    temp = data.split(" ")
    name = temp[1]
    passwd = temp[2]
    if db.register(name, passwd):
        connfd.send(b"OK")
    else:
        connfd.send(b"False")


# 接受客户端请求，分级处理
def request(connfd):
    # 创建游标
    db.create_curour()
    data = connfd.recv(1024).decode()
    if not data or data[0] == "E":
        return  # 对应子进程退出
    elif data[0] == "R":
        do_register(connfd, data)
    elif data[0] == "L":
        do_login(connfd, data)
    elif data[0] == "Q":
        do_query(connfd, data)
    elif data[0] == "H":
        do_history(connfd,data)

def main():
    # 创建tcp套节字
    sockfd = socket()
    # 绑定地址
    sockfd.bind((ADDR))
    # 设置监听
    sockfd.listen(5)
    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    # 循环等待客户连接
    print("Listen the port 6666")
    while True:
        try:
            connfd, addr = sockfd.accept()
            print("Connect from ", addr)
        except KeyboardInterrupt:
            sockfd.close()
            db.close()
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue
        request(connfd)
        # 为客户端创建子进程
        p = Process(target=request, args=(connfd,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
