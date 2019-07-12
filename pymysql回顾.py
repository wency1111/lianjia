import pymysql
db=pymysql.connect(host='localhost',
                   user='root',
                   port=3306,
                   password='123456',
                   charset="utf8")
cursor=db.cursor()
cursor.execute("create database if not EXISTS testspider;")
cursor.execute("use testspider;")
cursor.execute("create table if not EXISTS t1(id int);")
cursor.execute("insert into t1 VALUES (1);")

db.commit()
cursor.close()
db.close()