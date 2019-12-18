#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Description: 客户端进程操作（使用多线程）
# Author: Afeng
# Date: 2019/11/24

import os
import time
import pymysql
import _thread
import logging
from module.utils import *
from tkinter import *

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
NAME = 'LetsChat_C '
VERSION = 'V0.1-local'


# UDP相关进程处理
class UDPProcess(object):
    def __init__(self, text_history, list_persons, account):
        self.text_history = text_history
        self.list_persons = list_persons
        self.account = account
        self.ip = '127.0.0.1'  # 服务器为本机
        self.port = 12306
        self.addr = (self.ip, self.port)  # 服务器地址
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.users_id = []  # 存储在线用户id  ['id', ]
        self.members = []  # 群用户成员  [('id', 'nickname'), ]
        self.process = SQLProcess()

    def start(self):
        self.alive()  # 维持心跳
        self.recv()  # 接收信息

    # 发送信息
    def send_data(self, message):
        self.socket.sendto(message.encode('utf-8'), self.addr)
        logging.info('send: [' + message + '] to ' + str(self.addr))

    def send(self, message):
        _thread.start_new_thread(self.send_data, (message,))

    # 接收消息
    def recv_data(self):
        self.socket.sendto(''.encode('utf-8'), self.addr)
        try:
            while True:
                # TODO: 使用昵称代替ip
                # TODO: 服务端发来上线下线通知
                # TODO: 客户端做出上线下下通知响应（用户列表变色，消息栏显示）
                message, addr = self.socket.recvfrom(1024)
                message = str(message.decode('utf-8')).strip(' ')
                if message[:9] == '#[update]':  # 加载全部在线用户（仅进行一次）
                    self.users_id = message[9:].split(',')
                    logging.info('初始化在线用户id表')
                elif message:
                    self.update_message(message)
                    logging.info('get: [' + message + '] from ' + str(addr))
        except:
            logging.error("服务器正在维护中...请稍后使用")
            os._exit(-1)

    def recv(self):
        _thread.start_new_thread(self.recv_data, ())

    # 心跳机制
    def keep_alive(self):
        while True:
            self.socket.sendto(('#[update]' + str(self.account)).encode('utf-8'), self.addr)
            logging.info('维持心跳')
            time.sleep(3)  # 粗略的循环定时器

    def alive(self):
        _thread.start_new_thread(self.keep_alive, ())

    # 更新消息展示框UI
    def update_message(self, message):
        self.text_history.config(state=NORMAL)
        self.text_history.insert('end', get_time() + ' Others（' + self.ip + '）：\n    '
                                 + message + '\n')
        self.text_history.config(state=DISABLED)

    # 初始化成员列表组件
    def init_users_status(self):
        # 获取群成员
        for _, i in self.members:
            self.list_persons.insert(END, str(i))
        for i, user in enumerate(self.list_persons.get(0, len(self.members))):
            # 更改用户状态
            if user in self.users_id:
                self.list_persons.itemconfig(i, fg='green')
            else:
                self.list_persons.itemconfig(i, fg='red')

    # 更新用户状态
    def update_users_status(self, user_id, status):
        nickname = self.process.nickname(user_id)
        index = self.members.index((user_id, nickname))
        self.list_persons.itemconfig(index, fg='green' if status else 'red')
        logging.info(user_id + '上线' if status else '下线')


# 数据库相关进程处理
class SQLProcess(object):
    def __init__(self):
        self.db = pymysql.connect('localhost', 'root', '145200')
        self.cursor = self.db.cursor()

    # 登录检测
    def login(self, account, password):
        sql = "select count(*) from db_test.tb_user where id = %s and password = '%s'"
        try:
            self.cursor.execute(sql % (account, password))
            self.db.commit()
        except Exception as e:
            logging.info("账号或密码错误" + str(e))
            return False
        results = self.cursor.fetchall()
        return results[0][0] == 1

    # TODO: 用户注册
    def register(self):
        return False

    # 群聊权限检测
    def join(self, account):
        sql = "select status from db_test.tb_groupmember where id='%s'"
        try:
            self.cursor.execute(sql % account)
            self.db.commit()
            return self.cursor.fetchall()[0][0] == 1
        except:
            return False

    # 进群申请
    def join_apply(self, account):
        sql1 = "select count(*) from db_test.tb_groupmember where id=%s" % account
        sql2 = "insert into db_test.tb_groupmember(id, nickname, status) values('%s', " \
               "(select username from db_test.tb_user where id = '%s'), False)" % (account, account)
        self.cursor.execute(sql1)
        self.db.commit()
        if self.cursor.fetchall()[0][0]:
            logging.info("重复申请")
        else:
            self.cursor.execute(sql2)
            self.db.commit()

    # 获取成员
    def members(self):
        sql = "select id, nickname from db_test.tb_groupmember where status=True order by nickname"
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()

    # 通过id获取昵称
    def nickname(self, id):
        sql = "select nickname from db_test.tb_groupmember where id='%s'" % id
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()[0][0]
