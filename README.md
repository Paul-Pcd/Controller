# Controller
这是我在去年学习Paramiko和Redis时开发的系统监控与运维程序：

- 基于Redis pub/sub通信：    
1、服务端中定义监控配置模板（包括系统监控指标、监控主机组等）并写入Redis；        
2、客户端从Redis中获取模板并根据模板调用插件获取系统监控数据，计算并整理后发布到Redis；    
3、服务端订阅（客户端的发布频道）获取监控数据；
4、目前支持Linux下CPU、内存、网卡的监控（系统异常自动处理有待实现）；

- 基于SSH2协议连接的远程控制（paramiko）：       
1、支持多线程文件分发和命令批量执行；    
2、记录历史操作日志。    
     
## 开发环境
环境 | 版本
---|---
操作系统 | Ubuntu 14.04
数据库 | Redis 3.0.6
开发语言 | Python 2.7.4
IDE | PyCharm 2017.1 x64

## 使用方法
1、安装Redis及python redis模块，以Ubuntu为例：
<pre><code>sudo apt-get install redis-server
sudo pip install redis
</code></pre>

2、启动Redis：
<pre><code>service redis start</code></pre>

3、安装paramiko模块：
<pre><code>sudo pip install paramiko</code></pre>

4、系统监控：   
    
服务端：
<pre><code>python Server/bin/manage.py monitor</code></pre>
客户端：
<pre><code>python Client/bin/manage.py</code></pre>
 
5、系统运维：   
    
服务端：
<pre><code>python Server/bin/manage.py operate</code></pre>

## 运行效果
![Controller](http://ooaovpott.bkt.clouddn.com/Monitor-Operator.png)
 
 ## 注意事项
 1、启用系统监控时必须先启动服务端（把监控模板写入Redis）才能启动客户端，否则客户端获取不到监控指标会报错。     
 2、实现客户端CPU的监控使用sar命令，需要先安装sysstat包：    
 <pre><code>sudo apt-get install sysstat</code></pre>
 3、指定监控指标可修改Server/conf/service.py文件；指定监控组和集群可修改Server/conf/settings.py。    
 4、由于默认以root用户登录，远程执行命令时默认为客户端root用户的根目录。
 5、使用apt-get、yum安装的redis默认绑定本地127.0.0.1，要使其他机器也能访问则修改配置文件（一般为/etc/redis/redis.conf）：
 <pre><code>bind 0.0.0.0</code></pre>
 重新启动redis：
 <pre><code>service redis restart</code></pre>
 6、重新启动程序时出现获取监控数据异常的情况，可以尝试清空redis数据再重新启动服务端程序：
 <pre><code>redis-cli
 127.0.0.1:6379> flushall
 </code></pre>