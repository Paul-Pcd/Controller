# coding:utf-8
import services

Cluster1 = services.MonitorTemplate1()      # 主机集群：集群内的主机监控相同的模板（项目和指标）
Cluster1.hosts = ['127.0.0.1', ]
Cluster2 = services.MonitorTemplate2()
Cluster2.hosts = ['192.168.1.3', '192.168.1.4']
MonitorGroups = [Cluster1]                  # 监控组：对加入组内的集群启动监控服务

RedisServer = '127.0.0.1'       # Redis服务端ip
RedisPort = 6379                # Redis服务端端口
RedisSubChannel = '87.7'        # 服务端订阅频道
RedisPubChannel = '103'         # 服务端发布频道

MySQL_HOST = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '123456',
    'db': 'clients_management'
}

Client_Username = 'root'
Client_password = '123456'