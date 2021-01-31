
import redis

client = redis.Redis(host='server1', password='hUN7e4_1')

def counter(video_id: int):
    if client.exists(video_id) :
        client.set(video_id, 1, nx=True)
        count_number = 1
    else:
        count_number = client.incr(video_id)
    return count_number

if __name__ == '__main__':
    counter('1001')
