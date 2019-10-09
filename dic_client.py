"""
电子词典服务端
功能：根据用户输入，发送请求，得到结果
结构：一级界面 --> 注册 登录 退出
     二级界面 --> 查单词 历史记录 注销
"""
from socket import *
from getpass import getpass
import sys

# 全局变量
ADDR = ("127.0.0.1", 6666)
# 创建套接字
sockfd = socket()
# 连接服务器
sockfd.connect(ADDR)
# 查询历史
def do_history(name):
    msg = "H" + " "+name
    # 发送信息
    sockfd.send(msg.encode())
    # 接受
    data = sockfd.recv(128).decode()
    if data == "OK":
        while True:
            data = sockfd.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print("您还没有查询记录")

# 查询单词
def do_query(name):
    while True:
        word = input("请输入(输入##退出)：")
        if word == "##":
            break
        data = "Q %s %s" % (name, word)
        # 发送信息
        sockfd.send(data.encode())
        msg = sockfd.recv(2048).decode()
        print(msg)


# 二级界面
def login(name):
    while True:
        print("""
       ==============Query================
       1.查单词       2.查询历史       3.退出
       ===================================
           """)

        cmd = input("请输入选择")
        if cmd == "1":
            do_query(name)
        elif cmd == "2":
            do_history(name)
        elif cmd == "3":
            return
        else:
            print("请输入正确选项")


# 登录操作
def do_login():
    # 输入信息
    user = input("User:")
    passwd = getpass("Passwd:")
    data = "L %s %s" % (user, passwd)
    sockfd.send(data.encode())
    data = sockfd.recv(1024).decode()
    if data == "OK":
        print("登录成功")
        login(user)
    else:
        print("登录失败")


# 注册操作
def do_register():
    while True:
        # 输入用户和密码
        user = input("User:")
        passwd = getpass("Passwd:")
        passwd1 = getpass("Again:")
        if passwd != passwd1:
            print("两次输入请相同")
            continue
        if (' ' in name) or (' ' in passwd):
            print("用户名密码不可以有空格")
            continue
        data = "R %s %s" % (user, passwd)
        # 发送数据
        sockfd.send(data.encode())
        data = sockfd.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login(user)
        else:
            print("注册失败")
        return


def main():
    while True:
        print("""
        ==============Welcome==============
        1.注册         2.登录          3.退出
        ===================================""")

        cmd = input("请输入选择")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            sys.exit()
        else:
            print("请输入正确选项")


if __name__ == '__main__':
    main()
