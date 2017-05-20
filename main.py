import os
import threading

def Sensor():
    global sensor_out
    sensor_out = None
    sensor_out = os.popen('python /home/pi/watchdog/main_bcm_17.py').readlines()
    sensor_out = str(sensor_out)
def Video():
    global video_out
    video_out = None
    video_out = os.popen('python3 /home/pi/watchdog/Face/camera.py').readlines()
    video_out = str(video_out)


if __name__ == "__main__":
    threads = []
    t1 = threading.Thread(target=Sensor)
    threads.append(t1)
    t2 = threading.Thread(target=Video)
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    while True:
        print(sensor_out)
        print(video_out)
        if sensor_out == 'Someone' and video_out == 'unknow':
            os.popen('python /home/pi/watchdog/main_beep.py')
        else:
            continue


