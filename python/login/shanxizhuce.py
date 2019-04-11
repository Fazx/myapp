import requests
import ssl
import random
import os
import re
import sys
import io
import json
import base64
import pytesseract
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from PIL import ImageOps,Image
from urllib import parse

ssl._create_default_https_context = ssl._create_unverified_context

class ShanXizhuce():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    def __init__(self):
        self.session=requests.session()
        self.rname = str(int(random.random() * 10000000000000))
        self.num = str(int(random.random()*10000000000))

    def zhuce(self):
        self.session.get("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/register/unionpayRegist",headers=self.headers,verify=False)
    def getyzm(self):
        res=self.session.get(" https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/captcha/captcha?t=0.576455512568752",headers=self.headers)
        with open(self.num+".jpg","wb") as f:
            f.write(res.content)

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
        res=self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/captcha/validateCaptcha",data=data,headers=self.headers).json()
        return res["data"]

    def zhuce1(self,name,idnum,banknum,phone,code,username,password):
        data={
            "xm":name,
            "sfzjhm":idnum,
            "gjhdqdm":"156",
            "yhkh":banknum,
            "sjhm":phone,
            "yzm":code,
            "sftyxy":"true",
            "sfzjlxDm":"201"
                    }
        # print(data)
        headers={
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"

        }
        res=self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/register/verifyBankcardWithHlj",data=data,headers=headers).json()
        # print(res)
        if res["type"]=="ERROR":
            print(res["content"])
            return
        res=self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/register/editBaseInfo",data=data,headers=self.headers)
        if name not in res.text:
            print("注册失败,请重新注册")
            return
        rsapubkey=re.search('data-param-rsapubkey="(.*?)"',res.text,re.S)
        if not rsapubkey:
            print("注册超时,请重新注册")
            return
        rsapubkey=rsapubkey.group(1)
        data={
            "dlm":username
        }
        res=self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/validate/dlm",data=data,headers=self.headers).json()
        if res["type"]=="ERROR":
            print(res["content"])
            return
        # print(res)
        passwords=self.getmm(password,rsapubkey)
        data = {"dlm": username, "mm": passwords, "qrmm": password, "needSjhm": "", "st": ""}
        data=json.dumps(data)
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json;charset=UTF-8"
        }
        res=self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/register/registerUser",data=data,headers=head)
        # print(res.text)
        if name not in res.text:
            print("注册错误,请重新注册")

            return
        self.session.get("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/pwdProtect",headers=self.headers)
        print("注册成功")
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

if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    name=sys.argv[1]
    name = parse.unquote(name)
    idnum=sys.argv[2]
    banknum=sys.argv[3]
    username=sys.argv[4]
    phone=sys.argv[5]
    password=sys.argv[6]

    # name="贾浩"
    # idnum="131022198806100719"
    # banknum="6228481000884523118"
    # username="颓废的兔子1"
    # phone="156004611001"
    # #password="8到15位，且至少包含字母、数字与符号中的两种"
    # password="a8050980200"
    sxz=ShanXizhuce()
    sxz.zhuce()
    num=0
    while True:
        sxz.getyzm()
        code=sxz.readcode(sxz.num+".jpg")
        result=sxz.puanduan(code)
        if not result:
            os.remove(sxz.num+".jpg")
            break
        os.remove(sxz.num + ".jpg")
        if num==10:
            break
        num += 1
    sxz.zhuce1(name=name,idnum=idnum,banknum=banknum,phone=phone,code=code,username=username,password=password)

