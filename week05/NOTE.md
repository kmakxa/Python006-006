# 学习笔记（第五周缓存）

## Redis的安装

redis的特点

1. 使用IO多路复用
2. 监听多个文件描述符实现读写事件
3. 单线程工作（6.0以前）

redis的数据类型

1. 字符串
2. 列表
3. 哈希
4. 集合
5. 有序集合

```shell
##升级gcc来编译安装redis
yum install centos-release-scl scl-utils-build
yum list all --enablerepo='centos-sclo-rh'
yun install -y devtoolset-8-toolchain
scl enable devtoolset-8 bash
gcc --version
##gcc是8版本以上的就可以了
##查看端口看是否成功启动
ss -ntpl|grep 6379
##服务器端通过客户端连接
redis-cli
>>auth [密码]
>>shutdown
```

通过python连接redis

```python
# 连接 Redis
import redis
# pip3 install redis

client = redis.Redis(host='server1', password='hUN7e4_1')

print(client.keys())

for key in client.keys():
    print(key.decode())
```

## Python对redis的操作

### 字符串

```python
# 操作string
import redis

client = redis.Redis(host='server1', password='hUN7e4_1')
##nx=True参数可以当key已经存在value时不进行覆盖
client.set('key', 'value3', nx=True)
##append可以让字符串在原有基础上进行拼接
client.append('key', 'value4')
result = client.get('key')

client.set('key2', '100')
##当保存的是数值类型时，统一通过这个方法进行+1
result2 = client.incr('key2')  # +1
##当保存的是数值类型时，统一通过这个方法进行-1
print(result2)
result3 = client.decr('key2')  # -1
print(result3)

print(result.decode())

# 不要贸然使用keys * 指令,会造成redis短暂不响应
# 数据量在百万级以下的话，可以使用字符串进行保存，更大的话建议采用hash方式，是字符串资源的1/4左右
```

### 列表

```python
# 操作list
import redis

client = redis.Redis(host='server1', password='hUN7e4_1')

# 存入列表
# client.lpush('list_redis_demo', 'python')
# client.rpush('list_redis_demo', 'java')

# 查看长度
print(client.llen('list_redis_demo'))

# 弹出数据
# lpop() rpop()
# data = client.lpop('list_redis_demo')
# print(data)

# 查看一定范围的list数据
# data = client.lrange('list_redis_demo', 0, -1)
# print(data)
##遍历处理所有数据
while True:
    phone = client.rpop('list_redis_demo')
    if not phone:
        print('发送完毕')
        break

    # sendsms(phone)
    # result_times = retry_once(phone)
    # if result_times >= 5:
    #     client.lpush('list_redis_demo', phone)
##获取所有数据
data = client.lrange('list_redis_demo', 0, -1)
print(data)
```

### 集合

```python
# 操作set
import redis

client = redis.Redis(host='server1', password='hUN7e4_1')
##给集合添加元素
print(client.sadd('redis_set_demo', 'new_data'))
##随机弹出一个集合的元素
# client.spop()
##获取集合中的所有成员
# client.smembers('redis_set_demo')

# 交集
client.sinter('set_a', 'set_b')

# 并集
client.sunion('set_a', 'set_b')

# 差集
client.sdiff('set_a', 'set_b')
```

### 哈希

```python
# 操作hash
import redis

client = redis.Redis(host='server1', password='hUN7e4_1')

# client.hset('vip_user', '1001', 1)
# client.hset('vip_user', '1002', 1)
# client.hdel('vip_user', '1002')
##是否存在
# print(client.hexists('vip_user','1001'))

# 添加多个键值对
# client.hmset('vip_user', {'1003':1, '1004':1})
# hkeys hget hmget(获取多个) hgetall（获取所有）
field = client.hkeys('vip_user')
print(field)
print(client.hget('vip_user', '1001'))
print(client.hgetall('vip_user'))
# bytes
```

### 有序集合

