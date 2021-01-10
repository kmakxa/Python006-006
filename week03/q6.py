# ORM方式连接 MySQL 数据库
# pip3 install sqlalchemy
#!/usr/bin/python3

from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy import create_engine, Table, Float, Column, Integer, String, MetaData, ForeignKey,DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

Base = declarative_base()

class user_table(Base):
    __tablename__ = 'user_table'
    id = Column(Integer(), primary_key=True)
    user_name = Column(String(50), index=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now,
                        onupdate=datetime.now)

class user_asset(Base):
    __tablename__ = 'user_asset'
    id = Column(Integer(), primary_key=True)
    balance = Column(DECIMAL())

class audit(Base):
    __tablename__ = 'audit'
    id = Column(Integer(), primary_key=True)
    from_user_id = Column(Integer(), primary_key=True)
    to_user_id = Column(Integer(), primary_key=True)
    amt = Column(DECIMAL())
    created_on = Column(DateTime(), default=datetime.now)

# 实例一个引擎
dburl = "mysql+pymysql://python_test:JustForTest#06@39.96.60.116:3306/testdb?charset=utf8mb4"
engine = create_engine(dburl, echo=True, encoding="utf-8")
##建表
# Base.metadata.create_all(engine)
##写入
db = pymysql.Connect(host="39.96.60.116",user="python_test",passwd="JustForTest#06",db="testdb",port=3306)
 
try:

    # %s是占位符
    with db.cursor() as cursor:
        sql = 'select count(1) from user_asset where user_name = %s and balance > 100 '
        value = ('张三')
        sql1 = 'INSERT INTO audit (from_user_id,to_user_id,amt,created_on) VALUES (%s, %s, %s, %s)'
        value1 = ('%s','%s',100, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        sql2 = 'update user_asset set balace = balance -100 where user_id = $s'
        value2 = ('player2', 7,'2020-01-15','男','中学',datetime.now().strftime("%Y-%m-%d %H:%M:%S"),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        value3 = ('player3', 9,'2020-01-16','男','中学',datetime.now().strftime("%Y-%m-%d %H:%M:%S"),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(sql1, value1)
        cursor.execute(sql, value2)
        cursor.execute(sql, value3)

except Exception as e:
    print(f"insert error {e}")
    db.rollback()
else:
    db.commit()
finally: 
    # 关闭数据库连接
    db.close()
    print(cursor.rowcount)

