import socket
import os
import sys
import struct
import time
import threading
import datetime

import pymysql

def socket_service_image():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('172.22.8.155', 8042))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Wait for Connection.....................")
    db = pymysql.connect(host='localhost', port=3306, database='foo', password='12345678', user='root')
    cursor = db.cursor()

    while True:
        sock, addr = s.accept()  # addr是一个元组(ip,port)
        threading.Thread(target=lambda :deal_image(sock, addr, cursor, db)).start()

def deal_image(sock, addr, cursor, db):
    print("Accept connection from {0}".format(addr))  # 查看发送端的ip和端口
    buf = b''
    while buf == b'':
        buf = sock.recv(1024)  # 接收图片名
        # print(buf)
    fname = str(time.time()).split('.')[0]
    f = open('/Users/wanghanyu/PycharmProjects/WarehouseManagementSystem/image/{}.png'.format(fname), 'wb')
    sql = """SELECT max(id) from foo_alarm"""
    cursor.execute(sql)
    maxid = cursor.fetchall()[0][0]
    if maxid == None:
         maxid = 0

    sql = """insert into foo_alarm(id, alarmCode, deviceCode, deviceName, alarmDate, alarmType, processDate, processState, imgPath) values ({}, "{}", "{}", "{}", "{}", {}, {}, {}, "{}")""".format(maxid+1, fname, addr[0], "仓库"+addr[0], datetime.datetime.now(), 1, 'NULL', 0, 'image/{}.png'.format(fname))
    cursor.execute(sql)
    db.commit()

    while buf:
        f.write(buf)
        buf = sock.recv(1024)
    f.close()

    sock.close()