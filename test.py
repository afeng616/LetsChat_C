#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Afeng
# Time: 2019/11/21 9:19
# Description: 测试

import time
import pymysql


def sql_test():
    db = pymysql.connect(host='localhost', user='root', password='145200')
    cursor = db.cursor()

    account = '3117005390'
    password = 'afeg'

    sql = "select count(*) from db_test.tb_user where id = %s and password = '%s'" % (account, password)
    sql1 = "select username from db_test.tb_user where id = '%s'" % '3117005390'
    sql2 = "insert into db_test.tb_groupmember(id, nickname, status) values('%s', " \
           "(select username from db_test.tb_user where id = '%s'), False)" \
           % ('3117005390', '3117005390')

    cursor.execute(sql2)
    db.commit()
    results = cursor.fetchall()


def dict_test():
    dic = {'aa': 11, 'bbs': 22}
    dic1 = {}
    for i in dic1:
        print('aa' + str(i))


def str_test():
    s = "#[update]asdf"
    print(s[:9])


if __name__ == '__main__':
    sql_test()
