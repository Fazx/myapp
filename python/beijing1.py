# coding:utf-8
import requests
import time
import logging
import sys
import importlib
import os
import random
import stat
import json
import threading
import io
import importlib
import subprocess
import pytesseract
from urllib import parse
from PIL import Image
from PIL import ImageOps

class BeiJing():

    session=requests.session()
    session.headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    ctime=str(int(time.time()*1000))
    pname = str(int(random.random() * 1000000000000)) + ".jpg"
    def __init__(self):
        pass

    def login(self,sfz,name,card,password):

        respon=self.session.get("http://yidong.tax861.gov.cn/bsfw/gscx.htm")
        res=self.session.get("http://yidong.tax861.gov.cn/random.do?d="+self.ctime)
        with open('/home/wwwroot/wbsr/python/images/'+self.pname, 'wb') as f:
            f.write(res.content)
            os.chmod('/home/wwwroot/wbsr/python/images/'+self.pname, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        code=self.getAuthCode('/home/wwwroot/wbsr/python/images/'+self.pname)
        data={
           "idCardtype":sfz,
            "idCardno":card,
            "name":name,
            "password":password,
           "code":code
        }
        if os.path.exists('/home/wwwroot/wbsr/python/images/'+self.pname):
            os.remove('/home/wwwroot/wbsr/python/images/'+self.pname)
        #if os.path.exists("captcha.txt"):
            #os.remove("captcha.txt")S
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


    def check(self,sfz,name,card,password):
        resp=self.login(sfz,name,card,password)
        if resp=="证照类型、号码不存在或密码错误" or resp=="验证码错误":
            print(resp)
            return
        datass=[]
        for year in resp:
            year=year["year"]
          
            datas={
                "taxYear":year
            }
            datass.append(datas)
        return datass
            # res=self.session.post("http://yidong.tax861.gov.cn/gscx.do?d="+self.ctime,data=datas).json()
            # detail.append(res)
            # detail=json.dumps(detail)
            # print(detail)
            #lists=res["mxsbList"]
            # print(lists)
            #
            # if lists:
            #     for result in lists:
            #         name=result["name"]
            #         income=result["income"]
            #         nsrmc=result["nsrmc"]
            #         taxmonth=result["taxmonth"]
            #         taxyear=result["taxyear"]
            #         taxactual=result["taxactual"]
            #         #print(name,income,nsrmc,taxmonth,taxyear,taxactual)
            # #else:
            #     #print(year+"无纳税信息")

    def cleanImage(self,imagePath):
        image = Image.open(imagePath)  # 读取文件
        image = image.point(lambda x: 0 if x<143 else 255)  #对像素点处理
        borderImage = ImageOps.expand(image,border=20,fill='white') #图片延伸
        borderImage.save(imagePath) #保存

    def getAuthCode(self,file, driver="a", url="b"):

        self.cleanImage('/home/wwwroot/wbsr/python/images/'+self.pname)  # 图片处理
        res = Image.open('/home/wwwroot/wbsr/python/images/'+self.pname, "r")
        try:
            ress = pytesseract.image_to_string(res)
            return ress
        except Exception as e:
            print(e)


if __name__=="__main__":


    try:

        bj=BeiJing()
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        #print(sys.argv)
        data1 = parse.unquote(sys.argv[1])
        data2 = parse.unquote(sys.argv[2])
        #print(sys.argv[1].encode("utf-8"))
        #print(data1)
        ss=bj.check(data1,data2,sys.argv[3],sys.argv[4])


        def detail(datas):
            detail = list()
            res = bj.session.post("http://yidong.tax861.gov.cn/gscx.do?d=" + bj.ctime, data=datas).json()
            detail.append(res)
            detail = json.dumps(detail)
            print(detail)
        for i in range(len(ss)):
            t = threading.Thread(target=detail, args=(ss.pop(),))
            t.start()
            t.join()


    except Exception as e:
        print(e)






