#!/usr/bin/env python
# coding:utf-8
import json
import time
import operator
from conf import settings


# 写入客户端监控配置信息
def save_configs(main_ins, monitor_groups):
    host_config_dic = {}
    for group in monitor_groups:                # group：<templates.LinuxGenericTemplate object at 0x91f846c>
        for ip in group.hosts:
            if ip not in host_config_dic:       # ip：192.168.1.1、192.168.1.2
                host_config_dic[ip] = {}
            for service in group.services:      # service：<services.linux.CPU object at 0x8c8f28c>
                                                # host_config_dic[ip]：{'Memory': ['get_memory_status', 20, 0], }
                host_config_dic[ip][service.name] = [service.plugin_name, service.interval, 0]
    for ip, services in host_config_dic.items():
        main_ins.redis.set(ip, json.dumps(services))


# 读取客户端监控配置信息
def load_configs(monitor_groups):
    host_config_dic = {}
    for group in monitor_groups:
        for ip in group.hosts:
            if ip not in host_config_dic:
                host_config_dic[ip] = {}
            for service in group.services:      # host_config_dic[ip]：<services.linux.CPU object at 0x8c8f28c>
                host_config_dic[ip][service.name] = service
    return host_config_dic


# 处理客户端数据
def data_process(main_ins):
    while True:
        for ip, service in load_configs(settings.MonitorGroups).items():    # 读取客户端监控配置信息
            for service_name, service_instance in service.items():
                service_data = main_ins.redis.get(                          # 读取客户端监控数据
                    '{ip}:{service_name}'.format(
                        ip=ip, service_name=service_name
                    )   # 192.168.1.1:CPU    service_data
                )
                if service_data:    # 成功獲取客戶端數據
                    service_data = json.loads(service_data)
                    time_stamp = service_data['time_stamp']
                    if time.time() - time_stamp < service_instance.interval and service_data['data']['status'] == 0:
                        # 数据有效、且在监控间隔时间内：当前时间 - 数据时间戳 < 监控间隔
                        print("\033[32;1mHost[{ip}] Service[{service_name}] data is valid.\033[0m".format(
                            ip=ip,
                            service_name=service_name
                        ))
                        for item_key, val_dic in service_instance.triggers.items():     # 监控阈值指标、阈值
                            print('\n{time}=========================='.format(
                                time=time.strftime('%Y-%m-%d %H:%M:%S')
                            ))
                            service_item_handle(main_ins, item_key, val_dic, service_data)
                    else:
                        # 超出监控间隔，数据过期
                        print("\033[31;1mHost[{ip}] Service[{service_name}] error has occured.\033[0m" .format(
                            ip=ip,
                            service_name=service_name
                        ))
                else:
                    print("\033[31;1mFailed to get Host[{ip}] Service[{service_name}] data.\033[0m" .format(
                        ip=ip,
                        service_name=service_name
                    ))
            time.sleep(5)


# 分析客户端数据
def service_item_handle(main_ins, item_key, val_dic, service_data):     # 监控阈值指标、阈值、客户端数据
    print '===>  %s\t%s\t%s' %(service_data['service'], item_key, service_data['data'][item_key])
    # Memory    MemUsage_p  25
    item_data = service_data['data'][item_key]      # 客户端（具体指标的）数据
    warning_val = val_dic['warning']                # 监控阈值和计算函数
    critical_val = val_dic['critical']
    operator_val = val_dic['operator']
    oper_func = getattr(operator, operator_val)     # 获取阈值计算函数
    if val_dic['data_type'] is float:
        item_data = float(item_data)                # 阈值与客户端数据比较
        warning_res, critical_res = oper_func(item_data, warning_val), oper_func(item_data, critical_val)
        print("warning: [{warning_threshold}]\tcritical: [{critical_threshold}]".format(
            warning_threshold=warning_val,
            critical_threshold=critical_val
        ))
        print("warning: [{warning_res}]\tcritical: [{critical_res}]".format(
            warning_res=warning_res,
            critical_res=critical_res
        ))
        if critical_res:
            print("\033[41;1mCRITICAL\033[0m       Host[{host}] Service[{service}] threshold[{critical_val}] current[{item_data}]".format(
                host=service_data['host'],
                service=service_data['service'],
                critical_val=critical_val,
                item_data=item_data
            ))
        elif warning_res:
            print("\033[43;1mWARNING\033[0m        Host[{host}] Service[{service}] threshold[{warning_val}] current[{item_data}]".format(
                host=service_data['host'],
                service=service_data['service'],
                warning_val=warning_val,
                item_data=item_data
            ))
        else:
            print("\033[42;1mNORMAL\033[0m         Host[{host}] Service[{service}] threshold[{warning_val}] current[{item_data}]".format(
                host=service_data['host'],
                service=service_data['service'],
                warning_val=warning_val,
                item_data=item_data
            ))