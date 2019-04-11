import requests
import re
import random
import io
import sys
import os
import json
import ssl
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from urllib import parse

ssl._create_default_https_context = ssl._create_unverified_context
class ShangHaizhuceyzm():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    def __init__(self):
        self.session=requests.session()
        self.mmname=str(int(random.random()*1000000000000))
    def yanzhengma(self,yhm,username,idcard,phone,bankcard):
        self.session.get("https://gr.tax.sh.gov.cn/portals/web/register",headers=self.headers,verify=False)
        res=self.session.get("https://gr.tax.sh.gov.cn/portals/web/thirdparty/authorize/dispatch/dyrz",headers=self.headers,verify=False)
        clientId=re.search("clientId : '(.*?)'",res.text).group(1)
        data={
            "clientId":clientId
        }
        res=self.session.post("http://oauth.iiap.sheca.com/web/app/info",data=data,headers=self.headers)
        res=self.session.get("http://oauth.iiap.sheca.com/web/auth/bankcard.jsp",headers=self.headers)
        data={
            'j_username':'{"type":7,"userName":"'+username+'","idNo":"'+idcard+'","dataSource":2,"mobile":"'+phone+'","bankNo":"'+bankcard+'"}}',
            'j_password':idcard
        }

        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "Referer": "http://oauth.iiap.sheca.com/web/auth/bankcard.jsp"
            }
        res=self.session.post("http://oauth.iiap.sheca.com/web/login.do",data=data,headers=headers,verify=False)
        if "上海多源认证平台OAuth回调中转服务" not in res.text:
            print("认证失败")
            return
        url=res.url.split("?")
        baseurl="http://gr.tax.sh.gov.cn/portals/web/thirdparty/authorize/notify/dyrz?"+url[1]
        res=self.session.get(baseurl,headers=self.headers)


        if username not in res.text:
            print("认证失败")
            return
        respubkey=re.search('data-param-rsapubkey="(.*?)"',res.text,re.S).group(1)
        data1={
            "dlm":yhm
        }
        res=self.session.post("http://gr.tax.sh.gov.cn/portals/web/validate/dlm",data=data1,headers=self.headers).json()

        if res["type"] != "SUCCESS":
            print("登陆名不可用,请重新填写登陆名")
            return
        data2={
            "smsType":"registerPhone"
        }
        self.session.post("http://gr.tax.sh.gov.cn/portals/web/sms/send/nosjhm",data=data2,headers=self.headers).json()
        item1 = {}
        item1["JSESSIONID"] = self.session.cookies.values()[0]
        item={}
        item["cookies"]=str(item1)
        item["respubkey"]=respubkey
        item["yhm"]=yhm
        item=json.dumps(item)
        print(item)



if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    yhm=sys.argv[1]
    yhm=parse.unquote(yhm)
    username=sys.argv[2]
    username=parse.unquote(username)
    idcard=sys.argv[3]
    phone=sys.argv[4]
    bankcard=sys.argv[5]
    shy=ShangHaizhuceyzm()
    # yhm="颓废的兔子"
    # username="贾浩"
    # idcard="131022198806100719"
    # phone="15600461100"
    # bankcard="6228481000884523118"


    shy.yanzhengma(yhm,username=username,idcard=idcard,phone=phone,bankcard=bankcard)



