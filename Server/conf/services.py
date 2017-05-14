# coding:utf-8


# 通用监控服务
class BaseService(object):  
    def __init__(self):
        self.name = 'BaseService'               # 监控服务名
        self.interval = 300                     #监控间隔
        self.plugin_name = 'your_plugin_name'   # 插件名
        self.triggers = {}                      # 触发条件


# 监控CPU：需要先安装sysstat（apt-get install sysstat）
class CPU(BaseService):
    def __init__(self):
        super(CPU, self).__init__()             # 执行父类构造函数
        self.name = 'CPU'                       # 服务名
        self.plugin_name = 'get_cpu_status'     # 插件名，对应客户端的监控函数
        self.interval = 30                      # 监控间隔
        self.triggers = {
            'idle': {                           # 状态：空闲
                'func': 'avg',                  # 数值类型：平均值
                'last': 10 * 60,                # 持续时间：10min，单位s
                'operator': 'lt',               # 计算函数：小于
                'count': 1,                     # 触发次数：1次
                'warning': 20,                  # 状态：20%警告，
                'critical': 5,                  # 状态：5%严重警告
                'data_type': float,             # 数据类型：浮点型
            },
             'iowait': {                        # 状态：等待I/O
                 'func': 'hit',                 # 数值类型：超出
                 'last': 15 * 60,               # 数值类型：15min，单位s
                 'operator': 'gt',              # 计算函数：大于
                 'count': 5,                    # 触发次数：5次
                 'warning': 40,                 # 状态：40%警告
                 'critical': 50,                # 状态：50%警告
                 'data_type': float,            # 数据类型：浮点型
             },
        }


# 监控内存
class Memory(BaseService):
    def __init__(self):
        super(Memory, self).__init__()
        self.interval = 20
        self.name = 'Memory'
        self.plugin_name = 'get_memory_status'
        self.triggers = {
            'mem_usage': {
               'func': 'avg',
               'last': 3 * 60,
               'count': 1,
               'operator': 'gt',
               'warning': 60,
               'critical': 80,
               'data_type': float
            },
            'swap_usage': {
               'func': 'avg',
               'last': 3 * 60,
               'count': 1,
               'operator': 'gt',
               'warning': 70,
               'critical': 90,
               'data_type': float
            }
        }


# 监控网卡带宽
class Network(BaseService):
    def __init__(self):
        super(Network,self).__init__()
        self.interval = 60
        self.name = 'Network'
        self.plugin_name = 'get_network_status'
        self.triggers = {
            'in': {
                'func': 'hit',
                'last': 1 * 60,
                'count': 5,
                'operator': 'gt',
                'warning': 3000,        # rxpck/s   每秒接收包数量
                'critical': 4000,
                'data_type': float
             },
             'out': {
                 'func': 'hit',
                 'last': 1 * 60,
                 'count': 5,
                 'operator': 'gt',      # txpck/s   每秒发送包数量
                 'warning': 2000,
                 'critical': 3000,
                 'data_type': float
             }
         }


# 通用监控模板
class BaseTemplate(object):
    def __init__(self):
        self.name = 'TemplateName'
        self.hosts = []
        self.services = []


# 集群1的监控模板
class MonitorTemplate1(BaseTemplate):
    def __init__(self):
        super(MonitorTemplate1, self).__init__()
        self.name = "LinuxCommonServices"
        self.hosts = []
        self.services = [CPU(), Memory(), Network()]


# 集群2的监控模板
class MonitorTemplate2(BaseTemplate):
    def __init__(self):
        super(MonitorTemplate2, self).__init__()
        self.name = "LinuxCommonServices"
        self.hosts = []
        self.services = [Network(), Memory()]       # 实例化监控服务，方便动态修改监控服务的指标
        self.services[0].interval = 35



