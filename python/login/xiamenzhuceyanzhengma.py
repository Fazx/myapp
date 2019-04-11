import requests
import random
import re
import os
import io
import sys
import base64
import json
import pytesseract
from PIL import Image,ImageOps
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

class XiaMenzhuce():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    def __init__(self):
        self.session=requests.session()
        self.rname=str(int(random.random()*10000000000000))
        self.rtime=str(random.random())
    def getindex(self):
        self.session.get("https://zrr.xm-l-tax.gov.cn/portals/web/register",headers=self.headers,verify=False)
        self.session.get("https://zrr.xm-l-tax.gov.cn/portals/web/register/unionpayRegist",headers=self.headers)


    def getphoneyanzhengam(self,phone):

        data={
            "smsType":"registerPhone",
            "phoneNumber":phone
                    }

        res=self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/sms/send",data=data,headers=self.headers,verify=False).json()
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

    xmz=XiaMenzhuce()
    xmz.getindex()
    xmz.getphoneyanzhengam(phone=phone)







    #
    # xmz.zhuce(name=name,idcard=idcard,bankcard=bankcard,phone=phone,phonecode=phonecode,imagecode=imagecode,password=password)