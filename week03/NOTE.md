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

读取链接配置信息的样例

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

```

