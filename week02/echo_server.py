#!/usr/bin/env python
import socket
from pathlib import Path
import time
##定义要链接的主机和端口
HOST = 'localhost'
PORT = 10008

def echo_server():
    #AF_INET是IPV4,SOCK_STREAM 是TCP
    ##创建socket对象
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print(f's1:{s}')
    ##将socket对象与端口进行绑定
    s.bind((HOST,PORT))
    ##只接受1个链接
    s.listen(1)
    print(f's2:{s}')
    while True:
        ##接收用户的远程链接
        conn, addr = s.accept()
        ##输出客户端地址
        print(f'connnet by {addr}')
        ##准备写入的文件名：
        file_name = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
        p = Path(__file__)
        recv_file = p.resolve().parent.joinpath(file_name)
        with open(recv_file,'wb+') as f:
            while True:
                data = conn.recv(1024)
                if not data:                    
                    break
                f.write(data)
        conn.close()
    s.close()

if __name__ == '__main__':
    echo_server()