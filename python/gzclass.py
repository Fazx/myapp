import requests
import pytesseract
import re
import time
import sys
import os
import io
import threading
import json
from urllib import parse
from PIL import ImageOps,Image

class GuangZhou():
    times=str(int(time.time()*1000))
    def __init__(self):
        self.session = requests.session()

    def getyzm(self):
        yzm=self.session.get("http://mtax.gdltax.gov.cn/appserver/security/binduser/captcha.do?t="+self.times)
        with open("/home/wwwroot/wbsr/python/images/"+self.times+".jpg","wb") as f:
            f.write(yzm.content)

    def cleanImage(self,imagePath):
        image = Image.open(imagePath)
        image = image.point(lambda x: 0 if x<143 else 255)  #对像素点处理
        borderImage = ImageOps.expand(image,border=20,fill='white') #图片延伸
        borderImage.save(imagePath)

    def readcode(self,path):
        self.cleanImage(path)
        image=Image.open(path)
        code=pytesseract.image_to_string(image)
        code=code.replace(" ","")[0:4]
        return code

    def login(self,phone,password,code):

        accountInfoStr='{"phonenum":"'+phone+'","password":"'+password+'","yzm":"'+code+'"}'
        accountInfoStr=parse.quote(str(accountInfoStr).encode("utf-8"))
        resp=self.session.get("http://mtax.gdltax.gov.cn/appserver/security/user/tpLogin.do?accountInfoStr="+accountInfoStr+"&callback=jsonp_callback3&time="+self.times+"&timeOut=100000")
        return resp.text
    def sessionid(self):
        respon=self.session.get("http://mtax.gdltax.gov.cn/appserver/security/binduser/getWebAppUserDetails.do?callback=jsonp_callback4&time="+self.times+"&timeOut=20000")
        html=respon.text
        ress=re.search('"sessionId":"(.*?)"',html)
        sessionid=ress.group(1)
        return sessionid

    def djxh(self):
        response=self.session.get("http://mtax.gdltax.gov.cn/appserver/dzsp/getGrDjxhandNsrsbh.do?callback=jsonp_callback3&time="+self.times+"&timeOut=30000")
        res=re.search('"djxh":"(.*?)".*?"xm":"(.*?)"',response.text)
        
        return res

    def detil(self,djxh,sessionid,name):
        timeArray = time.localtime(time.time())
        times = int(time.strftime("%Y", timeArray))
        for i in range(2006,times+1):
            ress=self.session.get("http://mtax.gdltax.gov.cn/appserver/dzsp/getGrsdsqdxx.do?djxh="+djxh+"&startdate="+str(i)+"-01-01&enddate="+str(i)+"-12-31&ignore=true&yzm=&callback=jsonp_callback4&time="+self.times+"&timeOut=20000")
            if "dataList" in ress.text:
                shuju=re.search('"dataList":(.*?),"flag":"ok"',ress.text)
                datalist=shuju.group(1)
                rkrq=re.search('"rkrq":"(.*?)",',datalist)
                fname=""
                if rkrq.group(1):
                    text=self.session.get("http://mtax.gdltax.gov.cn/appserver/dzsp/getGrsdszmPDF.do?startdate="+str(i)+"-01-1&enddate="+str(i)+"-12-31&djxh="+djxh+"&loadSessionId="+sessionid+""+self.times+"&time="+self.times+"&timeOut=30000")
                    fname=str(djxh)+str(i)+".pdf"
                    with open("/home/wwwroot/wbsr/python/files/"+str(djxh)+str(i)+".pdf",'wb') as f:
                        f.write(text.content)
                item={}
                item["name"]=name
                item["year"]=str(i)
                item["fname"]=fname
                item["lists"]=datalist
                item=json.dumps(item)
                print(item)

if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # print(sys.argv)
    # data1 = parse.unquote(sys.argv[1])
    # data2 = parse.unquote(sys.argv[2])

    phone=sys.argv[1]
    password=sys.argv[2]
   # phone="15899978911"
   # password="Zhaoxiuli830924"
    gz=GuangZhou()
    num=1
    while True:
        gz.getyzm()
        yzm=gz.readcode("/home/wwwroot/wbsr/python/images/"+gz.times+".jpg")
        massage=gz.login(phone,password,yzm)
        if "ok" in massage:
            os.remove("/home/wwwroot/wbsr/python/images/"+gz.times+".jpg")
            break
        if "密码错误" in massage:
            print(1)
            os.remove("/home/wwwroot/wbsr/python/images/" + gz.times + ".jpg")
            break
        if "手机号尚未注册" in massage:
            print(2)
            os.remove("/home/wwwroot/wbsr/python/images/" + gz.times + ".jpg")
            break
        if num==6:

            print(3)
            break
        num+=1
    try:
        sessionid=gz.sessionid()
        sj=gz.djxh()
        if sj:
            djxh=sj.group(1)
            name=sj.group(2)
        
            
            gz.detil(djxh,sessionid,name)
        else:
            print(4)
    except Exception as e:
        print(0)

