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
        return self.conn.set(key, value)
        
    def set_ex(self, key, value, expire):   # 赋值（包括过期时间）
        return self.conn.set(name=key, value=value, ex=expire)

    def keys(self, pattern='*'):    # 取所有值
        return self.conn.keys(pattern)
    
    def delete(self, key):          # 删除
        return self.conn.delete(key)
    
    def publish(self, msg):         # 发布
        return self.conn.publish(self.chan_pub, msg)
        
    def subscribe(self):            # 订阅
        pub = self.conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub
'''
    pub = conn.pubsub()
    pub.subscribe('87.7')
    pub.parse_response()
    while True:
        pub.parse_response()
'''

