# ORM方式连接 MySQL 数据库
# pip3 install sqlalchemy
#!/usr/bin/python3

from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy import create_engine, Table, Float, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

Base = declarative_base()

class player_table(Base):
    __tablename__ = 'player'
    player_id = Column(Integer(), primary_key=True)
    player_name = Column(String(50), index=True)
    age = Column(Integer(), index=True)
    birth = Column(String(10), index=True)
    sex = Column(String(50), index=True)
    edu = Column(String(50), index=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now,
                        onupdate=datetime.now)


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
        sql = 'INSERT INTO player (player_name,age,birth,sex,edu,created_on,updated_on) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        value1 = ('player1', 5,'2020-01-14','男','中学',datetime.now().strftime("%Y-%m-%d %H:%M:%S"),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        value2 = ('player2', 7,'2020-01-15','男','中学',datetime.now().strftime("%Y-%m-%d %H:%M:%S"),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        value3 = ('player3', 9,'2020-01-16','男','中学',datetime.now().strftime("%Y-%m-%d %H:%M:%S"),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(sql, value1)
        cursor.execute(sql, value2)
        cursor.execute(sql, value3)
        sql = '''SELECT * FROM player'''
        cursor.execute(sql)
        players = cursor.fetchall() # fetchone()
        for player in players: 
            print(player)
    db.commit()
    ##读取

except Exception as e:
    print(f"insert error {e}")

finally: 
    # 关闭数据库连接
    db.close()
    print(cursor.rowcount)

