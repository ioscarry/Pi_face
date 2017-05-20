from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS
from camera import video
import importFace
import ConfigParser
import socket
import fcntl
import struct
import threading
import time,datetime,commands,os,sys
import RPi.GPIO as GPIO


SAKS = SAKSHAT()

BCM27 = 27
__human_body = 0
__light_status = False
__press = 0
__switch_press = 1
__shutdown_reboot = 0
_count = 10
GPIO.setup(BCM27,GPIO.IN)


def get_ip_address(ifname = 'eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])
def init():
    SAKS.digital_display.show("8.8.8.8.")
    SAKS.ledrow.on()
    time.sleep(1)
    SAKS.ledrow.off()
    time.sleep(1)
    SAKS.digital_display.show("####")
    time.sleep(1)
    SAKS.ledrow.set_row([False,False,True,True,False,False,False,False])


def get_cpu_temp():
    global cpu_temp
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp) / 1000
def get_gpu_temp():
    global gpu_temp
    gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp'  ).replace( 'temp=', ''  ).replace( '\'C', ''  )
    return float(gpu_temp)
def get_time():
        t = time.localtime()
        h = t.tm_hour
        m = t.tm_min
        s = t.tm_sec
        SAKS.digital_display.show(("%02d.%02d") % (h , m))
        time.sleep(1)
        SAKS.digital_display.show(("%02d%02d") % (h , m))
        time.sleep(1)

def dip_switch_status_changed_handler(status):
    global __switch_press
    if status[0]:
        __switch_press = 1
    else :
        __switch_press = 2

def tact_event_handler(pin, status):
    global __light_status
    global __press
    global __human_body
    global __shutdown_reboot
    global _count
    if pin == PINS.TACT_RIGHT and status == True and __switch_press == 1:
        if not __light_status:
            __press += 1
            if __press > 2:
                __press = 0
        __light_status = not __light_status
    if pin == PINS.TACT_LEFT and status == True and __switch_press == 1:
        if not __light_status:
            __human_body =+ 1
            if __human_body > 2:
                __human_body = 0
        __light_status = not __light_status
    if pin == PINS.TACT_RIGHT and status == True and __switch_press == 2:
        if not __light_status:
            __shutdown_reboot += 1
            if __shutdown_reboot > 2:
                __shutdown_reboot = 1
        __light_status = not __light_status
    if pin == PINS.TACT_LEFT and status == True and __switch_press == 2:
        if not __light_status:
            __shutdown_reboot = 3
        __light_status = not __light_status


def restart():
    SAKS.digital_display.show("####")
    SAKS.ledrow.set_row([0,0,0,0,0,0,0,0])


if __name__ == "__main__":
    try:
        init()
        importFace.main()
        while True:
            cp = ConfigParser.SafeConfigParser()
            cp.read('/home/pi/watchdog/Face/Face_Project/data/face.conf')
            c = get_cpu_temp()
            g = get_gpu_temp()
            time_switch = int(cp.get('settings','time'))
            temp_switch = int(cp.get('settings','temp'))
            red = int(cp.get('settings','red'))
            ONF = int(cp.get('settings','ONF'))
            temp = SAKS.ds18b20.temperature
            SAKS.dip_switch_status_changed_handler = dip_switch_status_changed_handler
            SAKS.tact_event_handler = tact_event_handler
            human = GPIO.input(BCM27)
            print(human)
            if red == 1:
                SAKS.buzzer.beepAction(0.02,0.02,30)
            if ONF == 1:
                if human == 0:
                    #SAKS.buzzer.beepAction(0.02,0.02,30)
                    SAKS.ledrow.set_row([None,None,None,None,True,True,None,None])
                    t = threading.Thread(target=video)
                    t.setDaemon(True)
                    t.start()
                    t.join()
            elif ONF == 0:
                SAKS.ledrow.set_row([None,None,None,None,False,False,None,None])

            if __switch_press == 1:
                SAKS.ledrow.set_row([False,True,None,None,None,None,None,None])
                if __press == 0 and time_switch == 1:
                    get_time()
                elif __press == 1 or temp_switch == 1:
                    SAKS.digital_display.show(("%d.%d.") % (c, g) )
                    if c > 53 or g > 53:
                        SAKS.buzzer.beepAction(0.02,0.02,30)
                elif __press == 2:
                    if temp == -128.0:
                        #time.sleep(10)
                        continue
                    SAKS.digital_display.show(("%5.1f" % temp).replace(' ','#'))
            elif __switch_press == 2:
                SAKS.ledrow.set_row([True,False,None,None,None,None,None,None])
                if __shutdown_reboot == 1 and _count == 0:
                    SAKS.digital_display.show("####")
                    SAKS.ledrow.set_row([0,0,0,0,0,0,0,0])
                    os.system("shutdown now")
                    sys.exit()
                elif __shutdown_reboot == 2 and _count == 0 :
                    SAKS.digital_display.show("####")
                    SAKS.ledrow.set_row([0,0,0,0,0,0,0,0])
                    os.system("reboot now")
                    sys.exit()
                elif __shutdown_reboot == 1 or __shutdown_reboot == 2:
                    if __shutdown_reboot == 1:
                        SAKS.ledrow.set_row([None,None,False,False,True,False,False,False])
                    elif __shutdown_reboot == 2:
                        SAKS.ledrow.set_row([None,None,False,False,True,True,False,False])
                    _count -= 1
                    SAKS.digital_display.show(("###%d") % (_count))
                    time.sleep(1)


                elif __shutdown_reboot == 3:
                    _count = 10
                    SAKS.digital_display.show("##10")
                    SAKS.ledrow.set_row([None,None,True,True,False,False,False,False])
    except:
        raise
        time.sleep(1)
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
