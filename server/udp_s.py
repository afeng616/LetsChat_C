#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Afeng
# Time: 2019/11/21 9:41
# Description: UDP Client仅接收Server发送内容

from socket import *

# 绑定本地地址，端口
LOCAL_ADDR = ('', 12306)

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(LOCAL_ADDR)

while True:
    # 接收数据
    recv_data = udp_socket.recvfrom(1024)
    if recv_data[0]:
        print(recv_data[1])
        print("接收到" + recv_data[1][0] + "发来数据：" + recv_data[0].decode('utf-8'))
