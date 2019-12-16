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
    def __init__(self, text_history):
        self.text_history = text_history
        self.ip = '127.0.0.1'  # 服务器为本机
        self.port = 12306
        self.addr = (self.ip, self.port)  # 服务器地址
        self.socket = socket(AF_INET, SOCK_DGRAM)

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
        self.socket.sendto('#[update]'.encode('utf-8'), self.addr)
        try:
            while True:
                message, addr = self.socket.recvfrom(1024)
                message = str(message.decode('utf-8')).strip(' ')
                if message[:] != '#[update]':
                    self.update_message(message)

                logging.info('get: [' + message + '] from ' + str(addr))
        except:
            logging.error('服务器维护中...暂时无法正常使用')
            os._exit(-1)

    def recv(self):
        _thread.start_new_thread(self.recv_data, ())

    # 心跳机制
    def keep_alive(self):
        while True:
            time.sleep(3)  # 粗略的循环定时器
            self.socket.sendto('#[update]'.encode('utf-8'), self.addr)
            logging.info('维持心跳')

    def alive(self):
        _thread.start_new_thread(self.keep_alive, ())

    # 更新消息展示框UI
    def update_message(self, message):
        self.text_history.config(state=NORMAL)
        self.text_history.insert('end', get_time() + ' Others（' + self.ip + '）：\n    '
                                 + message + '\n')
        self.text_history.config(state=DISABLED)


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
