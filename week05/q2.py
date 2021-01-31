import redis

client = redis.Redis(host='server1', password='hUN7e4_1')

def sendsms(telephone_number: int, content: str, key=None):
    count_number = 0
    if not client.exists(telephone_number) :
        client.set(telephone_number, 1, nx=True)
        client.expire(telephone_number,60)
        count_number = 1
    else:
        count_number = client.incr(telephone_number)
    if count_number <= 5:
        print("发送成功")
    else:
        print("相同手机号最多发送五次功能,1 分钟后重试稍后")
    
