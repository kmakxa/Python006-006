# 学习笔记（第一周）

## Python的安装

到官网选择一个想下载版本的安装包

[python官网下载地址](https://www.python.org/downloads/)

我选择的是3.7.9的版本，点击了版本号后，由于是windows系统，我直接选择了可执行文件。

[Windows x86-64 executable installer](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe)

安装的时候，最好把python直接安装在盘的根目录下面，不要有太长的安装路径，并且最好不要有中文。

安装后开启命令行cmd

执行python -V 成功查看到版本号即可

## Python执行时解释器的选择

我们平时执行的python 这个命令，实际上调用的是python的解释器，将我们编写的代码文件转换为字节码，并传递给python的虚拟机

想判断当前执行python解析器，具体使用的python版本是什么的时候，可以使用python -V命令。

在选择解析器的时候，是按顺序在PATH路径下逐步寻找符合的命令。在PATH中越前面的文件夹越早能找到。如果想要让python命令找到对应的版本，可以把对应版本的安装路径在PATH中的位置往前调整。

对于类UNIX系统，可以加环境变量的修改配置

```shell
vi /etc/profile
##添加修改PATH的命令
export PATH = 'python包位置':$PATH
```

同时**pip**命令也会有类似的影响，pip用于管理python的依赖包

pip会将扩展包安装到对应python安装目录下面的：site-packages中

## REPL（python的交互式解析器）

1. type(变量) ：可以获取变量的类型
2. help(类型)：可以列出可用的方法
3. 没法通过tab进行命令补全

使用ipython增强命令交互环境

## pip 加速

修改pip源

1. 方法一：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip(要安装的包) -U(如果是升级加上该参数)
2. 方法二：pip config set global.index-url http://pypi.doubanio.com/simple/  |pip install pip -U

要永久修改的话

```shell
##window 创建 C:/user/xx/pip/pip.ini
##linux 创建~/.pip/pip.conf
##文件内容为
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```



## python的IDE

1. vscode
2. pycharm
3. jupyter notebook

vscode工具上需要安装的插件：

1. rainbow fart:能用不同的颜色标志多对括号
2. chinese：中文界面的支持
3. python:能更好的显示python代码，当我们打开python文件的时候会自动推荐安装

vscode的常用快捷键：

1. 格式化代码：shift+alt+f
2. 跳往上下个单词：ctrl+左右方向键
3. 移动到代码开头和结尾/行首行尾：ctrl+home/end  &home/end
4. 单行移动代码：alt+上下方向键
5. 单行复制代码：shift+alt+上下方向键
6. 代码注释：ctrl+/
7. 单独执行选中代码：选中代码后shift+回车

jupyter notebook:使用pip install -i jupyter 后执行jupyter notebook就可以启动网页版的编辑器了

## 虚拟环境

```shell
##创建一个虚拟环境
python -m venv venv1(此处为虚拟环境目录的名称)
##激活虚拟环境
source venv1/bin/activate
##确认python解析器的地址
which python
##回到原始环境
deactivate
```

利用虚拟环境进行版本的迁移

```shell
##确保python版本是一致的
python -V
##切换到虚拟环境
source venv1/bin/activate
##在虚拟环境中查看第三方库,并输出到一个文件中
pip3 freeze > requirements.txt

##进入到生产环境中，进入虚拟环境
source venv2/bin/activate
##查看python 和pip的版本是否一致
python -V
pip -V
which python
##从文件中读取依赖来进行安装
pip install -r ./requirements.txt
##进行核对
pip3 freeze
```

## python的基础数据类型

1. None:空值
2. Bool:布尔值
3. 数值：整数、浮点数、复数
4. 序列：字符串、列表、元组
5. 集合：字典
6. 可调用：函数

基础数据类型和java的差别并不大。列表就像list,字典就像map,元组就是不可变的list.

```python
##空值
a = None
a is None
##布尔值
a = True
b = False
##数值
i = 1
f = 1.3
c = complex(4,5)
##序列
s = "567"
lst = [5,6,7]
yz = (5,6,7)
##不可变的整数序列range
r = range(1,10,2)
list(r)
##二进制序列bytes,bytearray,memoryview
value = b'\xf0\xf1\xf2'
ba = bytearray(b'.\xf0\xf1\xf2')
##set
se = {5,6,7}
##dist
di = {"A":"B","C":"D"}
```



## python的高级数据类型

collections:容器数据类型

1. nametuple():命名元组
2. deque：双端队列
3. counter:计数器
4. OrderedDict:有顺序的字典

详细可以查看python标准库的文档

## 控制流

1. if 和else :与shell和java的写法差别不大，区别在与后面带:，要注意缩进
2. while: 一样的，while后面跟条件即可。（ps:类似i++的写法，在python 中是 i+=1）
3. for: 与java类似 for i in list

## 函数与模块

模块：由函数组成，被应用的py文件

包：由多个模块，通过特殊处理形成的文件夹

```python
##想让模块在被引入的时候，不执行方法的执行时
if __name__ == '__main__':
    ##执行的语句
```

## python的标准库

### 日期时间（time&datetime)

```python
import time
##获取当前时间-数值
time.time()
##可阅读的结构化的时间
time.localtime()
##将结构化的时间处理为字符串
time.strftime("%Y-%m-%d %X",time.localtime())
##将字符串转换回结构化时间
time.strptime('2020-12-27 01:31:33',"%Y-%m-%d %X")
```

时间的偏移

```python
from datetime import datetime
from datetime import timedelta
##获取当前时间datetime.now()也是一样效果
datetime.today()
##获取昨天的时间
datetime.today()-timedelta(days=1)
```

### 日志处理（logging）

日志的级别

1. info:日常打印的信息
2. warning:不影响应用程序的执行的警告
3. error:需要关注或优化的信息
4. critical:灾难性的问题，非常严重
5. debug:调试级别的日志

```python
##打印日志,默认只有info级别以上的日志才会被打印
import logging
logging.debug("debug log")
logging.info("info log")
logging.warning("warning log")
logging.error("error log")
logging.critical("critical log")
##对日志进行配置，logging的basicConfig
logging.basicConfig(filename='test.log',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(name)-8s %(levelname)-8s [line:%(lineno)d] %(message)s')
```

### 常用处理(random&json&pathlib)

随机数

```python
from random import *
##生成一个0.0-1.0之间的浮点数
random.random()
##从A到B，以C为步长生成随机数
random.randrange(A,B,C)
##从列表中随机获取1个元素
random.choice(['A','B','C'])
##从列表中随机获取n个元素
random.sample(['A','B','C','D'],k=2)
```

json

```python
import json
##加载json
json.loads('["foo",{"bar":["baz",null,1.0,2]}]')
##使用json进行序列化
json.dumps(['foo', {'bar': ['baz', None, 1.0, 2]}])
```

路径处理

```python
from pathlib import Path
##实例化
p=Path()
##获取当前路径
p.resolve()	
##获取当前脚本的绝对路径
p=Path(__file__)
##提取路径信息
path='C:/testfile/test.txt.py'
p=Path(path)
##获取文件名称
p.name
##去除后缀的文件名
p.stem
##获取文件的后缀
p.suffix
##多扩展名时获取多个后缀
p.suffixes
##获取路径名称
p.parent
##获取所有上级路径
for i in p.parents:
    print(i)
##对路径进行分割
p.parts
```

```python
import os
##获取完整路径
os.path.abspath('test.log')
path='/usr/local/a.txt'
##获取文件名称
os.path.basename(path)
##获取目录名称
os.path.dirname(path)
##判断文件或目录是否存在
os.path.exists(path)
##判断是否文件/目录
os.path.isfile(path)/os.path.isdir(path)
##路径的拼接
os.path.join(path1,path2)
```

### 守护进程（daemon）

查看范式说明：

[daemon范式](https://www.python.org/dev/peps/pep-3143/)

[stackoverflow上的介绍](https://stackoverflow.com/questions/473620/how-do-you-create-a-daemon-in-python)

老师git上的样例

```python
#!/usr/bin/env python
import sys
import os
import time

'''
手动编写一个daemon进程
'''

def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:

        # 创建子进程
        pid = os.fork()

        if pid > 0:
            # 父进程先于子进程exit，会使子进程变为孤儿进程，
            # 这样子进程成功被init这个用户级守护进程收养
            sys.exit(0)

    except OSError as err:
        sys.stderr.write('_Fork #1 failed: {0}\n'.format(err))
        sys.exit(1)

    # 从父进程环境脱离
    # decouple from parent environment
    # chdir确认进程不占用任何目录，否则不能umount
    os.chdir("/")
    # 调用umask(0)拥有写任何文件的权限，避免继承自父进程的umask被修改导致自身权限不足
    os.umask(0)
    # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离
    os.setsid()

    # 第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            # 第二个父进程退出
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('_Fork #2 failed: {0}\n'.format(err))
        sys.exit(1)

    # 重定向标准文件描述符
    sys.stdout.flush()
    sys.stderr.flush()

    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'w')

    # dup2函数原子化关闭和复制文件描述符
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

# 每秒显示一个时间戳
def test():
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid()) 
    while True:
        now = time.strftime("%X", time.localtime())
        sys.stdout.write(f'{time.ctime()}\n') 
        sys.stdout.flush() 
        time.sleep(1)

if __name__ == "__main__":
    daemonize('/dev/null','/Users/edz/Downloads/demo/d1.log','/dev/null')
    test()
```

使用pyython标准库

```python
#!/usr/bin/python
import time
from daemon import runner

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
    def run(self):
        while True:
            print("Howdy!  Gig'em!  Whoop!")
            time.sleep(10)

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
```

### 正则表达式（re）

元字符介绍：

1. .:任意的字符
2. \*：任意个字符 ，和.连用的话就是任意个数的任意字符
3. ^:以什么开头
4. $:以什么结尾
5. +：1次到任意次

```python
import re
##当要反复使用时采用
prog = re.compile(patten)
result = prog.match(string)
##单次使用
result = re.match(patten,string)
##判断字符串是否手机
content = "13345355336"
re.match(".{11}",content)
##匹配成功并返回内容
re.match(".{11}",content).group()
##匹配成功了多少位
re.match(".{10}",content).span()
##匹配的邮箱，把匹配的内容用括号进行分组，就可以使用group取出结果
content = "abc@123.com"
re.match("(.*)@(.*)",content).group()
re.match("(.*)@(.*)",content).group(1)
re.match("(.*)@(.*)",content).group(2)

##查找字符串search返回第一个
re.search("@","abc@123.com")
##查找所有匹配上的字符串
re.findall("[1-9]","abc@123.com")
##替换字符串,此处例子为单独的数字替换为字母
re.sub("\d","x","abc@123.com")
##字符串分割
re.split("@","abc@123.com")
##字符串分割，分割符也进行保留
re.split("(@)","abc@123.com")
```



# 感想与总结

问题：

1. 我们的生产环境，一般都不能连接外网通过pip去直接下载安装包，是否能有离线的包安装方法的教程？
2. pathlib和os.path在课程中的讲解来看，功能并不完全重合，是否能完全使用pathlib来替代os.path呢？如果不行的话，不就用os.path更好了吗？因为课程中虽然建议使用pathlib后面又说要结合使用,但是介绍的场景，os.path的场景比pathlib还更多。

感想：

第一周的基础课程非常有用，为我们的学习打下了良好的基础，特别是标准库的介绍，对我的帮助特别的大，基本上能涵盖日常写一些小工具的大部分场景了。而且连IDE的一些基础操作也能有涉猎，从我个人的角度来说真的获益良多，提升了编码效率，在课程的设置中包含了这些内容真的很赞。