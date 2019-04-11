import requests
import time
import re
import sys
import io
import base64
import os
import json
import random
import pytesseract
from PIL import Image,ImageOps
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

class FuJian():

    session=requests.session()
    num=str(random.random())
    nowtime=str(int(time.time()*1000))
    yname=str(int(time.time()*1000000))
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    def gettoken(self):
        #proxy = {"http": "http://37.59.35.174:1080", "https": "http://37.59.35.174:1080"}
        resp=self.session.get('http://gszxsb.fj-l-tax.gov.cn/portals/web/login',headers=self.headers)
        rsapubkey=re.search('data-param-rsapubkey="(.*?)"',resp.text,re.S).group(1)
        token=re.search('data-param-token="(.*?)"',resp.text,re.S).group(1)
        return rsapubkey,token

    def getyzm(self,token):

        res=self.session.get("http://gszxsb.fj-l-tax.gov.cn/portals/web/captcha/refreshCaptcha?t="+self.num+"&token="+token,headers=self.headers)
        with open(self.yname+".png","wb") as f:
            f.write(res.content)

    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save(self.yname+".png")
        image = Image.open(self.yname+".png")
        image = image.convert("L")
        image = self.iamge2imbw(image, 160)
        image = ImageOps.invert(image)
        image.save(self.yname+".png")

    def iamge2imbw(self, image, threshold):
        # 设置二值化阀值
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, '1')
        image = image.convert('L')
        return image

    def readcode(self, path):
        image = Image.open(path)
        self.pretreat_image(image)
        image = Image.open(path)
        code = pytesseract.image_to_string(image).replace(" ", "").replace("\\", "").replace("¥","y")[0:6]
        return code

    def panduan(self,code):
        data={
            'captcha':code
        }
        res=self.session.post("http://gszxsb.fj-l-tax.gov.cn/portals/web/captcha/validateCaptcha",data=data,headers=self.headers).json()
        if not res["data"]:
            return

        return "验证码错误"

    def getmm(self,password,rsapubkey):
        with open(self.yname+'.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(rsapubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open(self.yname+'.txt', "r") as f:
            public_key = f.read()
            f.close()
        os.remove(self.yname+'.txt')
        password = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(password))
        cipher_text = cipher_text.decode("utf-8")
        return cipher_text
    def login(self,username,mm,code):
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8'

        }
        data={"yhm":username,"idType":"201","idNumber":"","mm":mm,"authCode":code,"redirect_uri":"","response_type":"","client_id":"","sign":"","st":"","dllx":"yhm","state":""}
        data=json.dumps(data)
        res=self.session.post("http://gszxsb.fj-l-tax.gov.cn/portals/web/oauth2/login",data=data,headers=headers).json()
        if res["type"]=='SUCCESS':
            resp=self.session.get("http://gszxsb.fj-l-tax.gov.cn/portals/web/biz/home",headers=self.headers)
            uname=re.search('<span id="current-user-name">(.*?)<',resp.text,re.S).group(1)
            return uname.strip()
        if res["type"]=="ERROR":
            if "密码" in res["content"]:

                return "100"
            elif "不存在" in res["content"]:

                return "300"
            elif "验证码" in res["content"]:
                return "600"
            else:
                return "400"

        return

    def detail(self,uname):
        self.session.get("http://gszxsb.fj-l-tax.gov.cn/wsz-ww-web/web/taxInfo", headers=self.headers)
        self.session.get("http://gszxsb.fj-l-tax.gov.cn/wsz-ww-web/web/base/code/list/DM_GY_KJFWSWJG",
                         headers=self.headers)
        for i in range(2006,self.atime+1):

            res=self.session.get("http://gszxsb.fj-l-tax.gov.cn/wsz-ww-web/web/taxInfo/search?skssqq="+str(i)+"-01-01&skssqz="+str(i)+"-12-31&kjfwjg=23500000000&_="+self.nowtime,headers=self.headers,verify=False).json()
            if res["data"]:
                shuju=res["data"]
                item={}
                item["name"]=uname
                item["year"]=str(i)
                item["fname"]=""
                item["lists"]=shuju
                item=json.dumps(item)
                print(item)
if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # username="dlqwer1234"
    # password="dl2519958023wo"
    username=sys.argv[1]
    password=sys.argv[2]
    try:
        fj=FuJian()
        result=fj.gettoken()
        num=0
        while True:
            fj.getyzm(result[1])
            code = fj.readcode(fj.yname+".png")
            res=fj.panduan(code)
            if not res:
                os.remove(fj.yname + ".png")
                break
            if num==8:
                os.remove(fj.yname+".png")
                break
            os.remove(fj.yname + ".png")
            num+=1
        mm=fj.getmm(password,result[0])
        uname=fj.login(username,mm,code)
        if uname=="100":
            print(100)
        elif uname=="300":
            print(300)
        elif uname=="400":
            print(400)
        elif uname=="600":
            print(600)
        elif uname:
            fj.detail(uname)
        else:
            print(500)
    except Exception as e:
        print(500)

