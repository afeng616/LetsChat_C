#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Afeng
# Time: 2019/11/21 10:04
# Description: TCP Client

from socket import *

IP = "192.168.1.109"
PORT = 12345

# 创建TCP套接字
tcp_client_socket = socket(AF_INET, SOCK_STREAM)
tcp_client_socket.connect((IP, PORT))

while True:
    send_data = input("请输入发送的数据：")
    if send_data:
        tcp_client_socket.send(send_data.encode('utf-8'))
    recv_data = tcp_client_socket.recv(1024)
    if recv_data[0]:
        print('接收到服务端' + IP + '回复数据：' + recv_data.decode('utf-8'))
