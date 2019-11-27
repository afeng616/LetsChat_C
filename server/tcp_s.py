#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Afeng
# Time: 2019/11/21 10:03
# Description: TCP Server

from socket import *

ADDR = ('', 12345)

tcp_server_socket = socket(AF_INET, SOCK_STREAM)
tcp_server_socket.bind(ADDR)
tcp_server_socket.listen(128)

client_socket, client_addr = tcp_server_socket.accept()
while True:
    recv_data = client_socket.recv(1024)
    if recv_data:
        print('接收到' + client_addr[0] + '发来数据：' + recv_data.decode('utf-8'))
    client_socket.send("隔这呢".encode('utf-8'))
    print('服务端已回复：隔这呢')
