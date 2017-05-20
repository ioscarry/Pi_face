#-*- coding:utf-8 -*-
#######################################################################
import sys,commands,os
import threading
import socket
import random
import ConfigParser
import importFace
from camdlib import *
reload(sys)
sys.setdefaultencoding('utf8')
from Face_video.screenfetch import ScreenFetch
import new_botton
import time,datetime
from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS
import RPi.GPIO as GPIO
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage, ShortVideoMessage)
######################################################################
conf = WechatConf(
   token='weixin',
   appid='wx2754bc14e0d446b8',
   appsecret='7fd629600a5dd033d502c866b22e0edd',
   encrypt_mode='normal'
   #encoding_aes_key=''
)
#####################################################################
os.environ['TZ'] =  'Asia/Shanghai'
global confPath
confPath = '/home/pi/watchdog/Face/Face_Project/data/face.conf'
global IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('10.255.255.255', 0))
IP = s.getsockname()[0]

global SAKS
SAKS = SAKSHAT()

##################################################################
####################################################################
@csrf_exempt
def wechat_home(request):
    global confPath
    cp = ConfigParser.SafeConfigParser()
    #读取配置文件
    cp.read('/home/pi/watchdog/Face/Face_Project/data/face.conf')
    time_switch = int(cp.get('settings','time'))
    temp_switch = int(cp.get('settings','temp'))
    ONF = int(cp.get('settings','onf'))
    Face = int(cp.get('settings','face'))
    sheel = int(cp.get('settings','sheel'))
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    global wechat_instance
    wechat_instance = WechatBasic(conf=conf)
    if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponseBadRequest('Verify Failed')
    else:
        if request.method == 'GET':
            response = request.GET.get('echostr', 'error')
        else:
            try:
                wechat_instance.parse_data(request.body)
                message = wechat_instance.get_message()
                #自定义菜单
                menu = {
                        'button':[
                            {
                                'name':'PI',
                                'sub_button':[
                                    {
                                        'type':'click',
                                        'name':'时间',
                                        'key':'PI_TIME'
                                        },
                                    {
                                        'type':'click',
                                        'name':'温度',
                                        'key':'PI_TEMP'
                                        },
                                    {
                                        'type':'click',
                                        'name':'关闭警报',
                                        'key':'RED'
                                        },
                                    {
                                        'type':'click',
                                        'name':'帮助',
                                        'key':'PI_HELP'
                                        },
                                    {
                                        'type':'view',
                                        'name':'Github',
                                        'url':'http://github.com'
                                        }
                                    ]
                                },
                            {
                                'name':'Face',
                                'sub_button':[
                                    {
                                        'type':'click',
                                        'name':'导入人脸',
                                        'key':'Face_import'
                                        },
                                    {
                                        'type':'click',
                                        'name':'添加信息',
                                        'key':'Face_data'
                                        },
                                    {
                                        'type':'click',
                                        'name':'显示细节',
                                        'key':'Face_small'
                                        },
                                    {
                                        'type':'click',
                                        'name':'拍照',
                                        'key':'Face_camera'
                                        }
                                    ]
                                },
                            {
                                'name':'settings',
                                'sub_button':[
                                    {
                                        'type':'click',
                                        'name':'开关',
                                        'key':'OFF'
                                        },
                                    {
                                        'type':'click',
                                        'name':'严格模式',
                                        'key':'SSS'
                                        },
                                    {
                                        'type':'click',
                                        'name':'普通模式',
                                        'key':'S'
                                        },
                                    {
                                        'type':'click',
                                        'name':'查看日志',
                                        'key':'LOG'
                                        },
                                    {
                                        'type':'click',
                                        'name':'开启sheel',
                                        'key':'Sheel'
                                        }
                                    ]
                                }
                            ]
                        }
                wechat_instance.create_menu(menu)
                if isinstance(message, TextMessage):
                    countent = message.content.strip()
                    if countent == '全灭':
                        new_botton.restart()
                        reply_text = 'OK'
                    elif countent == 'ip' or countent == 'IP':
                        reply_text = IP
                    elif countent == 'test':
                        img = open('/home/pi/watchdog/Face/Face_Project/data/unknow/q.jpg')
                        data = wechat_instance.upload_media('image',img , 'jpg')
                        img.close()
                        img_id = data['media_id']
                    elif 'name:' in countent:
                        name = countent.split(':')
                        name = name[1]
                        data = open('/home/pi/watchdog/Face/Face_Project/data/face_data.log','w')
                        data.write(name)
                        data.close()
                        reply_text = '信息导入成功'
                    else:
                        if sheel == 1:
                            if countent == 'vim' or 'rm' in countent:
                                reply_text == '警告！，禁止执行！'
                            else:
                                (status, output) = commands.getstatusoutput('{cmd}'.format(cmd=countent))
                                reply_text = output
                        else:
                            reply_text = countent

                elif isinstance(message, VoiceMessage):
                    reply_text = 'voice'
                elif isinstance(message, ImageMessage):
                    picurl = message.picurl
                    media_id = message.media_id

                    if Face == 0:
                        f = open('/home/pi/watchdog/Face/Face_Project/data/face_data.log')
                        result = f.readlines()
                        f.close()
                        if result == []:
                            reply_text = '还没有导入人脸信息'
                        else:
                            response = wechat_instance.download_media(media_id)
                            ra = random.randint(2,99)
                            if ra % 100 < 10:
                                img_path = '/home/pi/watchdog/Face/Face_Project/data/image/' + '10000000000' + str(ra) + '.' + str(result[0]) + '.' + 'jpg'
                            elif ra % 100 > 10:
                                img_path = '/home/pi/watchdog/Face/Face_Project/data/image/' + '1000000000' + str(ra) + '.' + str(result[0]) + '.' + 'jpg'
                            with open(img_path, 'wb')as fd:
                                for chunk in response.iter_content(1024):
                                    fd.write(chunk)
                            os.remove('/home/pi/watchdog/Face/Face_Project/data/face_data.log')
                            os.mknod('/home/pi/watchdog/Face/Face_Project/data/face_data.log')
                            importFace.main()
                            reply_text = '导入成功'

                    elif Face == 1:
                        response = wechat_instance.download_media(media_id)
                        img_path = '/home/pi/watchdog/Face/Face_Project/data/details/img.jpg'
                        with open(img_path, 'wb')as fd:
                            for chunk in response.iter_content(1024):
                                fd.write(chunk)
                        pi_face_landmark(img_path)
                        img = open(img_path)
                        data = wechat_instance.upload_media('image',img , 'jpg')
                        img.close()
                        media_id = data['media_id']
                        user_id = 'opL4ZwSzQPdCcefPKYo_LR0ImjhI'
                        wechat_instance.send_image_message(user_id, media_id)


                elif isinstance(message, LinkMessage):
                    reply_text = 'link'
                elif isinstance(message, LocationMessage):
                    reply_text = 'location'
                elif isinstance(message, VideoMessage):
                    reply_text = 'video'
                elif isinstance(message, ShortVideoMessage):
                    reply_text = 'shortvideo'
                elif isinstance(message, EventMessage):
                    if message.type == 'click':
                        if message.key == 'PI_TIME':
                            localtime = time.asctime(time.localtime(time.time()))
                            reply_text = '时间:' + str(localtime)
                            cp.set('settings','time','1')
                            cp.set('settings','temp','0')
                            fh = open(confPath,'w')
                            cp.write(fh)
                            fh.close()
                        elif message.key == 'RED':
                            SAKS.ledrow.set_row([None,None,None,None,None,None,False,False])
                            cp.set('settings','red','0')
                            fh = open(confPath,'w')
                            cp.write(fh)
                            fh.close()
                        elif message.key == 'PI_TEMP':
                            cpu_temp = new_botton.get_cpu_temp()
                            gpu_temp = new_botton.get_gpu_temp()
                            t = SAKS.ds18b20.temperature
                            if str(t) == '-128.0':
                                reply_text = 'cpu温度:' + str(cpu_temp) + '\n' + \
                                        'gpu温度:' + str(gpu_temp) + '\n' + \
                                        '室温:' + '获取失败，请稍后再试'
                            else:
                                reply_text = 'cpu温度:' + str(cpu_temp) + '\n' + \
                                        'gpu温度:' + str(gpu_temp) + '\n' + \
                                        '室温:' + str(t)

                            cp.set('settings','temp','1')
                            cp.set('settings','time','0')
                            fh = open(confPath,'w')
                            cp.write(fh)
                            fh.close()
                        elif message.key == 'Face_camera':
                            result = ScreenFetch()
                            if result == True:
                                screen_img = open('/home/pi/watchdog/Face/Face_Project/data/screenfetch/screenfetch.jpg')
                                data = wechat_instance.upload_media('image',screen_img,'jpg')
                                screen_img.close()
                                img_id = data['media_id']
                            else:
                                reply_text = '拍照失败'
                        elif message.key == 'Face_import':
                            cp.set('settings','face','0')
                            fh = open(confPath,'w')
                            cp.write(fh)
                            fh.close()
                            reply_text = '已设置导入人脸模式'
                        elif message.key == 'Face_data':
                            reply_text = '请输入名称:(格式如name:test)'
                        elif message.key == 'Face_small':
                            reply_text = '已设置显示人脸细节'
                            cp.set('settings','face','1')
                            fh = open(confPath,'w')
                            cp.write(fh)
                            fh.close()
                        elif message.key == 'S':
                            reply_text = '普通模式已开启'
                            cp.set('settings','mode','normal')
                            fh = open(confPath,'w')
                            cp.write(fh)
                            fh.close()
                        elif message.key == 'SSS':
                            reply_text = '严格模式已开启'
                            cp.set('settings','mode','strict')
                            fh = open(confPath,'w')
                            cp.write(fh)
                            fh.close()
                        elif message.key == 'OFF':
                            if ONF == 1:
                                reply_text = '正在关闭'
                                cp.set('settings','ONF','0')
                                fh = open(confPath,'w')
                                cp.write(fh)
                                fh.close()
                            elif ONF == 0:
                                reply_text = '正在开启'
                                cp.set('settings','ONF','1')
                                fh = open(confPath,'w')
                                cp.write(fh)
                                fh.close()
                        elif message.key == 'LOG':
                            log = open('/home/pi/watchdog/Face/Face_Project/data/log/out.log')
                            txt = log.readlines()
                            log.close()
                            reply_text = txt
                        elif message.key == 'Sheel':
                            if sheel == 1:
                                reply_text = '已关闭sheel'
                                cp.set('settings','sheel','0')
                                s = open(confPath,'w')
                                cp.write(s)
                                s.close()
                            if sheel == 0:
                                reply_text = '已开启sheel'
                                cp.set('settings','sheel','1')
                                s = open(confPath,'w')
                                cp.write(s)
                                s.close()


                else:
                    reply_text = 'other'
                try:
                    response = wechat_instance.response_text(content=reply_text)
                except UnboundLocalError:
                    pass
                try:
                    response = wechat_instance.response_image(img_id)
                except UnboundLocalError:
                    pass
            except ParseError:
                return HttpResponseBadRequest('Invalid XML Data')
        return HttpResponse(response, content_type="application/xml")
