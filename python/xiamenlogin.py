import requests
import re
import random
import json
import os
import datetime
import time
import io
import sys
import base64
import pytesseract
from urllib import parse
from PIL import Image,ImageOps
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
class XiaMen():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    timeArray = time.localtime(time.time())
    atime = time.strftime("%Y-%m-%d", timeArray)
    timeArray = time.localtime(time.time())
    nowyear= int(time.strftime("%Y", timeArray))
    cardtypes={
        "身份证":"201",
        "军官证":"202",
        "武警警官证":"203",
        "士兵证":"204",
        "外国护照":"208",
        "港澳居民来往内地通行证":"210",
        "台湾居民来往大陆通行证":"213",
        "香港身份证":"219",
        "台湾身份证":"220",
        "澳门身份证":"221",
        "中国护照":"227",
        "外国人永久居留证":"233"
    }
    def __init__(self):
        self.session=requests.session()
        self.rtime=str(random.random())
        self.nowtime=str(int(time.time()*1000))
        self.rname=str(int(random.random()*1000000000000))
    def getindex(self):
        res=self.session.get("https://zrr.xm-l-tax.gov.cn/portals/web/login",headers=self.headers,verify=False)
        # self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/getAnnouncement",headers=self.headers)
        # data={
        #     "pageIndex":"0",
        #     "pageSize":"2"
        #             }
        # res=self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/tzgg/findTzggsPage",data=data,headers=self.headers).json()
        token=re.search('data-param-token="(.*?)"',res.text).group(1)
        rsapubkey=re.search('data-param-rsapubkey="(.*?)"',res.text).group(1)
        return token,rsapubkey
    def getyzm(self,token):
        res=self.session.get("https://zrr.xm-l-tax.gov.cn/portals/web/captcha/refreshCaptcha?t="+self.rtime+"&token="+token,headers=self.headers)
        with open(self.rname+".jpg","wb") as f:
            f.write(res.content)

    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save(self.rname + ".jpg")
        image = Image.open(self.rname + ".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 180)
        image = ImageOps.invert(image)
        image.save(self.rname + ".jpg")
        # return image


        # 灰度图像二值化,返回0/255二值图像

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
        x_s = 100  # define standard width
        y_s = 40  # calc height based on standard width
        image = image.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
        image.save(path)
        self.pretreat_image(image)
        image = Image.open(path)
        code = pytesseract.image_to_string(image).replace(" ", "").replace("\\", "")[0:4]
        return code
    def yanzheng(self,code):
        data={
            "captcha":code
        }
        res=self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/captcha/validateCaptcha",data=data,headers=self.headers).json()
        return res["data"]

    def login(self,idtype,idnum,password,code,rsapubkey):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8"
        }
        data={"idType":self.cardtypes[idtype],"idNumber":idnum,"mm":self.getmm(password,rsapubkey),"authCode":code,"redirect_uri":"","response_type":"","client_id":"","sign":"","st":"","dllx":"yhm"}
        data=json.dumps(data)
        res=self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/oauth2/login",data=data,headers=headers).json()
        if res["type"] == "ERROR":
            if "验证码错误" in res["content"]:
                return "3"
            elif "账户不存在" in res["content"]:
                return "300"
            elif "次后账户将被锁" in res["content"]:
                return "100"
            else:
                return "400"
        data={"url":"https://zrr.xm-l-tax.gov.cn/portals/web/biz/home"}
        res=self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/oauth2/afterLoginRedirect",data=data,headers=self.headers).json()
        res=self.session.get("https://its.xm-l-tax.gov.cn//web/zh/oauth2/logout?backurl="+res["data"],headers=self.headers,verify=False)
        if "欢迎" not in res.text:
            return "500"
        uname=re.search('<span id="current-user-name">(.*?)</span>',res.text,re.S).group(1).strip()
        return uname

    def getmm(self, password, pubkey):
        with open(self.rname + '.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(pubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open(self.rname + '.txt', "r") as f:
            public_key = f.read()
            f.close()
        os.remove(self.rname + '.txt')
        password = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(password))
        cipher_text = cipher_text.decode("utf-8")
        return cipher_text

    def detail(self,uname):

        self.session.get("https://zrr.xm-l-tax.gov.cn/wsz-ww-web/web/taxInfo",headers=self.headers,verify=False)
        for i in range(2006,self.nowyear+1):
            res=self.session.get("https://zrr.xm-l-tax.gov.cn/wsz-ww-web/web/xiamen/taxInfo/search?skssqs="+str(i)+"-01-01&skssqz="+str(i)+"-12-31&_="+self.nowtime).json()
            if res["data"]:
                shuju=res["data"]
                data={
                    "skssqs":str(i)+"-01-01",
                    "skssqz":str(i)+"-12-31"
                                    }
                self.session.post("https://zrr.xm-l-tax.gov.cn/wsz-ww-web/web/xiamen/taxInfo/applyMakeNsqd",data=data,headers=self.headers)
                self.session.get("https://zrr.xm-l-tax.gov.cn/wsz-ww-web/web/taxBill?autoSearch=true",headers=self.headers)
                res=self.session.get("https://zrr.xm-l-tax.gov.cn/wsz-ww-web/web/taxBill/search?fromDate="+self.startime()+"&toDate="+self.atime+"&_="+self.nowtime)
                self.session.get("https://zrr.xm-l-tax.gov.cn/wsz-ww-web/web/taxBill?autoSearch=true",headers=self.headers)
                while True:
                    res=self.session.get("https://zrr.xm-l-tax.gov.cn/wsz-ww-web/web/taxBill/search?fromDate="+self.startime()+"&toDate="+self.atime+"&_="+self.nowtime).json()
                    if res["data"][0]["zzztMc"]=="制作成功":
                        pnum=str(res["data"][0]["nsqdxh"])
                        break
                    time.sleep(2)
                res=self.session.get("https://zrr.xm-l-tax.gov.cn/wsz-ww-web/web/taxBill/download/"+pnum,headers=self.headers)
                fname=str(i)+self.rname+".pdf"
                with open("/home/wwwroot/wbsr/python/files/"+fname,"wb") as f:
                    f.write(res.content)
                item={}
                item["name"]=uname
                item["years"]=str(i)
                item["fname"]=fname
                item["lists"]=shuju
                item=json.dumps(item)
                print(item)

    def startime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-7)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d')
        timeArray = time.strptime(n_days, "%Y-%m-%d")
        timestamp = time.mktime(timeArray)
        timeArray = time.localtime(timestamp)
        nowtime = time.strftime("%Y-%m-%d", timeArray)
        return nowtime
if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    idtype=sys.argv[1]
    idtype = parse.unquote(idtype)
    idnum=sys.argv[2]
    password=sys.argv[3]
    # idtype="身份证"
    # idnum="350206199609045525"
    # password="tangtang1996"
    try:
        xm=XiaMen()
        tokens=xm.getindex()
        num=0
        while True:
            rsapubkey=xm.getyzm(tokens[0])
            code=xm.readcode(xm.rname+".jpg")
            result=xm.yanzheng(code)
            if not result:
                os.remove(xm.rname+".jpg")
                break
            if num==15:
                os.remove(xm.rname+".jpg")
                break
            num+=1
            os.remove(xm.rname+".jpg")

        uname=xm.login(idtype=idtype,idnum=idnum,password=password,code=code,rsapubkey=tokens[1])
        if uname=="3":
            print(3)
        elif uname=="100":
            print(100)
        elif uname=="300":
            print(300)
        elif uname=="400":
            print(400)
        elif uname=="500":
            print(500)
        else:
            xm.detail(uname)

    except Exception as e:
        print(500)