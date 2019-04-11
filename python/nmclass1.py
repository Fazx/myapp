import requests
import re
import json
import time
import datetime
import os
import sys
import io
import base64
import pytesseract
from urllib import parse
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from PIL import Image,ImageOps

class NeiMengGu():
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))
    session=requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    ntime=str(int(time.time()*100000))
    nowtime=str(int(time.time()*1000))

    def getlt(self):
        res = self.session.get(
            "http://zrrtax.nmds.gov.cn:8985/portals/web/loginForNmsw",headers=self.headers,verify=False)

        lt = re.search('data-param-rsapubkey="(.*?)" data-param-token="(.*?)">', res.text)
        execution=lt.group(1)
        lt=lt.group(2)
        return execution,lt

    def getyzm(self,lt):
        res=self.session.get("http://zrrtax.nmds.gov.cn:8985/portals/web/captcha/refreshCaptcha?t=0.24949178832857077&token="+lt[1],headers=self.headers,verify=False)
        with open(self.ntime+".jpg","wb") as f:
            f.write(res.content)
            f.close()

    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save( self.ntime+".jpg")
        image = Image.open(self.ntime+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 160)
        image = ImageOps.invert(image)
        image.save(self.ntime+".jpg")
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
    def getmm(self,password,pubkey):
        with open(self.ntime+'.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(pubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open( self.ntime+'.txt', "r") as f:
            public_key = f.read()
            f.close()
        os.remove(self.ntime+'.txt')
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
        self.session.post("http://zrrtax.nmds.gov.cn:8985/portals/web/oauth2/login",data=data,headers=headers)
        res=self.session.get("http://zrrtax.nmds.gov.cn:8985/portals/web/biz/home",headers=self.headers)
        uname=re.search('item=INFO">(.*?)</a>',res.text)
        if uname:
            return uname.group(1)
        else:
            pass


    def detail(self,uname):


        for j in range(2006,self.atime+1):
            data={
                "skssqq":str(j)+"-01-01",
                "skssqz":str(j)+"-12-31",
                "kjfwSwjg":"21500000000",
                "pzkjzl":"Z99001002",
                "_":self.nowtime
            }
            res=self.session.get("http://zrrtax.nmds.gov.cn:8985/wsz-ww-web/web/wszm/mxcx",params=data,headers=self.headers).json()
            if res["data"]:
                djxh=res["data"][0]["djxh"]
                lists=res["data"]
                item_list=[]
                num=0
                for item in res["data"]:
                    item["checked"]=True
                    item["_uid"]=num
                    item["_index"]=num
                    num+=1
                    item_list.append(item)
                item_list=str(item_list)
                item_list=item_list.replace("None","null").replace("'",'"').replace(" ","").replace("True","true").replace("False","false")
                data1={
                    "skssqq":str(j)+"-01-01",
                    "skssqz":str(j)+"-12-31",
                    "kjfwSwjg":"21500000000",
                    "pzkjzl":"Z99001002",
                    "nsmxs":item_list
                }
                headers={
                    "Host":"zrrtax.nmds.gov.cn:8985",
                    "Connection":"keep-alive",
                    "Origin":"http://zrrtax.nmds.gov.cn:8985",
                    "X-Requested-With":"XMLHttpRequest",
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                    "Referer":"http://zrrtax.nmds.gov.cn:8985/wsz-ww-web/web/wszm?"

                }
                res=self.session.post("http://zrrtax.nmds.gov.cn:8985/wsz-ww-web/web/wszm/wszmSq",data=data1,headers=headers)
                time.sleep(2)
                data2={"tfrqq":self.startime(),"tfrqz":self.endtime(),"pzkjzl":"Z99001002","pageIndex":0,"pageSize":10}
                data2=json.dumps(data2)
                head={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                    "Content-Type": "application/json;charset=UTF-8"
                }
                res=self.session.post("http://zrrtax.nmds.gov.cn:8985/wsz-ww-web/web/ysqwszm/ysqwszmCx",data=data2,headers=head).json()
                dzwszcymw=res["data"]["records"][0]["dzwszcymw"]
                pzhm=res["data"]["records"][0]["pzhm"]

                data3={
                    "djxh":djxh,
                    "pzzlDm":"Z99001002",
                    "pzPcZg":"(180)蒙地电证明",
                    "pzhm":pzhm,
                    "dzwszcymw":dzwszcymw
                }
                res=self.session.post("http://zrrtax.nmds.gov.cn:8985/wsz-ww-web/web/ysqwszm/downloadWszm",data=data3,headers=self.headers)
                fname=str(j)+djxh+".pdf"
                with open(fname,"wb") as f:
                    f.write(res.content)
                item={}
                item["name"]=uname
                item["year"]=str(j)
                item["fname"]=fname
                item["lists"]=lists
                item=json.dumps(item)
                print(item)
    def startime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-30)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d %H:%M:%S')
        timeArray = time.strptime(n_days, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        timeArray = time.localtime(timestamp)
        nowtime = time.strftime("%Y-%m-%dT %H:%M:%S.658Z", timeArray)
        return nowtime

    def endtime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(hours=1)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d %H:%M:%S')
        timeArray = time.strptime(n_days, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        timeArray = time.localtime(timestamp)
        nowtime = time.strftime("%Y-%m-%dT %H:%M:%S.658Z", timeArray)
        return nowtime
if __name__=="__main__":
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # name=sys.argv[1]
    # name = parse.unquote(name)
    # password=sys.argv[2]
    name="15040219701123032X"
    password="23032X"
    nmg=NeiMengGu()
    token=nmg.getlt()
    num=0
    while True:
        nmg.getyzm(lt=token)
        mm=nmg.getmm(password,token[0])
        code=nmg.readcode(nmg.ntime+".jpg")
        uname=nmg.login(name,mm,code)
        if uname:
            os.remove(nmg.ntime+".jpg")
            nmg.detail(uname)
            break
        num+=1
        if num==8:
            print("验证码错误")
            os.remove(nmg.ntime + ".jpg")
            break






