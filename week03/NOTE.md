# 学习笔记(第三周-Mysql)

## Mysql的安装

Linux 查看当前系统的架构：arch

查看系统的版本：cat /etc/redhat-release

```shell
##通过网络yum命令进行安装
yum install mysql57-community-release-el7-10.noarch.rpm
yum install mysql-community-server
##安装完以后，移除自动更新
yum remove mysql57-community-release-el7-10.noarch
##启动mysql
systemctl start mysqld.service
##设置随系统自动启动
systemctl enable mysqld
##查看mysql的运行状态
systemctl status mysqld.service
##查看mysql的安装版本
rpm -qa | grep -i 'mysql'
##获取管理员密码
grep 'password' /var/log/mysqld.log | head -1
##修改用户密码
alter USER 'root'@'localhost' identified by 'NEW_PASSWORD';
##显示密码的安全需求
show variables like 'validate_password%';
##修改策略变量
set global validate_password_policy=0;


```

## Mysql的字符集

```sql
##查看字符集
show variables like '%character%';
##查看校对规则
show variables like '%collation_%'
##修改字符集
vi /etc/my.cnf
##加入[mysql]\[client]
default_character_set = utf8mb4
##加入[mysqld]
init_connect='SET collation_connection = utf8mb4_unicode_ci'
init_connect='SET NAMES utf8mb4'
character_set_server=uft8mb4
collation_server=uft8mb4_unicode_ci
character_set_client_handshake=FALSE
##排序的特性
xxx_ci(大小写不敏感)
xxx_cl（大小写敏感）
```

## Mysql的链接

```python
##mysql链接的安装,以及ORM框架,链接池
pip3 install PyMySQL
pip3 install sqlalchemy
pip3 install DBUtils
```

### 读取链接配置信息的样例

```python
[mysql]
host = server1
database = testdb
user = testuser
password = testpass

from configparser import ConfigParser


def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    if parser.has_section(section):
        items = parser.items(section)
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
    # print(items)
    return dict(items)

if __name__ == "__main__":
    print(read_db_config())
    
###使用    
import pymysql
from dbconfig import read_db_config

dbserver = read_db_config()
db = pymysql.connect(**dbserver)

try:

    # 使用 cursor() 方法创建一个游标对象 cursor
    with db.cursor() as cursor:
        sql = '''SELECT VERSION()'''
        # 使用 execute()  方法执行 SQL 查询 
        cursor.execute(sql)
        result = cursor.fetchone()
    db.commit()

except Exception as e:
    print(f"fetch error {e}")

finally: 
    # 关闭数据库连接
    db.close()

 
print (f"Database version : {result} ")

```

### 使用ORM框架链接

```python
# ORM方式连接 MySQL 数据库
# pip3 install sqlalchemy
#!/usr/bin/python3
 
import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# 打开数据库连接
# mysql> create database testdb;
# mysql> GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%' IDENTIFIED BY 'testpass';

Base = declarative_base()

class Book_table(Base): 
    __tablename__ = 'bookorm' 
    book_id = Column(Integer(), primary_key=True) 
    book_name = Column(String(50), index=True) 


# book_table=Table('book',metadata,
#     Column('id',Integer,primary_key=True),
#     Column('name',String(20)),
#     )

# 定义一个更多的列属性的类
# 规范写法要记得写在最上面
from datetime import datetime 
from sqlalchemy import DateTime

class Author_table(Base): 
    __tablename__ = 'authororm' 
    user_id = Column(Integer(), primary_key=True) 
    username = Column(String(15), nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now) 
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

# 实例一个引擎
dburl="mysql+pymysql://testuser:testpass@server1:3306/testdb?charset=utf8mb4"
engine=create_engine(dburl, echo=True, encoding="utf-8")

Base.metadata.create_all(engine)

```

### 使用链接池

```python
import pymysql
# pip3 install DBUtils
from dbutils.pooled_db import PooledDB
db_config = {
  "host": "server1",
  "port": 3306,
  "user": "testuser",
  "passwd": "testpass",
  "db": "testdb",
  "charset": "utf8mb4",
  "maxconnections":0,   # 连接池允许的最大连接数
  "mincached":4,        # 初始化时连接池中至少创建的空闲的链接,0表示不创建
  "maxcached":0,        # 连接池中最多闲置的链接,0不限制
  "maxusage" :5,        # 每个连接最多被重复使用的次数,None表示无限制
  "blocking":True       # 连接池中如果没有可用连接后是否阻塞等待
                        #  True 等待; False 不等待然后报错
}
 
spool = PooledDB(pymysql, **db_config) 

conn = spool.connection()
cur = conn.cursor()
SQL = "select * from bookorm;"
cur.execute(SQL)
f = cur.fetchall()
print(f)
cur.close()
conn.close()
```

