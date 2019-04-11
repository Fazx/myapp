import requests
import re
import random
import os
import sys
import io
import json
import ssl
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from urllib import parse
#import logging
#logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename="/home/wwwlogs/python/zhucelog.txt")
#logger = logging.getLogger(__name__)
ssl._create_default_https_context = ssl._create_unverified_context
class ShangHaizhuce():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    def __init__(self):
        self.session=requests.session()
        self.mmname=str(int(random.random()*1000000000000))



    def zhuce(self,yhm,password,code,respubkey,cookies):
        if cookies=="0":
            print("请获取短信验证码")
            return
        res=str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}

        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)

        with open(self.mmname+'.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(respubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open(self.mmname+'.txt', "r") as f:
            public_key = f.read()
            f.close()
        os.remove(self.mmname+'.txt')
        bpassword = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(bpassword))
        mm = cipher_text.decode("utf-8")
        data={
            "dlm":yhm
        }
        res=self.session.post("https://gr.tax.sh.gov.cn/portals/web/validate/dlm",data=data,headers=self.headers,verify=False).json()

        if res["type"]!= "SUCCESS":
            print("用户名已存在,请重新输入用户名")
            return

        header={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",

            "Content-Type": "application/json;charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",

        }
        data3={"dlm":yhm,"mm":mm,"qrmm":password,"needSjhm":"","sjyzm":code,"st":""}
        data3=json.dumps(data3)
        res=self.session.post("https://gr.tax.sh.gov.cn/portals/web/register/registerUser",data=data3,headers=header,verify=False)
        #logging.info(res.text)
        if "短信验证码错误" in res.text:
            print("短信验证码错误")
            return
        if "系统维护中" in res.text:
            print("注册失败")
            return
        if "该身份信息已被注册" in res.text:
            print("该身份信息已被注册")
            return
        if yhm in res.text:
            print("注册成功")
            return
        print("网络错误请重新注册")
        #{"type":"ERROR","code":null,"content":"短信验证码错误，请重新输入","cause":null,"contentList":null,"data":null}


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
   # print(sys.argv)
    yhm=sys.argv[1]
    yhm=parse.unquote(yhm)
    password=sys.argv[2]
    code=sys.argv[3]
    respubkey=sys.argv[4]
    cookies=sys.argv[5]
    shy=ShangHaizhuce()
    try:
        shy.zhuce(yhm=yhm, password=password, code=code, respubkey=respubkey,cookies=cookies)
    except Exception as e:
        #logging.info(e)
        print("系统维护中")

