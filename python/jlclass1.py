import requests
import base64
import json
import pytesseract
import sys
import io
import time
import os
import re
from PIL import Image,ImageOps
from urllib import parse
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class Jilin():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    session=requests.session()
    ntime=str(int(time.time()*1000))
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))
    def getoken(self):
        res=self.session.get("https://zrrwt.jl-n-tax.gov.cn:10803/portals/web/login",headers=self.headers,verify=False)
        html=res.text
        token=re.search('data-param-rsapubkey="(.*?)".*?data-param-token="(.*?)"',html,re.S)
        rsapubkey=token.group(1)
        token=token.group(2)
        return rsapubkey,token

    def getyzm(self,token):
        res=self.session.get("https://zrrwt.jl-n-tax.gov.cn:10803/portals/web/captcha/refreshCaptcha?t=0.42792863562510797&token="+token,headers=self.headers)
        with open("/home/wwwroot/wbsr/python/images/"+self.ntime+".jpg","wb") as f:
            f.write(res.content)
            f.close()

    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save("/home/wwwroot/wbsr/python/images/"+self.ntime+".jpg")
        image = Image.open("/home/wwwroot/wbsr/python/images/"+self.ntime+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 160)
        image = ImageOps.invert(image)
        image.save("/home/wwwroot/wbsr/python/images/"+self.ntime+".jpg")

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

    def verifycode(self,code):
        data={"captcha":code}
        res=self.session.post("https://zrrwt.jl-n-tax.gov.cn:10803/portals/web/captcha/validateCaptcha",data=data,headers=self.headers).json()
        return res["data"]

    def getmm(self,password,pubkey):
        with open("/home/wwwroot/wbsr/python/images/"+self.ntime+'.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(pubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open("/home/wwwroot/wbsr/python/images/"+self.ntime+'.txt', "r") as f:
            public_key = f.read()
            f.close()
        os.remove("/home/wwwroot/wbsr/python/images/"+self.ntime+'.txt')
        password = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(password))
        cipher_text = cipher_text.decode("utf-8")
        return cipher_text
    def login(self,name,mm,code):
        headers={
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        data={"yhm":name,"idType":"201","idNumber":"","mm":mm,"authCode":code,"redirect_uri":"","response_type":"","client_id":"","sign":"","st":"","dllx":"yhm"}
        data=json.dumps(data)
        self.session.post("https://zrrwt.jl-n-tax.gov.cn:10803/portals/web/oauth2/login",data=data,headers=headers)
        res=self.session.get("https://zrrwt.jl-n-tax.gov.cn:10803/portals/web/biz/home",headers=self.headers)
        self.session.post("https://zrrwt.jl-n-tax.gov.cn:10803/portals/web/biz/getSt",headers=self.headers)
        name=re.search('<span id="current-user-name">(.*?)<',res.text,re.S)
        if name:
            return name.group(1).strip()
        else:
            return
    def detail(self,uname):
        try:
            for i in range(2006,self.atime+1):
                self.session.post("https://zrrwt.jl-n-tax.gov.cn:10803/portals/web/biz/saveEvent",headers=self.headers)
                resp=self.session.get("https://zrrwt.jl-n-tax.gov.cn:10803/wsz-ww-web/web/base/code/list/DM_GY_SRLYSWJG",headers=self.headers).json()
                res=self.session.post("https://zrrwt.jl-n-tax.gov.cn:10803/wsz-ww-web/web/wszm/getPzkjzl",headers=self.headers).json()
                res=self.session.get("https://zrrwt.jl-n-tax.gov.cn:10803/wsz-ww-web/web/wszm/mxcx?skssqq="+str(i)+"-01-01&skssqz="+str(i)+"-12-31&kjfwSwjg=22200000000&pzkjzl=Z99001002&_="+self.ntime,headers=self.headers).json()
                if res["data"]:
                    item={}
                    item["year"]=str(i)
                    item["name"]=uname
                    item["fname"]=str(i)+res["data"][0]["dzsphm"]+".pdf"
                    item["lists"]=res["data"]
                    item=json.dumps(item)
                    print(item)
        except:
            print(400)

if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    name=sys.argv[1]
    name = parse.unquote(name)
    password=sys.argv[2]
    # name="18904321046wym"
    # password="123456wym"
    try:
        jl=Jilin()
        tokens=jl.getoken()
        num=0
        while True:
            jl.getyzm(tokens[1])
            code=jl.readcode("/home/wwwroot/wbsr/python/images/"+jl.ntime+".jpg")
            data=jl.verifycode(code)
            num+=1
            if not data:
                os.remove("/home/wwwroot/wbsr/python/images/"+jl.ntime+".jpg")
                mm=jl.getmm(password,tokens[0])
                uname=jl.login(name,mm,code)
                if uname:
                    jl.detail(uname)
                    break
                else:
                    print(300)

                    break
            os.remove("/home/wwwroot/wbsr/python/images/"+jl.ntime+".jpg")
            if num==5:
                print(100)
                break
    except:
        print(500)
