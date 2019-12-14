import hashlib
import time

import pymysql
import redis
from mysnakegame import SnakeGame

flag = [False]

def connect_mysql():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="123",
        db="snake",
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn, cursor

def connect_redis():
    rconn = redis.Redis(
        host="127.0.0.1",
        port="6379",
        db=1,
        decode_responses=True
    )
    return rconn

def encry_pwd(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    password = m.hexdigest()
    return password

def func():
    func_cho = """
        1：注册    2：登陆    3：玩耍  
        4：排行    5：退出
    """
    func_map = {
        "1" : register,
        "2" : login,
        "3" : play,
        "4" : rank,
    }
    while True:
        print(func_cho)
        cho = input("请输入选项：")
        if cho == "1":
            register()
        elif cho == "2":
            login()
        elif cho == "3":
            play()
        elif cho == "4":
            rank()
        elif cho == "5":
            break

def register():
    username = input("请输入用户名：")
    password = input("请输入用户密码：")
    if username and password:
        conn, cursor = connect_mysql()
        sql = "select name from userinfo where name=%s"
        cursor.execute(sql, (username,))
        user = cursor.fetchone()
        if user:
            print("该用户已存在")
            return
        sql = "insert into userinfo(name, password) values(%s, %s)"
        password = encry_pwd(password)
        cursor.execute(sql, (username, password))
        conn.commit()
        print("注册成功")
        return

def login():
    username = input("请输入用户名：")
    password = input("请输入用户密码：")
    if username and password:
        rconn = connect_redis()
        password = encry_pwd(password)
        try:
            if rconn.hmget(username, "password") == password:
                print("登陆成功")
                flag[0] = username
                return True
        except:
            pass
        conn, cursor = connect_mysql()
        sql = "select name, rank from userinfo where name=%s"
        cursor.execute(sql, (username,))
        query = cursor.fetchone()
        if not query:
            print("该用户不存在")
            return
        print("登陆成功")
        rconn.hmset(username, dict(query))
        flag[0] = username
        return True

def deco(auth):
    def wrapper(*args, **kwargs):
        if flag[0]:
            auth()
            return
        print("请先登陆")
    return wrapper

@deco
def play():
    ctime = time.time()
    sg = SnakeGame()
    sg.play()
    ntime = time.time()
    rank_score = int(ntime - ctime)
    conn, cursor = connect_mysql()
    sql = "update userinfo set rank=%s where name=%s"
    cursor.execute(sql, (rank_score, flag[0]))
    conn.commit()
    return

@deco
def rank():
    rconn = connect_redis()
    try:
        rank = rconn.hmget(flag[0], "rank")
    except:
        pass
    if rank:
        print(flag[0], rank)
        return

    conn, cursor = connect_mysql()
    sql = "select name, rank from userinfo where name=%s"
    cursor.execute(sql, (flag[0],))
    query = cursor.fetchone()
    print(query)
    return

if __name__ == '__main__':
    func()
