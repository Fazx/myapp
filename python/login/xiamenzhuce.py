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
from urllib import parse
class XiaMenzhuce():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    def __init__(self):
        self.session=requests.session()
        self.rname=str(int(random.random()*10000000000000))
        self.rtime=str(random.random())
    def getcookies(self,cookies):
        if cookies=="0":
            print("请填写注册信息")
            return
        res=str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}
        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
    def getyanzhengma(self):
        res=self.session.get("https://zrr.xm-l-tax.gov.cn/portals/web/captcha/captcha?t="+self.rtime,headers=self.headers,verify=False)
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
        self.pretreat_image(image)
        image = Image.open(path)
        code = pytesseract.image_to_string(image).replace(" ", "").replace("\\", "")[0:4]
        return code

    def yanzheng(self, code):
        data = {
            "captcha": code

        }
        res = self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/captcha/validateCaptcha", data=data,
                                headers=self.headers, verify=False).json()
        return res["data"]

    def zhuce(self,name,idcard,bankcard,phone,phonecode,imagecode,password):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        }
        data={
            "xm":name,
            "sfzjhm":idcard,
            "gjhdqdm":"156",
            "yhkh":bankcard,
            "sjhm":phone,
            "sjyzm":phonecode,
            "yzm":imagecode,
            "sfzjlxDm":"201"
        }
        #{"type":"ERROR","code":null,"content":"录入信息与您银行卡信息不符，请重新填写。","cause":null,"contentList":null,"data":null}
        #{'type': 'ERROR', 'code': '随机验证码已过期，请重新刷新验证码', 'content': '随机验证码已过期，请重新刷新验证码', 'cause': None, 'contentList': None, 'data': None}
        res=self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/register/verifyBankcard",data=data,headers=headers,verify=False).json()
        if res["type"] == "ERROR":
            print(res["content"])
            return
        if "sfzjlxMc" not in res["data"]:
            print(res["data"])
            return
        res=self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/register/editBaseInfo",data=data,headers=self.headers)
        res.encoding="utf-8"
        if name not in res.text:
            print("网络错误,请重新注册")
            return
        rsapubkey=re.search('data-param-rsapubkey="(.*?)"',res.text,re.S)
        if not rsapubkey:
            print("网络错误,请重新注册")
            return
        rsapubkey=rsapubkey.group(1)
        passwords=self.getmm(password,rsapubkey)
        data={"mm":passwords,"qrmm":password,"needSjhm":"","st":""}
        data=json.dumps(data)
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json;charset=UTF-8"
        }
        res=self.session.post("https://zrr.xm-l-tax.gov.cn/portals/web/register/registerUser",data=data,headers=head)
        if name not in res.text:
            print("注册失败,请重新注册")
            return
        self.session.get("https://zrr.xm-l-tax.gov.cn/portals/web/pwdProtect",headers=self.headers)
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

    xmz=XiaMenzhuce()
    # 姓名
    name = sys.argv[1]
    name = parse.unquote(name)
    # 手机号
    phone = sys.argv[2]
    # 密码
    password = sys.argv[3]
    # 身份证号
    idcard = sys.argv[4]
    # 银行卡号
    bankcard = sys.argv[5]
    # 手机验证码
    phonecode = sys.argv[6]
    cookies = sys.argv[7]
    xmz.getcookies(cookies=cookies)
    num=0
    while True:
        xmz.getyanzhengma()
        imagecode = xmz.readcode(xmz.rname + ".jpg")
        data = xmz.yanzheng(imagecode)
        if not data:
            os.remove(xmz.rname+".jpg")
            break
        if num==10:
            os.remove(xmz.rname + ".jpg")
            break
        os.remove(xmz.rname + ".jpg")


    xmz.zhuce(name=name,idcard=idcard,bankcard=bankcard,phone=phone,phonecode=phonecode,imagecode=imagecode,password=password)






    #
    # xmz.zhuce(name=name,idcard=idcard,bankcard=bankcard,phone=phone,phonecode=phonecode,imagecode=imagecode,password=password)