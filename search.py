import cv2
import os
import sys
import shutil
import time
import FaceApi
from DBconnect import *
from PIL import Image,ImageDraw,ImageFont

conn,cur = connDB()

if not os.path.exists("/Face/data/log/search.log"):
    os.mknod("/Face/data/log/search.log")

def filelist(dir,topdown=True):
    fileList=[]
    for root, dirs, files in os.walk(dir, topdown):
        for PicName in files:
            fileList.append(os.path.join(root,PicName))
        return fileList

def get_detail():
    sql = "select * from face_data where face_token='%s' "%face_token
    data = exeQuery(cur,sql)
    data_list = []
    for i in data:
        for a in i:
            data_list.append(a)
    stuID,stuname,gender = data_list[0],data_list[1],data_list[3]
    detail=[stuID,stuname]
    print("Stuid:{}".format(stuID))
    print("StuName:{}".format(stuname))
    print("gender:{}".format(gender))
    return detail

def detect(filename):
    global face_token
    count=0
    faces=[]
    face_cascade = cv2.CascadeClassifier("/Face/data/cascades/haarcascade_frontalface_alt.xml")
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #ft = cv2.freetype.createFreeType2()
    #ft.loadFontData(fontFileName='/Face/data/font/hua.ttf',id =0)

    for(x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),3)
        f = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
        cv2.imwrite('/Face/data/search/{}/{}.pgm'.format(filesdir,count), f)
        result=FaceApi.searchP(image_file='/Face/data/search/{}/{}.pgm'.format(filesdir,count))
        if len(result) == 4:
            break
        if result["results"][0]["confidence"] >= 80.00:
            print(result["results"][0]["confidence"])
            face_token=result["results"][0]["face_token"]
            print("face_token:{}".format(face_token))
            detail=get_detail()
            font = ImageFont.truetype('/Face/data/font/hua.ttf',20)
            im = Image.open(filename)
            draw = ImageDraw.Draw(im)
            print(detail[1])
            draw.text((x,y-10),detail[1], fill=(0,0,0),font=font)
            file_name = filename.split('/')[4].split('.')[0]
            im.save('/Face/data/out/' + file_name + 'jpg','JPEG')

            #ft.putText(img=img,text='tump',org=(x,y-10), fontHeight=30,line_type=cv2.LINE_AA, color=(0,255,165),thickness=1, bottomLeftOrigin=True)
            #cv2.putText(img,"特朗普", (x,y-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1 ,(0,0,255),2)
        else:
            print("Unkonw face")
            cv2.putText(img,"Unknow", (x,y-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1 ,(0,0,255),2)
        count+=1
        cv2.imwrite(i,img)

def main():
    global i,filesdir
    fileList = filelist('/Face/data/search')
    with open('/Face/data/log/search.log', 'r') as f:
        content=f.read()
    for i in fileList:
        if i in content:
            filesdir = i.split('/')[3]
            print("{}:----------Has Been exist!".format(filesdir))
        if i not in content:
            filesdir1=i.split('/')[3]
            filesdir=i.split('/')[3].split('.')[0]
            if not os.path.exists('/Face/data/search/{}'.format(filesdir)):
                os.makedirs('/Face/data/search/{}/'.format(filesdir))
                shutil.copyfile('/Face/data/search/{}'.format(filesdir1),'/Face/data/search/{}/{}'.format(filesdir,filesdir1))
            detect(i)
            with open("/Face/data/log/search.log",'a') as f:
                f.write(i)
if __name__ == "__main__":
    main()
    print("Done")
