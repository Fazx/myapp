import requests
import pytesseract
import re
import time
import os
import random
import json
import io
import sys
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from PIL import Image,ImageOps
class TianJingyzm():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }

    def __init__(self):
        self.session=requests.session()
        self.rname=str(int(random.random()*10000000000000))
        self.nowtime=str(int(time.time()*1000000))
    def yanzhengam(self):
        self.session.get("https://itswt.tjsat.gov.cn/portals/web/register",headers=self.headers,verify=False)
        res=self.session.get("https://itswt.tjsat.gov.cn/portals/web/register/unionpayRegist",headers=self.headers)
        data={
            "sfzjlxDm":"201"
        }
        self.session.post("https://itswt.tjsat.gov.cn/portals/web/base/code/getGjhdqDm",data=data,headers=self.headers).json()

    def getyzm(self,phone):
        data={
            "smsType":"registerPhone",
            "phoneNumber":phone
                    }
        res=self.session.post("https://itswt.tjsat.gov.cn/portals/web/sms/send",data=data,headers=self.headers,verify=False).json()
        # print(res)
        if res["type"] == "SUCCESS":
            item={}
            item["msg"]="验证码已发送"
            item["cookies"]=str(self.session.cookies.get_dict())
            item=json.dumps(item)
            print(item)
        else:
            print("验证码发送失败")


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    phone=sys.argv[1]
    # phone="15600461100"
    # password="a8050980200"
    # idcard="131022198806100719"
    # bankcard="6228481000884523118"
    tjz=TianJingyzm()
    tjz.yanzhengam()
    tjz.getyzm(phone=phone)
