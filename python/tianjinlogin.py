import binascii
import requests
import time
import re
import os
import json
import datetime
import sys
import io
import base64
import random
import pytesseract
from PIL import Image,ImageOps
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

class TianJin():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))
    def __init__(self):
        self.nowtime=str(int(time.time()*1000))
        self.rnum=str(random.random())
        self.session=requests.session()
        self.yname=str(int(random.random()*10000000000000))
    def getindex(self):
        self.session.get("https://wsswj.tjsat.gov.cn/index.do",headers=self.headers,verify=False)
        res =self.session.get("https://itswt.tjsat.gov.cn/portals/web/loginForTjsw",headers=self.headers,verify=False)
        token=re.search('data-param-token="(.*?)"',res.text,re.S).group(1)
        rsapubkey=re.search('data-param-rsapubkey="(.*?)"',res.text,re.S).group(1)
        return token,rsapubkey
    def getyzm(self,token):

        res=self.session.get("https://itswt.tjsat.gov.cn/portals/web/captcha/refreshCaptcha?t="+self.rnum+"&token="+token,headers=self.headers,verify=False)
        with open(self.yname+".jpg","wb") as f:
            f.write(res.content)

    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save(self.yname+".jpg")
        image = Image.open(self.yname+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 160)
        image = ImageOps.invert(image)
        image.save(self.yname+".jpg")
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
        # x_s = 100  # define standard width
        # y_s = 40  # calc height based on standard width
        # out = image.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
        # out.save(path)
        code = pytesseract.image_to_string(image).replace(" ", "").replace("\\", "")[0:4]
        return code
    def verifycode(self,code):
        data={
            "captcha":code
        }
        res=self.session.post("https://itswt.tjsat.gov.cn/portals/web/captcha/validateCaptcha",data=data,headers=self.headers).json()
        return res["data"]
    # def Encrypt(self,toEncrypt, key):
    #
    #     #toEncrypt = toEncrypt.encode("utf8")
    #     #print(toEncrypt)
    #     # 转换为UTF8编码
    #     key = key.encode("utf8")
    #
    #     bs = AES.block_size
    #     pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)  # PKS7
    #     print(pad)
    #     iv = Random.new().read(bs)
    #     print(iv)
    #     cipher = AES.new(key, AES.MODE_ECB, iv)  # ECB模式
    #     print(cipher)
    #     resData1 = cipher.encrypt(pad(toEncrypt))
    #     print(resData1)
    #     resData2 = binascii.hexlify(resData1)
    #     print(resData2)
    #     # 转为字符串
    #     resData3 = resData2.lower().decode() # 全部小写
    #
    #     print(resData3)
    def login(self,username,password,rsapubkey,code):
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8"
        }
        data={"idType":"201","idNumber":username,"mm":self.getmm(password,rsapubkey),"authCode":code,"redirect_uri":"","response_type":"","client_id":"","sign":"","st":"","dllx":"yhm"}
        data=json.dumps(data)

        res=self.session.post("https://itswt.tjsat.gov.cn/portals/web/oauth2/login",data=data,headers=headers).json()
        if res["type"] == "ERROR":
            if res["content"]=="账户不存在":
                return 300
            elif "账户已被锁" in res["content"]:
                return 600
            elif "1" in res["content"]:
                return 101
            elif "2" in res["content"]:
                return 102
            elif "3" in res["content"]:
                return 103
            elif "4" in res["content"]:
                return 104
            elif "随机验证码错误" in res["content"]:
                return 3
            else:
                return 100

        data={
            "url":"https://itswt.tjsat.gov.cn/portals/web/biz/home"
        }
        self.session.post("https://itswt.tjsat.gov.cn/portals/web/oauth2/afterLoginRedirect",data=data,headers=self.headers)
        res=self.session.get("https://itswt.tjsat.gov.cn/portals/web/biz/home",headers=self.headers)
        name=re.search('<span id="current-user-name">(.*?)<',res.text,re.S)
        if name:
            name=name.group(1).strip()
            return name
        else:
            return 400
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
    def detail(self,name,shuihao):
        res=self.session.get("https://itswt.tjsat.gov.cn/wsz-ww-web/web/taxInfo",headers=self.headers)
        # res=self.session.get("https://itswt.tjsat.gov.cn/wsz-ww-web/web/base/code/list/DM_GY_SRLYSWJG",headers=self.headers).json()
        # print(res)
        #https://itswt.tjsat.gov.cn/wsz-ww-web/web/tianjin/wszm  纳税证明主页
        #https://itswt.tjsat.gov.cn/wsz-ww-web/web/base/code/list/DM_GY_SRLYSWJG 税务机关代码
        #https://itswt.tjsat.gov.cn/wsz-ww-web/web/taxInfo/search?skssqq=2018-01-01&skssqz=2018-12-31&kjfwjg=21297000000&_=1546497487140
        for i in range(2006,self.atime+1):
            res=self.session.get("https://itswt.tjsat.gov.cn/wsz-ww-web/web/taxInfo/search?skssqq="+str(i)+"-01-01&skssqz="+str(i)+"-12-31&kjfwjg=21200000000&_="+self.nowtime,headers=self.headers).json()
            if res["data"]:
                lists=res["data"]
                data={
                    "skssqq":str(i)+"-01-01",
                    "skssqz":str(i)+"-12-31",
                    "kjfwjg":shuihao,
                    "sendEmail":"false",
                    "sbfs":"[]",
                    "kjqy":"[]"
                }
                res=self.session.post("https://itswt.tjsat.gov.cn/wsz-ww-web/web/taxInfo/applyMakeNsqd",data=data,headers=self.headers).json()
                num1=res["data"]
                res=self.session.get("https://itswt.tjsat.gov.cn/wsz-ww-web/web/taxBill?autoSearch=true",headers=self.headers)
                nums=0
                while True:
                    times = str(int(time.time() * 1000 + 100))
                    res = self.session.get("https://itswt.tjsat.gov.cn/wsz-ww-web/web/taxBill/search?fromDate=" + self.startime() + "&toDate=" + self.endtime() + "&_=" + times,headers=self.headers).json()
                    if res["type"] =="ERROR":
                        fname="123.pdf"
                        break

                    if res["data"][0]["zzztMc"] == "制作成功":

                        num = res["data"][0]["nsqdxh"]
                        res = self.session.get(
                            "https://itswt.tjsat.gov.cn/wsz-ww-web/web/taxBill/download/" + str(num))
                        fname = str(i) + self.yname + ".pdf"
                        with open("/home/wwwroot/wbsr/python/files/"+str(i) + self.yname + ".pdf", "wb") as f:
                            f.write(res.content)
                            break
                    if nums == 4:
                        fname = ""
                        break
                    time.sleep(5)
                    nums += 1
                if fname=="":
                    return 405
                item = {}
                item["name"] = name
                item["year"] = str(i)
                item["fname"] = fname
                item["lists"] = lists
                item = json.dumps(item)
                print(item)                # num = 0


    def startime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-6)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d %H:%M:%S')
        timeArray = time.strptime(n_days, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        timeArray = time.localtime(timestamp)
        nowtime = time.strftime("%Y-%m-%d", timeArray)
        return nowtime

    def endtime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(hours=1)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d %H:%M:%S')
        timeArray = time.strptime(n_days, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        timeArray = time.localtime(timestamp)
        nowtime = time.strftime("%Y-%m-%d", timeArray)
        return nowtime
if __name__=="__main__":

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    username=sys.argv[1]
    password=sys.argv[2]
    shuihao=sys.argv[3]
    # username="140109198811170012"
    # password="ask6185416"
    # shuihao="21297000000"
    # username="131022198806100719"
    # password="a8050980200"
    # shuihao="21297000000"
    tj=TianJin()
    result=tj.getindex()
    try:
        if result:
            num=0
            while True:
                tj.getyzm(result[0])
                code=tj.readcode(tj.yname+".jpg")
                data=tj.verifycode(code)
                if not data:
                    os.remove(tj.yname+".jpg")
                    break
                if num==10:
                    os.remove(tj.yname + ".jpg")
                    break
                num+=1
                os.remove(tj.yname + ".jpg")
            name=tj.login(username=username,password=password,rsapubkey=result[1],code=code)
            #用户名不存在
            if name==300:
                print(300)
            ##身份证件号码或密码错误,1次后账户将被锁
            elif name==101:
                print(101)
            ##身份证件号码或密码错误,2次后账户将被锁
            elif name==102:
                print(102)
            #身份证件号码或密码错误,3次后账户将被锁
            elif name==103:
                print(103)
            ##身份证件号码或密码错误,4次后账户将被锁
            elif name==104:
                print(104)
            #未知错误
            elif name==400:
                print(400)
            #密码错误
            elif name==100:
                print(100)
            #账户被锁定
            elif name==600:
                print(600)
            #验证码错误
            elif name==3:
                print(3)
            #登录成功
            elif name:
                resp=tj.detail(name=name,shuihao=shuihao)
                if resp==405:
                    print(405)
            #脚本报错
            else:
                print(500)
        else:
            # 脚本报错
            print(500)
    except Exception as e:
        # 脚本报错
        print(500)
