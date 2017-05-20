#-*- coding:utf-8 -*-
#################################################
import cv2
import time
import datetime
import shutil
import FaceApi
from DBconnect import *
from PIL import Image,ImageDraw,ImageFont
#################################################

conn,cur = connDB()
model_path = '/Face/data/cascades/haarcascade_frontalface_alt.xml'


def get_detail(face_token):
    '''
    识别人脸
    '''
    sql = "select * from face_data where face_token = '%s';" % face_token
    data = exeQuery(cur,sql)
    data_list = []
    for i in data:
        for a in i:
            data_list.append(a)
    stuID,stuname,gender=data_list[0],data_list[1],data_list[3]
    detail=[stuID,stuname]
    #print(stuID)
    #print(stuname)
    return detail

def Searchface(image,count):
    fps = 0
    #创建classifier
    clf = cv2.CascadeClassifier(model_path)
    #设定灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #识别面部
    faces = clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
            )
    for(x,y,w,h) in faces:
        img = cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255 ,0),2)
        if count%5 < 2:
            f = cv2.resize(gray[y:y+h,x:x+w],(200,200))
            cv2.imwrite('/Face/data/temp/temp.pgm',f)
            result = FaceApi.searchP(image_file='/Face/data/temp/temp.pgm')
            if(len(result)) == 4:
                break
            try:
                if result["results"][0]["confidence"] >= 80.00:
     #               print(result["results"][0]["confidence"])
                    face_token = result["results"][0]["face_token"]
                    detail = get_detail(face_token)
                    #print(detail)
                    cv2.putText(img,face_token, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                    r = str(detail[1])
                    return r
                else:
                    #print("Unknown Face")
                    cv2.putText(img,"Unknow", (x, y-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 ,(0,0,255), 2)
                    nowtime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
                    cv2.imwrite("/home/pi/watchdog/Face/data/unknow/" + nowtime + '.jpg',img)
                    r = "Unknow"
                    return r
            except:
     #           print("[E] ERROE! Trying...")
                continue
            fps += 1
            sfps = fps/(time.time() - t_start)
            cv2.putText(img, "FPS: " + str(int(sfps)), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
     #   print(count)
    #return image
def video():
    a = 0
    global t_start
    cap = cv2.VideoCapture(0)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc ,20.0 , (width, height))
    count = 0
    while(cap.isOpened and a <= 100):

        ret, frame = cap.read()
        if ret == True:
            t_start = time.time()
            frame=Searchface(frame, count)
            return(frame)
            count += 1
     #       out.write(frame)
            #cv2.imshow('My Camera', frame)
            #if(cv2.waitKey(1) & 0xFF) == ord('q'):
            #    break
        else:
            break
        a += 1
        if a == 100:
            break
    out.release()
    cap.release()
    #cv2.destroyAllWindows()
def main():
    while True:
        video()

if __name__ == '__main__':
    main()









