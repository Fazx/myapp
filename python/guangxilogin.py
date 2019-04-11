import requests
import time
import re
import pytesseract
import random
import base64
import io
import sys
import datetime
import json
import os
from PIL import Image,ImageOps
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from urllib import parse
class GuangXi():

    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))

    def __init__(self):
        self.session=requests.session()
        self.num=str(random.random())
        self.nowtime=str(int(time.time()*1000))
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
    def getyzm(self):
        resp=self.session.get("http://zrrwt.gxds.gov.cn:7666/portals/web/login",headers=self.headers)
        token=re.search('data-param-token="(.*?)"',resp.text).group(1)
        rsapubkey = re.search('data-param-rsapubkey="(.*?)"', resp.text, re.S).group(1)
        res=self.session.get("http://zrrwt.gxds.gov.cn:7666/portals/web/captcha/refreshCaptcha?t="+self.num+"&token="+token)
        with open(self.num+".jpg","wb") as f:
            f.write(res.content)
        return rsapubkey

    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save(self.num+".jpg")
        image = Image.open(self.num+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 160)
        image = ImageOps.invert(image)
        image.save(self.num+".jpg")

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
        code = pytesseract.image_to_string(image).replace(" ", "").replace("\\", "")[0:4]
        code=code.replace("?","7")
        return code

    def puanduan(self,code):
        data={
            "captcha":code
        }
        res=self.session.post("http://zrrwt.gxds.gov.cn:7666/portals/web/captcha/validateCaptcha",data=data,headers=self.headers).json()
        return res["data"]
    def getmm(self,password,rsapubkey):
        with open(self.num+'.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(rsapubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open(self.num+'.txt', "r") as f:
            public_key = f.read()
            f.close()
        os.remove(self.num+'.txt')
        password = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(password))
        cipher_text = cipher_text.decode("utf-8")
        return cipher_text
    def login(self,username,mm,code):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json;charset=UTF-8"
        }
        data={"yhm":username,"idType":"201","idNumber":"","mm":mm,"authCode":code,"redirect_uri":"","response_type":"","client_id":"","sign":"","st":"","dllx":"yhm","state":""}
        data=json.dumps(data)
        res=self.session.post("http://zrrwt.gxds.gov.cn:7666/portals/web/oauth2/login",data=data,headers=headers).json()
        if res["type"] == "ERROR":
            if "账户不存在" in res["content"]:
                return "300"
            if "次后账户将被锁" in res["content"]:
                return "100"
            if "随机验证码错误" in res["content"]:
                return "3"
            return "400"
        res=self.session.get("http://zrrwt.gxds.gov.cn:7666/portals/web/biz/home",headers=self.headers)
        uname = re.search('<span id="current-user-name">(.*?)<', res.text, re.S)
        if uname:
            return uname.group(1).strip()
        return
    def detail(self,uname):
        self.session.get("http://zrrwt.gxds.gov.cn:7666/wsz-ww-web/web/taxInfo",headers=self.headers)
        for i in range(2006,self.atime+1):
            res=self.session.get("http://zrrwt.gxds.gov.cn:7666/wsz-ww-web/web/taxInfo/search?skssqq="+str(i)+"-01-01&skssqz="+str(i)+"-12-01&kjfwjg=24500000000&_="+self.nowtime).json()

            if res["data"]:
                shuju=res["data"]
                djxh=res["data"][0]["kjywrdm"]
                data={
                    "kjqy":"[]",
                    "sbfs":"[]",
                    "skssqq":str(i)+"-01-01",
                    "skssqz":str(i)+"-12-31",
                    "kjfwjg":"24500000000",
                    "sendEmail":"false"
                }
                res=self.session.post("http://zrrwt.gxds.gov.cn:7666/wsz-ww-web/web/taxInfo/applyMakeNsqd",data=data,headers=self.headers).json()
                url="http://zrrwt.gxds.gov.cn:7666/wsz-ww-web/web/taxBill/search?fromDate="+self.startime()+"&toDate="+self.endtime()+"&_="+self.nowtime
                res=self.session.get(url,headers=self.headers).json()
                time.sleep(3)
                pnum=str(res["data"][0]["nsqdxh"])
                res=self.session.get("http://zrrwt.gxds.gov.cn:7666/wsz-ww-web/web/taxBill/download/"+pnum,headers=self.headers)
                fname=str(i)+djxh+'.pdf'
                with open("/home/wwwroot/wbsr/python/files/" + fname,"wb") as f:
                    f.write(res.content)
                item={}
                item["name"]=uname
                item["year"]=str(i)
                item["fname"]=fname
                item["lists"]=shuju
                item=json.dumps(item)
                print(item)

    def startime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-7)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d')

        return n_days

    def endtime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(hours=1)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d')
        return n_days

if __name__=="__main__":

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    username=sys.argv[1]
    username = parse.unquote(username)
    password=sys.argv[2]
    # username="廖玲秀"
    # password="a123456789"
    gx=GuangXi()
    try:
        gx=GuangXi()
        num=0
        while True:
            rsapubkey=gx.getyzm()
            code=gx.readcode(gx.num+".jpg")
            result=gx.puanduan(code)
            if not result:
                os.remove(gx.num+".jpg")
                break
            os.remove(gx.num + ".jpg")
            if num==7:
                break
            num += 1

        mm=gx.getmm(password,rsapubkey)
        uname=gx.login(username,mm,code)
        if uname=="100":
            print(100)
        elif uname=="300":
            print(300)
        elif uname=="3":
            print(3)
        elif uname=="400":
            print(400)
        elif uname:
            gx.detail(uname)
        else:
            print(500)
    except Exception as e:
        print(500)


