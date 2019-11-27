#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Description: 客户端进程操作（使用多线程）
# Author: Afeng
# Date: 2019/11/24

import os
import pymysql
import _thread
import logging
from module.utils import *
from tkinter import *

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


# UDP相关进程处理
class UDPProcess(object):
    def __init__(self, text_history):
        self.text_history = text_history
        self.ip = '127.0.0.1'
        self.port = 12306
        self.addr = (self.ip, self.port)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.recv()

    # 发送信息
    def send_data(self, message):
        self.socket.sendto(message.encode('utf-8'), self.addr)
        logging.info('send：' + message + ' to ' + str(self.addr))

    def send(self, message):
        _thread.start_new_thread(self.send_data, (message,))

    # 接收消息
    def recv_data(self):
        try:
            while True:
                # TODO: 心跳机制完善
                self.socket.sendto(''.encode('utf-8'), self.addr)

                message, addr = self.socket.recvfrom(1024)
                message = str(message.decode('utf-8')).strip(' ')
                if message:
                    self.update_message(message)

                logging.info('from ' + str(addr) + ' get: ' + message)
        except:
            logging.error('服务器维护中...暂时无法正常使用')
            os._exit(-1)

    def recv(self):
        _thread.start_new_thread(self.recv_data, ())

    # 更新消息展示框UI
    def update_message(self, message):
        self.text_history.config(state=NORMAL)
        self.text_history.insert('end', get_time() + ' Others（' + get_ip() + '）：\n    '
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
        self.cursor.execute(sql % (account, password))
        self.db.commit()
        results = self.cursor.fetchall()
        return results[0][0] == 1
