# 多人电子字典
author: 木星王
usepycharm
## 项目简介
基于tcp套接字的多人电子词典查询项目用多进程的技术，可实现在局域网内通过连接服务器实现单词查询，同时使用mysql数据库储存用户信息，在存入数据时对用户信息加密。

## 功能简介
1. 用户登录
2. 用户注册
3. 查询单词
4. 查询历史
## 注意点：
1. 在使用之前请详细阅读程序设计的markdown文档
2. 使用input_word.py进行单词的导入
3. 涉及到连接数据库的操作请自行修改用户名和密码
4. 在客户端中ADDR设置的是默认本机的地址，如果想要别的电脑进行连接请换成自己电脑的地址
5. 本程序应设计多进程，请在linux系统下运行服务端。
6. 客户端请在终端下运行！