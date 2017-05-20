#-*- coding:utf-8 -*-
import os
import sys
import json
import subprocess
import FaceApi
from DBconnect import *

outer_id = '1024'
conn,cur=connDB()

if not os.path.exists("/home/pi/watchdog/Face/Face_Project/data/log/face_import.log"):
    os.mknod("/home/pi/watchdog/Face/Face_Project/data/log/face_import.log")

def create_faceset():
    result = FaceApi.faceset_create('uter_id={}'.format(outer_id))
    sql = "select face_token from face_data ;"
    face_token_list=[]
    data = exeQuery(cur,sql)
    for i in data:
        for token in i:
            face_token_list.append(token)
    for i in face_token_list:
        print("*******************************************")
        with open('/home/pi/watchdog/Face/Face_Project/data/log/import.log','r') as f:
            f = f.read()
        if i in f:
            print("{}:-------Has Been Exist!".format(i))
        if i not in f:
            with open("/home/pi/watchdog/Face/Face_Project/data/log/import.log",'a') as f:
                f.write(i)
            result = FaceApi.faceset_add(face_tokens=i)


def create_table():
    sql = 'show tables;'
    try:
        data = exeQuery(cur,sql)
        table_list=[]
        for i in data:
            table_list.append(i)
        if 'face_data' not in table_list[0]:
            sql = 'create table face_data(`ID` varchar(12) NOT NULL default '',`name` varchar(12) NOT NULL default '',`face_token` varchar(32) NOT NULL default '',`gender` varchar(10) NOT NULL default '',`age` float) ENGINE=InnoDB DEFAULT CHARSET=utf-8;'
            exeQuery(cur,sql)
            sql = 'insert into face_data values(0,None,None,None,0);'
            exeQuery(cur,sql)
    except Exception:
        print("Mysql Error!")
        raise
    #finally:
     #   connClose(conn,cur)
def insert_data(ID,name,face_token,gender,age):
    sql = "insert into face_data values('%s','%s','%s','%s','%s');" % (ID,name,face_token,gender,age)
    print(sql)
    exeUpdate(conn,cur,sql)

def check_stuID(ID):
    stu_id_sql = "select ID from face_data;"
    data_id = exeQuery(cur,stu_id_sql)
    data_id_list = []
    for i in data_id:
        for data in i:
            data_id_list.append(data)

    try:
        if int(data_id_list[0]) == ID:
            print("{}:-------Has been Exist!".format(ID))
        elif int(data_id_list[0]) != ID:
            result = FaceApi.detect(image_file=imagedir)
            face_token=result["faces"][0]["face_token"]
            gender=result["faces"][0]["attributes"]["gender"]["value"]
            age=result["faces"][0]["attributes"]["age"]["value"]
            print("ID:{}".format(ID))
            print("Name:{}".format(name))
            print("face_token:{}".format(face_token))
            print("gender:{}".format(gender))
            print("age:{}".format(age))
            insert_data(ID,name,face_token,gender,age)
    except:
        pass

def get_ID_name(dir,topdown=True):
    global imagedir,ID,name
    filelist = []
    for root,dirs,files in os.walk(dir, topdown):
        for PicName in files:
            filelist.append(os.path.join(root,PicName))
        for f in sorted(filelist):
            imagedir = f
            print(imagedir)
            temp=imagedir.split('/')[8].split('.')
            print temp
            ID = temp[0]
            name = temp[1]
            print("***************************************")
            check_stuID(ID)
def main():
    os.remove("/home/pi/watchdog/Face/Face_Project/data/log/import.log")
    os.mknod("/home/pi/watchdog/Face/Face_Project/data/log/import.log")
    FaceApi.facesetdelete(check_empty=0)
    create_table()
    get_ID_name('/home/pi/watchdog/Face/Face_Project/data/image/')
    exeDelete(cur,100000000000)
    create_faceset()
    connClose(conn,cur)

if __name__ == "__main__":
    main()
    print("Done!")
