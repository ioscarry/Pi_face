#-*- coding:utf-8 -*-
import os
import json
from subprocess import Popen,PIPE

api_key = "5fPPstekR568ai4fhPUPMUzpJJkeO0MV"
api_secret = "NNsNFXQ02sxo5Slwi4Jtro8WQw3-PncI"
path = '/home/pi/watchdog/Face/data/log'
outer_id = '1024'

def detect(image_file,return_landmark=0):
    '''
    检测照片中的人脸
    '''
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/detect" -F \
            "api_key={api_key}" -F \
            "api_secret={api_secret}" -F \
            "image_file=@{image_file}" -F \
            "return_landmark={return_landmark}" -F \
            "return_attributes=gender,age"'
            .format(api_key=api_key,api_secret=api_secret,image_file=image_file,return_landmark=return_landmark),shell=True,stdout=PIPE)
    wait = ""
    result=(result.stdout.read())
    with open("{path}/detect.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/detect.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/detect.json'.format(path=path))
    return result

#if __name__ == "__main__":
#    result = detect(image_file="/Face/Pitcure/me.jpg",return_landmark=1)
#    print(result)
def compare(face_token1,face_token2):
    '''
    compare two faces
    '''
    result = Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/compare" \-F "api_key=<api_key>" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}" \
            -F "face_token1={face_token1}" \
            -F "face_token2={face_token2}"'
            .format(api_key=api_key,api_secret=api_secret,face_token1=face_token1,face_token2=face_token2),shell=True,stdout=PIPE)
    wait = ""
    result=(result.stdout.read())
    with open("{path}/compare.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/compare.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/compare.json'.format(path=path))
    return result

def compareP(image_file,face_token):
    '''
    comapre image_file and face_token
    '''
    result = Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/compare" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}" \
            -F "image_file1=@{image_file}" \
            -F "face_token2={face_token}"'.
            format(api_key=api_key,api_secret=api_secret,image_file=image_file,face_token=face_token),shell=True,stdout=PIPE)
    wait = ""
    result=(result.stdout.read())
    with open("{path}/compareP.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/compareP.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/compareP.json'.format(path=path))
    return result

def search(face_token):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/search" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}" \
            -F "face_token1={face_token}" \
            -F "outer_id={outer_id}"'
            .format(api_key=api_key,api_secret=api_secret,face_token=face_token,outer_id=outer_id),shell=True,stdout=PIPE)
    wait = ""
    result=(result.stdout.read())
    with open("{path}/search.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/search.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/search.json'.format(path=path))
    return result


def searchP(image_file):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/search" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}" \
            -F "image_file=@{image_file}" \
            -F "outer_id={outer_id}"'
            .format(api_key=api_key,api_secret=api_secret,image_file=image_file,outer_id=outer_id),shell=True,stdout=PIPE)
    wait = ""
    result=(result.stdout.read())
    with open("{path}/searchP.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/searchP.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/searchP.json'.format(path=path))
    return result

def faceset_create(face_tokens):
    result = Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/create" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}" \
            -F "outer_id={outer_id}" \
            -F "face_tokens={face_tokens}"'
            .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id,face_tokens=face_tokens),shell=True,stdout=PIPE)
    wait = ""
    result=(result.stdout.read())
    with open("{path}/faceset_create.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/faceset_create.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/faceset_create.json'.format(path=path))
    return result

def faceset_remove(face_tokens):
    result = Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}" \
            -F "outer_id={outer_id}" \
            -F "face_tokens={face_tokens}"'
            .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id,face_tokens=face_tokens),shell=True,stdout=PIPE)
    wait = ""
    result=(result.stdout.read())
    with open("{path}/faceset_remove.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/faceset_remove.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/faceset_remove.json'.format(path=path))
    return result

def faceset_add(face_tokens):
    result = Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}" \
            -F "outer_id={outer_id}" \
            -F "face_tokens={face_tokens}"'
            .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id,face_tokens=face_tokens),shell=True,stdout=PIPE)
    wait = ""
    result=(result.stdout.read())
    with open("{path}/faceset_add.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/faceset_add.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/faceset_add.json'.format(path=path))
    return result

def faceset_getdetail():
    result = Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}" \
            -F "outer_id={outer_id}"'
            .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id),shell=True,stdout=PIPE)
    wait = ""
    result=(result.stdout.read())
    with open("{path}/facesetgetdetail.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/facesetgetdetail.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/facesetgetdetail.json'.format(path=path))
    return result


def facesetdelete(check_empty=1):
    global confidence
    result = Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/delete" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}" \
            -F "check_empty={check_empty}" \
            -F "outer_id={outer_id}"'
            .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id,check_empty=check_empty),shell=True,stdout=PIPE)
    result=(result.stdout.read())
    with open("{path}/facesetdelete.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/facesetdelete.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/facesetdelete.json'.format(path=path))
    return result

def facesetgetfacesets():
    global confidence
    result = Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/delete" \
            -F "api_key={api_key}" \
            -F "api_secret={api_secret}"'
            .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id,check_empty=check_empty),shell=True,stdout=PIPE)
    result=(result.stdout.read())
    with open("{path}/facesetgetfacesets.json".format(path=path),"wb+") as f:
        f.write(result)
    with open("{path}/facesetgetfacesets.json".format(path=path)) as f:
        result = json.load(f)
    os.remove('{path}/facesetgetfacesets.json'.format(path=path))
    return result
