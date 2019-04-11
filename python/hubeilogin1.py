import requests
import io
import sys
import random
import json
import re
import base64
import time
import pytesseract
from PIL import Image,ImageOps


class HuBei():

    session=requests.session()
    nowtime = str(int(time.time() * 1000))
    #ntime = str(int(random.random() * 100000000000000))
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }


    def __init__(self):
        self.ntime=str(int(random.random() * 100000000000000))
        timeArray = time.localtime(time.time())
        self.atime = int(time.strftime("%Y", timeArray))

    def index(self):
        res=self.session.get("https://wsswj.hb-n-tax.gov.cn/portal/",headers=self.headers,verify=False)
        csrf=re.search('var csrfPreventionSalt = "(.*?)"',res.text).group(1)
        self.session.post("https://wsswj.hb-n-tax.gov.cn/portal/tzgg/loadTips.c",headers=self.headers,verify=False).json()
        return csrf
    def getyzm(self,csrf):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "X-CSRF-Token": csrf,
            "c-token": csrf
        }
        res=self.session.post("https://wsswj.hb-n-tax.gov.cn/portal/vCode.c",headers=headers,verify=False).json()
        image=res["repData"]["image"]

        with open(self.ntime+".jpg","wb") as f:
            f.write(base64.b64decode(image))

    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save(self.ntime+".jpg")
        image = Image.open(self.ntime+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 115)
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
        x_s = 100  # define standard width
        y_s = 40  # calc height based on standard width
        out = image.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
        out.save(path)
        out.show()
        code = pytesseract.image_to_string(out).replace(" ", "").replace("\\", "")[0:4]
        return code
    def login(self,csrf,username,password,code,cookies):
        if cookies=="0":
            print("请输入信息")
            return
        res=str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}

        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "X-CSRF-Token": csrf,
            "c-token": csrf,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json;charset=UTF-8"

        }

        data={"handleCode":"login","reqData":{"username":username,"password":password,"vcode":code}}
        data=json.dumps(data)
        res=self.session.post("https://wsswj.hb-n-tax.gov.cn/portal/login.c",data=data,headers=headers,verify=False).json()
        if not res["msg"]:
            result=res["repData"]["user"]["xm"]
            self.session.get("https://wsswj.hb-n-tax.gov.cn/portal/home.c", headers=self.headers)
            self.session.get("https://wsswj.hb-n-tax.gov.cn/zyy-cxfw/dzswj/tycx/zctx/ZCTX.jsp",headers=self.headers)
            self.session.post("https://wsswj.hb-n-tax.gov.cn/portal/checkLoginState.c?gnmkDm=14000",headers=headers)
            self.session.get("https://wsswj.hb-n-tax.gov.cn/portal/iframe.c?title=%E7%A8%8E%E6%94%B6%E5%AE%8C%E7%A8%8E%E8%AF%81%E6%98%8E%E5%BC%80%E5%85%B7%EF%BC%88%E4%B8%AA%E4%BA%BA%EF%BC%89&goUrl=/webroot/wlsb/wszm/grwszm.html",headers=self.headers)
            return result
        if "密码错误次数超过上限" in res["msg"]:
            return 400
        if "验证码错误" in res["msg"]:
            return 300
        if "密码错误" in res["msg"]:
            return 100
        return
        #print(res.text)
        #{"code":"03","msg":"","repData":{"user":{"id":
        #密码错误，剩余9次后将会被锁定
        #"{\"handleCode\":\"login\",\"reqData\":{\"username\":feifei854307482,\"password\":\":feifei854307482\",\"vcode\":\"vghc\"}}"
        #{"handleCode":"login","reqData":{"username":"1232143214324","password":"12312321","vcode":"6dgr"}}
        #{"code":"W1067","msg":"验证码错误","repData":{}}
        #{"code":"E9007","msg":"无法正确读取数据","repData":{}}
    def detail(self,result):
        self.session.get("https://wsswj.hb-n-tax.gov.cn/webroot/wlsb/wszm/grwszm.html",headers=self.headers,verify=False)
        self.session.get("https://wsswj.hb-n-tax.gov.cn/webroot/spark/js/spark-prototype.js",headers=self.headers)
        self.session.get("https://wsswj.hb-n-tax.gov.cn/webroot/spark/js/spark-ui.js",headers=self.headers)
        self.session.get("https://wsswj.hb-n-tax.gov.cn/webroot/spark/js/spark-ui-ext.js",headers=self.headers)

        headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        #"Referer": "https://wsswj.hb-n-tax.gov.cn/webroot/wlsb/wszm/grwszm.html",
        #"Host": "wsswj.hb-n-tax.gov.cn",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/plain, */*; q=0.01",
        "Origin": "https://wsswj.hb-n-tax.gov.cn",
        "Referer": "https://wsswj.hb-n-tax.gov.cn/webroot/wlsb/wszm/grwszm.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"}
        #"Cookie": "BIGipServerpool_dzshwj_http=2976164032.17183.0000; JSESSIONID=o_H4NJyj68N1W2bBlBT4-CHxmSmvbfamXta77kqLbx5rXZzTiTRh!-1199858257; PORTAL-TGC=C0B6E9EAAD2443EF8D4DD3436BE18B95; WSBSSESSIONID_161=cen4vMWhSLdCWXWukP2uxraM64ujEMK_J3ffFZUvq0mpqOrXDxww!-758646788"}
        #"Cookie": "BIGipServerpool_dzshwj_http=2976164032.17183.0000; JSESSIONID=o_H4NJyj68N1W2bBlBT4-CHxmSmvbfamXta77kqLbx5rXZzTiTRh!-1199858257; PORTAL-TGC=C0B6E9EAAD2443EF8D4DD3436BE18B95; WSBSSESSIONID_161=cen4vMWhSLdCWXWukP2uxraM64ujEMK_J3ffFZUvq0mpqOrXDxww!-758646788"        }
        #{"pageContext": {}, "data": "{}"}
        data={"pageContext":{},"data":"{}"}
        data=json.dumps(data)
        data=data.replace(" ","")
        resp=self.session.post("https://wsswj.hb-n-tax.gov.cn/webroot/com/neusoft/tax/wlsb/wszm/WszmList.smzCheck.svc",
                              data=data, headers=headers)
        for i in range(2014,self.atime+1):
            data={"pageContext":{},"data":'{"ssqq":"'+str(i)+'-01-01","ssqz":"'+str(i)+'-12-31","queryflag":"gs"}'}
            data=json.dumps(data)
            res=self.session.post("https://wsswj.hb-n-tax.gov.cn/webroot/com/neusoft/tax/wlsb/wszm/WszmList.initMX.svc",data=data,headers=headers,verify=False)
            data={"pageContext":{},"data":'{"queryflag":"gs","ssqq":"'+str(i)+'-01-01","ssqz":"'+str(i)+'-12-31","pageInfo":{"begin":1,"end":19,"pageDataName":"jkswszListData","sortMap":{}}}'}
            data=json.dumps(data)
            resp=self.session.post("https://wsswj.hb-n-tax.gov.cn/webroot/com/neusoft/tax/wlsb/wszm/JkdtxxList.execute.svc",data=data,headers=headers,verify=False).json()
            if resp["data"]:
                shuju=resp["data"]["jkswszListData"]
                item={}
                item["name"]=result
                item["years"]=str(i)
                item["fanme"]=""
                item["lists"]=shuju
                item=json.dumps(item)
                print(item)


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # 300 验证码错误
    # 100 密码错误
    # 400 账号被锁
    # 600 未知错误
    # 500 脚本错误
    username=sys.argv[1]
    password=sys.argv[2]
    csrf=sys.argv[3]
    code=sys.argv[4]
    cookies=sys.argv[5]
    # username="xly123400"
    # password="1989Xly00"
    # csrf=""
    # cookies=""
    # code=""
    try:
        hb = HuBei()
        result=hb.login(csrf,username,password,code,cookies)
        if result == 100:
            print(100)
        elif result==300:
            print(300)
        elif result==400:
            print(400)
        elif result:
            hb.detail(result)
        else:
            print(600)
    except Exception as e:
        print(500)