```python
# 操作zset
import redis

client = redis.Redis(host='server1', password='hUN7e4_1')
##加入集合
# client.zadd('rank', {'a': 4, 'b': 3, 'c': 1, 'd': 2, 'e': 5})
##对集合某个元素的分值进行操作
# client.zincrby('rank', -2, 'e')
##按顺序取前5
print(client.zrangebyscore('rank', 1, 5))
# zrevrank  从大到小
# 基card-不包含分值的底
print(client.zcard('rank'))
# 显示评分-正向前三
print(client.zrange('rank', 0, 2, withscores=True))
# 显示评分-反向前三
print(client.zrevrange('rank', 0, 2, withscores=True))

```

## Redis的关键机制

生存时间：

1. LRU
2. LFU

可用性

1. 主从复制:写主，读主、从，只能一主多从
2. 哨兵：可以通知客户端，并升级一个从服务器为主服务器，并让其他从服务器转换。起码有3个节点作为哨兵来作为冲裁，为奇数值，能保证投票结果。



## 消息队列

用途

1. 异步处理
2. 流量控制
3. 服务解耦

模型

1. 队列模型
2. 发布-订阅模型

## RabbitMq的主要结构

使用的是AMQP协议

RabbitMQ是AMQP的代理服务器，在通信的过程中采用的是RPC的方式

```shell
##RabbitMQ的安装
yum install rabbitmq-server
##启动管理插件
rabbitmq-plugins enable rabbitmq_management
##启动rabbitMq :默认端口是5672，插件端口是15672和25672
systemctl start rabbitmq-server
##通过浏览器访问，15672端口可以进行web页面，使用默认guest/guest作为管理员登录
```

rabbitMQ的独有概念

1. direct:生产者和消费者一一对应
2. topic:多个交换机到一个队列
3. fanout:一个生产者可以对应多个队列。

## Python使用rabbitmq-队列

生产者

```python
# 生产者代码
import pika
# pip3 install pika

# 用户名和密码
credentials = pika.PlainCredentials('guest', 'hUN7e4_1')

# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
parameters = pika.ConnectionParameters(host='server1',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)
# 阻塞方法
connection = pika.BlockingConnection(parameters)

# 建立信道
channel = connection.channel()

# 声明消息队列
# 如不存在自动创建
# durable=True 队列持久化
channel.queue_declare(queue='direct_demo', durable=False)

# exchange指定交换机
# routing_key指定队列名
channel.basic_publish(exchange='', routing_key='direct_demo',
                      body='send message to rabbitmq')

# 关闭与rabbitmq server的连接
connection.close()

```

消费者

```python
# 消费者代码
import pika

credentials = pika.PlainCredentials('guest', 'hUN7e4_1')

parameters = pika.ConnectionParameters(host='server1',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# 声明消息队列
channel.queue_declare(queue='direct_demo', durable=False)

# 定义一个回调函数来处理消息队列中的消息
def callback(ch, method, properties, body):

    # 手动发送确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # 实现如何处理消息
    print(body.decode())

# 消费者使用队列和哪个回调函数处理消息
channel.basic_consume('direct_demo',on_message_callback=callback)

# 开始接收信息，并进入阻塞状态
channel.start_consuming()

```

## Python使用rabbitmq-发布订阅

生产者

```python
# 生产者代码
import pika

# 用户名和密码
credentials = pika.PlainCredentials('guest', 'hUN7e4_1')

# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
parameters = pika.ConnectionParameters(host='server1',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)
# 阻塞方法
connection = pika.BlockingConnection(parameters)

# 建立信道
channel = connection.channel()

# 声明消息队列
# 如不存在自动创建
# durable=True 队列持久化
channel.queue_declare(queue='task_queue', durable=True)

message = 'send message to taskqueue'
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # 消息持久化
                      ))


# 关闭与rabbitmq server的连接
connection.close()

```

消费者

