#!/usr/bin/env python
import socket
from pathlib import Path

##定义要链接的主机和端口
HOST = 'localhost'
PORT = 10008

def echo_client():
    #AF_INET是IPV4,SOCK_STREAM 是TCP
    ##创建socket对象
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print(f's1:{s}')
    ##与远程建立TCP链接
    s.connect((HOST,PORT))
    print(f's2:{s}')
    while True:
        ##接收用户输入
        filePath = input('input file full path > ')
        if filePath == 'exit':
            break 
        ##读取文件
        p = Path(filePath)
        if p.exists() and p.is_file():
            with open(p,'rb') as f:
                ##发送数据到服务端
                s.sendall(f.read())
        else:
            print(f'file is not exists')
    s.close()

if __name__ == '__main__':
    echo_client()
