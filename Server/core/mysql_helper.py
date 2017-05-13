# -*- coding: utf-8 -*-

import MySQLdb
import conf


class MySQLHelper(object):
    def __init__(self):
        self.__ip_port = conf.server_ip_port

    def get_all(self, sql, *params):
        conn = MySQLdb.connect(**self.__ip_port)
        cur = conn.cursor()
        if len(params) == 0:
            res = cur.execute(sql)
        else:
            res = cur.execute(sql, params)
        data = cur.fetchall()
        return (res, data)

    def get_one(self, sql, params):
        conn = MySQLdb.connect(**self.__ip_port)
        cur = conn.cursor()
        res = cur.execute(sql, params)
        data = cur.fetchone()
        return (res, data)

