#-*- coding:utf-8 -*-
import pymysql

def connDB():
    global conn,cur
    conn=pymysql.connect(host='localhost',user='root',passwd='cujam137',db='face',charset="utf8")
    cur=conn.cursor()
    return(conn,cur)

def exeUpdate(conn,cur,sql):
    sta = cur.execute(sql)
    conn.commit()
    return(sta)

def exeDelete(cur,ID):
    sta=cur.execute('delete from face_data where Id = %d'%int(ID))
    conn.commit()
    return(sta)

def exeQuery(cur,sql):
    cur.execute(sql)
    return(cur)

def connClose(conn,cur):
    cur.close()
    conn.close()
