#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Afeng
# Time: 2019/11/21 9:24
# Description: UDP Server

from socket import *

IP = 'localhost'
PORT = 12306
ADDR = (IP, PORT)

# 创建UDP套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)

while True:
    send_data = input("请输入发送到" + IP + "的数据：")
    if send_data:
        udp_socket.sendto(send_data.encode('utf-8'), ADDR)
    # recv_data = udp_socket.recvfrom(1024)
    # if recv_data[0]:
    #     print("接收到" + recv_data[1] + "发来数据：" + recv_data[0].decode('gbk'))
