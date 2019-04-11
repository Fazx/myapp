# -*- coding:utf-8 -*-
import requests
import re
import ssl
import os
import json
import sys
import io
import time
import datetime
import base64
from Crypto.Cipher import PKCS1_v1_5
from urllib import parse
from Crypto.PublicKey import RSA
import pytesseract
from PIL import Image,ImageOps
import random
from urllib import parse
ssl._create_default_https_context=ssl._create_unverified_context

class ShangHai():


    session=requests.session()
    times=str(int(time.time()*1000))
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    pname=str(int(random.random()*100000000000))
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))
    nowtime = time.strftime("%Y-%m-%d", timeArray)
    n_days =datetime.datetime.now()+datetime.timedelta(days=-7)
    startday = n_days.strftime('%Y-%m-%d')
    def login(self):
        respon=self.session.get("https://gr.tax.sh.gov.cn/portals/web/login",headers=self.headers,verify=False)
        #print(respon.text)
        token=re.search('data-param-rsapubkey="(.*?)" data-param-token="(.*?)">',respon.text)
        return token

    def yzm(self,token):
        token=token.group(2)
        res=self.session.get("https://gr.tax.sh.gov.cn/portals/web/captcha/refreshCaptcha?t=0.21238156459281932&token="+token,headers=self.headers,verify=False)
        with open(self.pname+".jpg",'wb')as f:
            f.write(res.content)


    def pretreat_image(self,image):
        image = ImageOps.invert(image)
        image.save(self.pname+".jpg")
        image = Image.open(self.pname+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 160)
        image = ImageOps.invert(image)
        image.save(self.pname+".jpg")
        #return image


