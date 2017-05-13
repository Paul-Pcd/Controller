#!/usr/bin/env python
# coding:utf-8
from conf import settings
import redis_helper
import serialize
import json
import time
import threading
import signal
import paramiko
import select
import os
import sys

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)


# 监控模块
class Monitor(object):

    def __init__(self):
        self.redis = redis_helper.RedisHelper()     # 连接Redis
        self.save_configs()                         # 把配置信息写入Redis
        self.data_handle()                          # 处理客户端监控数据
        self.save_monitor_data()                    # 保存客户端监控数据

    # 把所有配置信息写入Redis，供客户端提取调用
    def save_configs(self):
        serialize.save_configs(self, settings.MonitorGroups)

    # 多线程处理客户端数据
    def data_handle(self):      # 设置信号，使子线程也能接收到信号而退出
        signal.signal(signal.SIGINT, sys.exit)         # SIGINT：Ctrl+C
        signal.signal(signal.SIGTERM, sys.exit)        # SIGTERM：更友好的退出，kill命令默认不带参数发送的信号
        t = threading.Thread(target=self.data_process)
        t.setDaemon(True)                               # 守护线程，随主线程退出而退出
        t.start()

    # 处理客户端数据
    def data_process(self):
        serialize.data_process(self)

    # 处理客户端信息并存入Redis
    def save_monitor_data(self):
        chan_sub = self.redis.subscribe()   # 从订阅频道接收信息
        while 1:
            # chan_sub.parse_response()：['message', '87.7', {'host': '127.0.0.1', 'service': 'cpu', 'data': xxx}]
            host_service_data = json.loads(chan_sub.parse_response()[2])
            # host_service_data：{'host': '127.0.0.1', 'service': 'cpu', 'data': xxx, 'time_stamp': 1494659857.091}
            host_service_data['time_stamp'] = time.time()
            self.redis.set(
                '{host_ip}:{service_name}'.format(
                    host_ip=host_service_data['host'], service_name=host_service_data['service']
                ), json.dumps(host_service_data)
            )    # 键：192.168.1.1:CPU    值：data

    # 警告处理接口
    def alert_handle(self):
        pass


# 运维模块
class Operator(object):

    def __init__(self):
        print("Remote control system.")
        self.ip_list = []
        for cluster in settings.MonitorGroups:
            for ip in cluster.hosts:
                self.ip_list.append(ip) # 获取所有监控组的所有ip
        self.run()

    # 启动控制器
    def run(self):
        self.cmd = raw_input('Please input your command: ')
        if self.cmd == 'file':      # 输入命令，file表示启用文件分发，其余命令直接执行
            self.file_distribute()
        else:
            self.remote_control_all()

    # 分发文件
    def send_file(self, ip, file):
        ip_port = (ip, 22)
        t = paramiko.Transport(ip_port)     # 建立SSH连接
        t.connect(username=settings.Client_Username, password=settings.Client_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(file, file)                # 发送文件
        t.close()

    # 批量分发文件
    def file_distribute(self):
        thread_list = []
        file = raw_input('Please input filename: ')
        for ip in self.ip_list:
            thread_list.append(
                threading.Thread(
                    target=self.send_file,
                    args=(ip, file)
                )
            )                   # 创建远程控制线程并添加到列表
        for t in thread_list:   # 遍历线程列表并启动
            t.setDaemon(True)
            t.start()

    # 远程控制（注意连接后的目录默认为root的家目录）
    def remote_control(self, ip, cmd, output_filename):
        s = paramiko.SSHClient()        # 远程连接到客户机并执行命令
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            s.connect(ip, 22, settings.Client_Username, settings.Client_password)       # 连接指定的客户机
            transport = s.get_transport()
            channel = transport.open_session()      # 建立一个会话通道
            channel.get_pty()
            channel.exec_command(cmd)               # 执行命令
            print("\n================================================")
            print("ip: {}                command: {}".format(ip, cmd))
            f = open(output_filename, 'a+')
            f.write('\n\n\n====== %s    %s ======\n\n' % (ip, time.strftime('%Y-%m-%d %H:%M:%S')))
            while True:
                if channel.exit_status_ready():                     # 返回退出状态则结束循环
                    break
                # 异步方式获取远程命令的执行结果，有返回内容时即感知到channel的改变，把内容返回给rl
                readable, writable, error = select.select([channel], [], [], 1)
                if len(readable) > 0:                               # 可读列表不为空则读取最大长度消息，输出并写入文件
                    recv = channel.recv(65536)
                    print(recv)
                    f.write(str(recv))                              # 把执行命令的结果写入日志文件
                    f.flush()
        except Exception as e:
            print(e)

    # 批量远程控制
    def remote_control_all(self):
        thread_list = []
        for ip in self.ip_list:
            ctime = time.strftime('%Y-%m-%d')
            log_dir = BASEDIR + '/log/'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            output_filename = log_dir + ip + '_' + ctime + '_' + '.log'
            self.remote_control(ip, self.cmd, output_filename)
            thread_list.append(
                threading.Thread(
                    target=self.remote_control,
                    args=(ip, self.cmd, output_filename)
                )
            )                   # 创建远程控制线程并添加到列表
        for t in thread_list:   # 遍历线程列表并启动
            t.setDaemon(True)
            t.start()
