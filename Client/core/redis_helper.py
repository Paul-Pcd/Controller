# coding:utf-8
import redis
from conf import settings


class RedisHelper(object):
    
    def __init__(self):
        self.conn = redis.Redis(host=settings.RedisServer, port=settings.RedisPort)
        self.chan_sub = settings.RedisSubChannel
        self.chan_pub = settings.RedisPubChannel

    def get(self, key):             # 取值
        return self.conn.get(key)
    
    def set(self, key, value):      # 赋值
        self.conn.set(key, value)
        
    def keys(self, pattern='*'):    # 取所有值
        return self.conn.keys(pattern)
    
    def publish(self, msg):         # 发布消息
        self.conn.publish(self.chan_pub, msg)
        
    def subscribe(self):            # 订阅消息
        pub = self.conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