# 灰度图像二值化,返回0/255二值图像
    def iamge2imbw(self,image, threshold):
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

    def readcode(self,path):
        image=Image.open(path)
        self.pretreat_image(image)
        image = Image.open(path)
        code=pytesseract.image_to_string(image).replace(" ","").replace("\\","")[0:4]

        return code

    def yanzheng(self,code):
        data={
            "captcha":code

        }
        res=self.session.post("https://gr.tax.sh.gov.cn/portals/web/captcha/validateCaptcha",data=data,headers=self.headers,verify=False).json()
        return res["data"]

    def tokenlogin(self,name,password,code):
        with open(self.pname+".txt","r") as f:
            public_key=f.read()
            f.close()
        headerss={
            "Host": "gr.tax.sh.gov.cn",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            #"X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": "https://gr.tax.sh.gov.cn/portals/web/login"
        }
        # print(public_key.replace("'","'''"))
    #     public_key = '''-----BEGIN PUBLIC KEY-----
    # MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC7kw8r6tq43pwApYvkJ5laljaN9BZb21TAIfT/vexbobzH7Q8SUdP5uDPXEBKzOjx2L28y7Xs1d9v3tdPfKI2LR7PAzWBmDMn8riHrDDNpUpJnlAGUqJG9ooPn8j7YNpcxCa1iybOlc2kEhmJn5uwoanQq+CA6agNkqly2H4j6wIDAQAB
    # -----END PUBLIC KEY-----'''
        password = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(password))

        cipher_text=cipher_text.decode("utf-8")

        data={"yhm":name,
              "idType":"201",
              "idNumber":"",
              "mm":cipher_text,
              "authCode":code,
              "redirect_uri":"",
              "response_type":"",
              "client_id":"",
              "sign":"",
              "st":"",
              "dllx":"yhm",
              "state":""}
        cipher_text = json.dumps(data)
        res=self.session.post("https://gr.tax.sh.gov.cn/portals/web/oauth2/login",data=cipher_text,headers=headerss,verify=False).json()
        if res["type"]=="ERROR":
            if "密码" in res["content"]:

                return "100"
            elif "用户不存在" in res["content"]:

                return "300"
            else:
                return "400"

        return
    def detail(self):

        for i in range(2006,self.atime+1):
            res=self.session.get("https://gr.tax.sh.gov.cn/wsz-ww-web/web/shanghai/taxInfo/search?skssqq="+str(i)+"-01-01&skssqz="+str(i)+"-12-31&_="+self.times,headers=self.headers,verify=False).json()
            shuju=res["data"]
            if shuju:
                self.session.get("https://gr.tax.sh.gov.cn/wsz-ww-web/web/taxBill?autoSearch=true",headers=self.headers,verify=False)
                data={
                    "skssqq": str(i) + "-01-01",
                    "skssqz":str(i)+"-12-31",
                    "sendEmail":"false",
                    "qsfw":"true",
                    "sbfs":'[{"dm":"K","mc":"扣缴申报"}]',
                    "kjqy":'[{"dm":"10013101003001674026","mc":"上海新飞凡电子商务有限公司"}]'
                }
                resp=self.session.post("https://gr.tax.sh.gov.cn/wsz-ww-web/web/shanghai/taxInfo/applyMakeNsqd",data=data,headers=self.headers,verify=False)

                nums=0
                while True:
                    res=self.session.get("https://gr.tax.sh.gov.cn/wsz-ww-web/web/taxBill/search?fromDate="+self.startday+"&toDate="+self.nowtime+"&_="+self.times,headers=self.headers,verify=False).json()
                    #"打开PDF文件需要密码，密码为身份证件号码后6位，若包含字母请大写。"
                    if res["data"][0]["zzztMc"]=="制作成功":
                        num=res["data"][0]["nsqdxh"]
                        url = "https://gr.tax.sh.gov.cn/wsz-ww-web/web/taxBill/download/" + str(num)
                        # time.sleep(1)

                        res = self.session.get(url=url, headers=self.headers, verify=False)
                        fname=self.pname+str(num) + ".pdf"
                        with open("/home/wwwroot/wbsr/python/files/"+ fname, "wb") as f:
                            f.write(res.content)
                        break
                    time.sleep(2)
                    if nums==10:
                        fname=""
                        break
                    nums+=1
                resps = self.session.get(
                    "https://gr.tax.sh.gov.cn/portals/web/biz/personalInfo/personalInfoPage",
                    headers=self.headers, verify=False)
                name = re.search(
                    '<div class="col-2 fn-ar label">真实姓名</div>(.*?)<div class="col-8 content">(.*?)</div>',
                    resps.text, re.S)
                name = name.group(2)
                item={}
                item["name"]=name
                item["year"]=str(i)
                item["fname"]=fname
                item["lists"]=shuju
                item=json.dumps(item)
                print(item)


if __name__=="__main__":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        name=sys.argv[1]
        password=sys.argv[2]
        name=parse.unquote(name)

        # name="13661506575"
        # password="1234567c"
        sh=ShangHai()
        token=sh.login()
        #sh.yzm(token)
        with open(sh.pname+'.txt','w') as f:
            f.write("-----BEGIN PUBLIC KEY-----"+"\n")
            f.write(token.group(1)+"\n")
            f.write("-----END PUBLIC KEY-----")
        num=0
        while True:
            sh.yzm(token)
            #print(sh.pname)
            code=sh.readcode(sh.pname+".jpg")

            if code:
                data=sh.yanzheng(code)
                if data:
                    num+=1
                    pass
                else:
                    break
                if num==5:
                    print(3)
                    break


        result=sh.tokenlogin(name,password,code)
        if result == "100":
            print(100)

        elif result=="300":
            print(300)

        elif result=="400":
            print(400)
        else:
            sh.detail()
            os.remove(sh.pname+".jpg")
            os.remove(sh.pname+".txt")
    except Exception as e:
        print(500)


    #
    # rsaEncry: function (password) {
    #     var rsaPubKey = this.uis.st.param.rsapubkey;
    #     var encrypt = new JSEncrypt();
    #     encrypt.setPublicKey(rsaPubKey);
    #     return encrypt.encrypt(password);
    # },
