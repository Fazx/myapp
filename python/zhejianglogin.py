import requests
import random
import re
import json
import time
import sys
import base64
import io
import os
import pytesseract
from PIL import Image,ImageOps
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from urllib import parse
class ZheJiang():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    timeArray = time.localtime(time.time())
    atime = time.strftime("%Y%m%d", timeArray)
    ntime=time.strftime("%Y-%m-%d", timeArray)
    timeArray = time.localtime(time.time())
    nowyear= int(time.strftime("%Y", timeArray))
    def __init__(self):
        self.session=requests.session()
        self.imagename=str(int(random.random()*1000000000000))
        self.rtime=str(random.random())
        self.nowtime=str(int(time.time()*1000))
    def getyanzhengma(self):

        res=self.session.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/kaptcha.jpg?v="+self.rtime,headers=self.headers,verify=False)
        with open(self.imagename+".jpg","wb") as f:
            f.write(res.content)
    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save( self.imagename+".jpg")
        image = Image.open(self.imagename+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 100)
        image = ImageOps.invert(image)
        image.save(self.imagename+".jpg")
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
    def getkey(self):
        res=self.session.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/main/util/publicKey.js?v="+self.ntime,headers=self.headers,verify=False)
        pubkey=re.search('publickey = "(.*?)"',res.text,re.S).group(1)
        return pubkey
    def check(self,code):
        #https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/Yybs/validateYzm.do?yzm=gg78
        res=self.session.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/Yybs/validateYzm.do?yzm="+code,headers=self.headers).json()
        return res["resultCode"]
        #{"resultCode":"000000","resultMsg":"验证通过","resultObj":null}
    def getmm(self,password,pubkey):
        with open(self.imagename+'.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(pubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open(self.imagename+'.txt', "r") as f:
            public_key = f.read()
            f.close()
        os.remove(self.imagename+'.txt')
        password = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(password))
        cipher_text = cipher_text.decode("utf-8")
        return cipher_text
    def login(self,username,password,pubkey,code):
        mm=self.getmm(password,pubkey)
        mm=parse.quote(mm)
        #https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/LoginController/login.do?username=18668001833&password=ajElMgks2%2BJpXRvtGkO01E%2BBdH7KhRoK3iRir9J533q7EIqM%2FV0LA%2FD2X1AjiQ%2F3u9VaLJhuL86iiTPrsHBWXayzcGFC7GBASHxh7p0dOT8TNhbA41AW8wCrfQV2f2BEXc9SNlcJEz0tMuOuG8DvDTF7UxyH2T76%2BI3lcFnrbaM%3D&service=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%2Fzjgfdzswj%2Fmain%2Fhome%2Fwdxx%2Findex.html&loginType=zhu&yzm=gg78&dxyzm=
        #https://etax.zjtax.gov.cn/zjgfdzswj/LoginController/login.do?username=18668001833&password=liuxin19920810&service=https%3A%2F%2Fetax.zjtax.gov.cn%2Fzjgfdzswj%2Fmain%2Fhome%2Fwdxx%2Findex.html&loginType=zhu&yzm=ngnx&dxyzm=
        res=self.session.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/LoginController/login.do?username="+username+"&password="+mm+"&service=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%2Fzjgfdzswj%2Fmain%2Fhome%2Fwdxx%2Findex.html&loginType=zhu&yzm="+code+"&dxyzm=",headers=self.headers).json()
        if res["resultCode"]=="100002":
            if "1" in res["resultMsg"]:
                return 101
            elif "2" in res["resultMsg"]:
                return 102
            elif "3" in res["resultMsg"]:
                return 103
            elif "4" in res["resultMsg"]:
                return 104
            else:
                return 100
        if res["resultCode"]=="999999":
            return 3
        if res["resultCode"]=="100001":
            return 600
        if res["resultCode"]!="000000":
             return 400
        #{"resultCode":"100002","resultMsg":"用户名或密码错误，您还有4次机会！","resultObj":null}
        #{'resultCode': '999999', 'resultMsg': '验证码错误', 'resultObj': None}
        #{"resultCode":"000000","resultMsg":"登陆成功","resultObj":"https://etax.zjtax.gov.cn/zjgfdzswj/main/home/wdxx/index.html?ticket=ST-288722-QESq34tgFWkhfihF4FkC-com.hz.zkxx.ydzhz"}
        url = res["resultObj"]
        if url:
            self.session.get(url,headers=self.headers,verify=False)
            res=self.session.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/UserController/getUser.do",headers=self.headers).json()
            if res["resultMsg"]:
                return res["resultMsg"]
            #{'resultCode': '000000', 'resultMsg': '', 'resultObj': {'dsInfo': {'CJXM': '刘昕', 'SJGSDQ': '23301060000', 'LYQD_DM': 'ZJDSSJQY', 'SFUUID': 'ebd1dee3bf8042159470cd7e2dda60ae', 'SFZJLX_DM': '201', 'ZLSFQQ': 'Y', 'ZRRLX_DM': '1', 'SFZJHM': '43061119920906560X', 'NSRMC': '刘昕', 'XM': '刘昕', 'LYDM': '2', 'DJXH': '20123301009001084328', 'NSRSBH': '43061119920906560X'}, 'code': 'UP', 'LRRQ': 'Dec 1, 2018 2:34:02 PM', 'USER_ID': '5e18b3492e544b5db43c2e886d67db62', 'lyqd_dm': 'ZKXX_DZSWJ_PC', 'USER_NAME': '18668001833', 'SFZJHM': '43061119920906560X', 'nsrInfo': {'NSRMC': '刘昕', 'YEAR': '2018', 'XM': '刘昕', 'DJXH': '20113300100004926070', 'SWJG_DM': '13301060000', 'SFLX': '04', 'MRBZ': 'Y', 'SFUUID': 'ebd1dee3bf8042159470cd7e2dda60ae', 'SFZJLX_DM': '201', 'NSRSBH': '43061119920906560X', 'SFZJHM': '43061119920906560X'}, 'dsList': [{'CJXM': '刘昕', 'SJGSDQ': '23301060000', 'LYQD_DM': 'ZJDSSJQY', 'SFUUID': 'ebd1dee3bf8042159470cd7e2dda60ae', 'SFZJLX_DM': '201', 'ZLSFQQ': 'Y', 'ZRRLX_DM': '1', 'SFZJHM': '43061119920906560X', 'NSRMC': '刘昕', 'XM': '刘昕', 'LYDM': '2', 'DJXH': '20123301009001084328', 'NSRSBH': '43061119920906560X'}], 'XMING': '刘昕', 'USER_TYPE': '03', 'SJHM': '18668001833', 'nsrList': [{'NSRMC': '刘昕', 'YEAR': '2018', 'XM': '刘昕', 'DJXH': '20113300100004926070', 'SWJG_DM': '13301060000', 'SFLX': '04', 'MRBZ': 'Y', 'SFUUID': 'ebd1dee3bf8042159470cd7e2dda60ae', 'SFZJLX_DM': '201', 'NSRSBH': '43061119920906560X', 'SFZJHM': '43061119920906560X'}]}}
            uname=res["resultObj"]["XMING"]
            self.session.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/cysx/queryCysx.do",headers=self.headers)
            return uname
        return 500

    def detail(self,uname):
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        for i in range(2006,self.nowyear+1):
            res=self.session.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/main/pubutil.js?v="+self.atime+"&_="+self.nowtime,headers=self.headers)
            appid=re.search('appId=(.*?)&',res.text).group(1)
            #{"tid":"","ctrl":"/zjgfcssdzswjzs/zsgrsdswszmctrl/cxGrsdsxx.do","data":[{"name":"cxtj","value":"1","sword":"attr"},{"name":"rqq","value":"2019-01-01","sword":"attr"},{"name":"rqz","value":"2019-01-09","sword":"attr"},{"name":"xzqh","value":"330000","sword":"attr"}],"bindParam":true}
            data={
                "postData":'{"tid":"","ctrl":"/zjgfcssdzswjzs/zsgrsdswszmctrl/cxGrsdsxx.do","data":[{"name":"cxtj","value":"1","sword":"attr"},{"name":"rqq","value":"'+str(i)+'-01-01","sword":"attr"},{"name":"rqz","value":"'+str(i)+'-12-31","sword":"attr"},{"name":"xzqh","value":"'+appid+'","sword":"attr"}],"bindParam":true}'
            }
            #{"tid":"","ctrl":"/zjgfcssdzswjzs/zsgrsdswszmctrl/cxGrsdsxx.do","data":[{"name":"cxtj","value":"1","sword":"attr"},{"name":"rqq","value":"2018-01-01","sword":"attr"},{"name":"rqz","value":"2018-12-01","sword":"attr"},{"name":"xzqh","value":"330000","sword":"attr"}],"bindParam":true}
            res=self.session.post("https://etax.zhejiang.chinatax.gov.cn/zjgfcssdzswjzs/zsgrsdswszmctrl/cxGrsdsxx.do?1=1",data=data,headers=headers).json()
            shujus=json.loads(res["jsonresult"])
            if shujus["data"][0]["name"]=="ccsTable":
                shuju=shujus["data"][0]["trs"]
                res=self.session.get(" https://etax.zhejiang.chinatax.gov.cn/zjgfcssdzswjzs/zsgrsdswszmctrl/wszmKj/"+str(i)+"-01-01/"+str(i)+"-12-31/1/1/1/"+appid+".do")
                fname=str(i)+self.imagename+".pdf"
                with open("/home/wwwroot/wbsr/python/files/"+fname,"wb") as f:
                    f.write(res.content)
                item={}
                item["years"]=str(i)
                item["name"]=uname
                item["fname"]=fname
                item["lists"]=shuju
                item=json.dumps(item)
                print(item)





if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    username=sys.argv[1]
    password=sys.argv[2]
    # username="18668001833"
    # password="liuxin19920810"
    # username="13968268262"
    # password="963708aabb"
    try:
        zj=ZheJiang()
        pubkey=zj.getkey()
        num=0
        while True:
            zj.getyanzhengma()
            code=zj.readcode(zj.imagename+".jpg")
            res=zj.check(code)
            if res=="000000":
                os.remove(zj.imagename+".jpg")
                break
            if num == 5:
                os.remove(zj.imagename + ".jpg")
                break
            num+=1
            os.remove(zj.imagename + ".jpg")
        uname=zj.login(username,password,pubkey,code)
        if uname==3:
            print(3)
        elif uname==100:
            print(100)
        elif uname==101:
            print(101)
        elif uname==102:
            print(102)
        elif uname==103:
            print(103)
        elif uname==104:
            print(104)
        elif uname==400:
            print(400)
        elif uname == 600:
            print(600)
        elif uname==500:
            print(500)
        elif uname:
            zj.detail(uname)
        else:
            print(500)
    except Exception as e:
        print(e)