```python
# 消费者代码
import pika
import time

credentials = pika.PlainCredentials('guest', 'hUN7e4_1')

parameters = pika.ConnectionParameters(host='server1',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# 声明消息队列
channel.queue_declare(queue='task_queue', durable=True)

# 定义一个回调函数来处理消息队列中的消息


def callback(ch, method, properties, body):


    time.sleep(1)
    print(body.decode())
    # 手动确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 如果该消费者的channel上未确认的消息数达到了prefetch_count数，则不向该消费者发送消息
channel.basic_qos(prefetch_count=1)

# 消费者使用队列和哪个回调函数处理消息
channel.basic_consume('task_queue', callback)

# 开始接收信息，并进入阻塞状态
channel.start_consuming()

```

交换情况的生产者

```python
# 生产者代码
import pika

# 用户名和密码
credentials = pika.PlainCredentials('guest', 'hUN7e4_1')

# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
parameters = pika.ConnectionParameters(host='server1',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)
# 阻塞方法
connection = pika.BlockingConnection(parameters)

# 建立信道
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = 'send message to fanout'
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message,
                      )

# 关闭与rabbitmq server的连接
connection.close()

```

交换机-消费者

```python
# 消费者代码
import pika


credentials = pika.PlainCredentials('guest', 'hUN7e4_1')

parameters = pika.ConnectionParameters(host='server1',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# 声明交换机
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# 声明消息队列
# exclusive 当与消费者断开连接的时候，队列被立即删除
result = channel.queue_declare(queue='',
                               exclusive=True)
queue_name = result.method.queue

# 通过bind实现exchange将message发送到指定的queue
channel.queue_bind(exchange='logs',
                   queue=queue_name)


# 定义一个回调函数来处理消息队列中的消息
def callback(ch, method, properties, body):

    print(body.decode())
    # 手动确认消息
    # ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
# 消费者使用队列和哪个回调函数处理消息
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)


# 开始接收信息，并进入阻塞状态
channel.start_consuming()

```

## 消息队列的常见问题

如何保证事务在分布式消息队列下的一致性？

：使用分布式事务，组件会提供不同的参数。各组件不一样

如何保证消息不会丢？

：通过消息确认的机制，结合消息序号的监控

如何处理重复消息？

：至多一次|至少一次|恰好一次-》尽量通过幂等性解决。

## RPC与gRPC

基于proto,使用tcp协议，进行二进制数据的交换

proto样例

```shell
syntax = "proto3";
 
package schema;
 
service Gateway {
    rpc Call(stream Request) returns (stream Response){}
}
 
message Request {
    int64 num = 1;
}
 
message Response {
    int64 num = 1;
}
```

编写好上面文件后，产生Python文件:

python3 -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. ./sechma.proto

grpc-server

```python
# grpcio 是启动 gRPC 服务的项目依赖
# pip3 install grpcio
# gPRC tools 包含 protocol buffer 编译器和用于从 .proto 文件生成服务端和客户端代码的插件
# pip3 install grpcio-tools
# 升级protobuf
# pip3 install --upgrade protobuf -i https://pypi.douban.com/simple

import grpc
import time
import schema_pb2
import schema_pb2_grpc
from concurrent import futures
 
 
class GatewayServer(schema_pb2_grpc.GatewayServicer):
 
    def Call(self, request_iterator, context):
        for req in request_iterator:
            yield schema_pb2.Response(num=req.num+1)
            time.sleep(1)
 
 
def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schema_pb2_grpc.add_GatewayServicer_to_server(GatewayServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
 
 
if __name__ == "__main__":
    main()
```

grpc-client

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import queue
import schema_pb2
import schema_pb2_grpc
queue = queue.Queue()
def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = schema_pb2_grpc.GatewayStub(channel)
        queue.put(1)
        resp = stub.Call(generate_message())
        for r in resp:
            num = r.num
            queue.put(num)
def generate_message():
    while True:
        num = queue.get()
        print(num)
        yield schema_pb2.Request(num=num)
if __name__ == "__main__":
    main()

```

