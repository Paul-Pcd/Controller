#!/usr/bin/env python
# coding:utf-8

import redis_helper
from plugins import plugin_api
from conf import settings
import json
import time
import threading
import sys


class Monitor(object):
    
    def __init__(self):
        self.ip = settings.ClientIP
        self.redis = redis_helper.RedisHelper()     # 连接Redis
        self.configs = self.load_configs()          # 从Redis获取配置信息
        self.handle()                               # 启动监控

    # 从Redis获取监控配置信息
    def load_configs(self):
        if self.redis.get(settings.ClientIP):  # 192.168.1.1   {u'Memory': [u'get_memory_status', 20, 0] }
            configs = json.loads(self.redis.get(settings.ClientIP))  # {u'Memory': [u'get_memory_status', 20, 0] }
            return configs
        else:
            sys.exit("Please connect to redis.")

    # 处理监控请求
    def handle(self):
        if self.configs:
            while 1:
                for service, val in self.configs.items():           # linux_memory  [u'get_memory_status', 20, 0]
                    plugin_name, interval, last_run_time = val      # get_memory_status, 20, 0
                    if time.time() - last_run_time < interval:      # 未到监控时间
                        next_run_time = interval - (time.time() - last_run_time)  # 下次监控时间 = 间隔 - (当前时间 - 上次监控时间)
                        print("Service [{service_name}] will run after {next_run_time}s".format(
                            service_name=service,
                            next_run_time=int(next_run_time)
                        ))
                    else:       # 启用多线程调用监控插件
                        print "\033[32;1m Service [{service}] start to run.\033[0m".format(service=service)
                        self.configs[service][2] = time.time()      # 监控配置的第三个字段为“上次监控时间”
                        t = threading.Thread(target=self.call_plugin, args=(service, plugin_name))
                        t.start()   # args: 'Memory' 'get_memory_status'
                time.sleep(1)
        else:
            print "\033[31;1mFailed to get host configs\033[0m"
            
    # 调用监控插件
    def call_plugin(self, service_name, plugin_name):
        func = getattr(plugin_api, plugin_name)     # 根据插件名调用插件函数
        service_data = func()
        report_data = json.dumps({
            'host': self.ip,             # 192.168.1.1
            'service': service_name,     # 'linux_memory'
            'data': service_data,        # {'status': 0, 'MemTotal': '1936996', 'MemUsage': 757860, 'Cached': '802120', 'MemUsage_p': '39', 'SwapFree': '2064548', 'SwapUsage': 32596, 'SwapTotal': '2097144', 'MemFree': '249884', 'SwapUsage_p': '2', 'Buffers': '127132'}
        })
        self.redis.publish(report_data)
