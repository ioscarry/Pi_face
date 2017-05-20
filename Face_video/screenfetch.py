#-*- coding:utf-8 -*-
import cv2
def ScreenFetch():
    c = cv2.VideoCapture(0)
    img = c.read()
    result = cv2.imwrite("/home/pi/watchdog/Face/Face_Project/data/screenfetch/screenfetch.jpg",img[1])
    return result
