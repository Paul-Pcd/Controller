#!/usr/bin/env python
# coding:utf-8
# 主程序

import os
import sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from core.main import Operator, Monitor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        msg = '''
            monitor:    lanuch monitor.
             
            operate:    launch operator.
        '''
        sys.exit(msg)
    else:
        if sys.argv[1] == "monitor":
            EntryPoint = Monitor()
        else:
            EntryPoint = Operator()

'''
    测试
    import redis
    r = redis.Redis(host='127.0.0.1', port=6379)
    sub = r.pubsub()
    sub.subscribe('87.7')
    sub.parse_response()
    while True:
        sub.parse_response()
'''