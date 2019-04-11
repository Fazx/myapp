# -*- coding:utf-8 -*-
import requests
import time
import logging
import sys
import os
import io
from urllib import parse
import subprocess
import pytesseract
from PIL import Image
from PIL import ImageOps

class BeiJing():

    session=requests.session()
    ctime=str(int(time.time()*1000))

    def __init__(self):
        pass

    def login(self,name,card,password):

        respon=self.session.get("http://yidong.tax861.gov.cn/bsfw/gscx.htm")
        #respon.encoding="utf-8"
        res=self.session.get("http://yidong.tax861.gov.cn/random.do?d="+self.ctime)
        #print(res.cookies.get_dict())
        with open('text.jpg', 'wb') as f:
            f.write(res.content)
        code=self.getAuthCode("text.jpg")
        data={
           "idCardtype":"身份证",
            "idCardno"	:card,
            "name":name,
            "password":password,
           "code":code
        }
        if os.path.exists("text.jpg"):
            os.remove("text.jpg")
        #if os.path.exists("captcha.txt"):
            #os.remove("captcha.txt")
        res=self.session.post("http://yidong.tax861.gov.cn/gscxLogin.do?d="+self.ctime,data=data).json()
        print(res["message_code"])

        if res["message_code"]=="0":
            resp=self.session.post("http://yidong.tax861.gov.cn/gscxYears.do?d=1536300774668").json()
            return resp

        elif res["message"]=="证照类型、号码不存在或密码错误":
            result="证照类型、号码不存在或密码错误"
            return result
        else:
            result="验证码错误"
            return result


    def check(self,name,card,password):
	
        resp=self.login(name,card,password)
        print("yiyunxing")
	if resp=="证照类型、号码不存在或密码错误" or resp=="验证码错误":
            return
        #return resp
        for year in resp:
            year=year["year"]
            datas={
                "taxYear":year
            }
            #return year
            res=self.session.post("http://yidong.tax861.gov.cn/gscx.do?d="+self.ctime,data=datas).json()

            print(res)
            #lists=res["mxsbList"]
#
                    #print(name,income,nsrmc,taxmonth,taxyear,taxactual)
            #else:
                #print(year+"无纳税信息")

    def cleanImage(self,imagePath):
        image = Image.open(imagePath)  # 读取文件
        image = image.point(lambda x: 0 if x<143 else 255)  #对像素点处理
        borderImage = ImageOps.expand(image,border=20,fill='white') #图片延伸
        borderImage.save(imagePath) #保存

    def getAuthCode(self,file, driver="a", url="b"):

        self.cleanImage("text.jpg")  # 图片处理
        res = Image.open("text.jpg", "r")
        #print(res)
        #p = subprocess.Popen(["tesseract", "text.jpg", "captcha"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #ress = pytesseract.image_to_string(res)
        try:
            ress = pytesseract.image_to_string(res)
            return ress
        except Exception as e:
            print(e)
        #print(1)
        #print(ress)
        #return ress
        #p.wait()
        #f = open("captcha.txt", "r")
        # Clean any whitespace characters
        #captchaResponse = f.read().replace(" ", "").replace("\n", "").replace("", "")

        #print("Captcha solution attempt: " + captchaResponse)
        #if (len(captchaResponse) == 4) or (len(captchaResponse) == 5):
           # return captchaResponse
        #else:
            #return False



if __name__=="__main__":

    argv=["D:/wamp/www/python/bjsw1.py","贾浩","131022198806100719","a8050980200"]
    bj=BeiJing()
    print(bj)
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    #data = parse.unquote(sys.argv[1])
    print(argv)
    bj.check(argv[1],argv[2],argv[3])

