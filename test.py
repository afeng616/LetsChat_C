#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Afeng
# Time: 2019/11/21 9:19
# Description: 测试

import pymysql


def sql_test():
    db = pymysql.connect('localhost', 'root', '145200')
    cursor = db.cursor()

    account = '3117005390'
    password = 'afeg'

    sql = "select count(*) from db_test.tb_user where id = %s and password = '%s'" % (account, password)

    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    print(results[0][0] == 1)


if __name__ == '__main__':
    sql_test()
