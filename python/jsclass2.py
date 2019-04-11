import requests
import pytesseract
import re
import json
import os
import io
import sys
import time
import math
import base64
from urllib import parse
from PIL import Image

class JiangSu():
    cardtypes={"武警警官证": "31",
     "士兵证": "32",
     "军队离退休干部证": "33",
     "残疾人证": "34",
     "残疾军人证（1-8级）": "35",
     "就业失业登记证": "36",
     "城镇退役士兵自谋职业证": "37",
     "就业创业证": "38",
     "退休证": "39",
     "离休证": "40",
     "医学出生证明": "42",
     "其他个人证件": "43",
     "中国护照": "49",
     "港澳居民来往内地通行证": "51",
     "中华人民共和国往来港澳通行证": "52",
     "外国人居留证": "53",
     "外交官证": "54",
     "领事馆证": "55",
     "海员证": "56",
     "香港身份证": "57",
     "台湾身份证": "58",
     "外国人身份证件": "59",
     "其他单位证件": "91",
     "税务登记证": "92",
     "居民身份证（澳门）": "20",
     "永久性居民身份证": "19",
     "营业执照": "11",
     "台湾居民来往大陆通行证": "22",
     "护照": "01",
     "通行证": "02",
     "身份证": "06",
     "军官证": "07",
     "全国组织机构统一代码证": "80"}
    session=requests.session()
    nowtime=str(int(time.time()*1000))
    ntime = str(int(time.time() * 1000000))
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    def getyzm(self):
        self.session.get("http://www.jsds.gov.cn/index/portal/login.html?xtlx=zrr",headers=self.headers)
        res=self.session.get("http://www.jsds.gov.cn/index/portal/yzm.jsp?xx=0.8748369770096547",headers=self.headers)
        with open(self.ntime+".jpg","wb") as f:
            f.write(res.content)
    def rodecode(self,path):
        image=Image.open(path)
        code=pytesseract.image_to_string(image)
        return code
    def login(self,username,password,code):

        data={
            'jsonData':'{"handleCode":"loginByJsswSjmm","data":{"appId":"201706281026","sjhm":"'+username+'","yhmm":"'+password
                       +'","yzm":"'+code+'"}}'
        }
        res=self.session.post("https://zrrbs.jsds.gov.cn/Zrr/DlAction.do",data=data,headers=self.headers,verify=False)
        #{"handleCode":"loginBySjmm","data":{"telphone":"17396805504","yhmm":"778010A2","yzm":"4661","dlIp":"","dlDz":""}}
        #{"handleCode":"loginBySjmm","data":{"telphone":"17396805504","yhmm":"778010A2","yzm":"0960","dlIp":"","dlDz":""}}
        data["callback"]="jQuery111103629389960867504_"+self.nowtime
        data["_"]=self.nowtime
        res=self.session.get("http://zrrbs.jsds.gov.cn/Zrr/DlAction.do",headers=self.headers,params=data,verify=False)
        msg=re.search('"msg":"(.*?)"}',res.text).group(1)
        if msg !="登录成功":
            return
        name=re.search('"xm":"(.*?)"',res.text).group(1)
        zjHm=re.search('"zjHm":"(.*?)"',res.text).group(1)
        token=re.search('"access_token":"(.*?)"',res.text).group(1)
        data={
            'Code':'zjhmtoHome',
            'data':'{"zjhm":"'+zjHm+'","sjhm":"","token":"'+token+'","appId":"201706281026","code":"0","mesg":"登录成功"}'
        }
        self.session.get("http://zrrbs.jsds.gov.cn/Zrr/DlAction.do",params=data,verify=False)
        data={
            'jsonData':'{"handleCode":"getUserDjXh","blhName":"CommBLH","data":{}}'
        }
        resp=self.session.post('https://zrrbs.jsds.gov.cn/Zrr/GeneralAction.do',data=data,verify=False).json()

        djxh=resp["data"]["djxh"]

        for i in range(2006,self.atime+1):
            data = {
                'jsonData': '{"blhName":"DzpzBLH","handleCode":"getDzpzDyBwxx","data":{"ssqq":"'+str(i)+'-01-01","ssqz":"'+str(i)+'-12-31","rtkrqq":"","rtkrqz":"","zsxm":"10106","zspm":["101060100"],"cxlx":"","pzxh":"","djxh":"'+djxh+'"}}'
                #{"handleCode":"loginByJsswSjmm","data":{"appId":"201706281026","sjhm":"17396805504","yhmm":"17396805504","yzm":"3878"}}
            }
            res = self.session.post("http://zrrbs.jsds.gov.cn/Zrr/DzpzAction.do", data=data,
                                    verify=False).json()
            if res["code"]=='0':
                datas = res["data"]["rtnList"]
                num=0
                for j in datas:
                    jj=j["sjje"]
                    num+=float(jj)
                num=str(round(num,2))

                data = {
                    'jsonData': '{"blhName":"DzpzBLH","handleCode":"showPdf","data":{"rtnList":' + str(
                        datas) + ',"djxh":"'+djxh+'","ssqq":"'+str(i)+'-01-01","ssqz":"'+str(i)+'-12-31","skssqs":"'+str(i)+'-01-01","skssqz":"'+str(i)+'-12-31","kkrqq":"","kkrqz":"","zsxm":"10106","zspm":["101060100"],"cxbj":"","skhj":"'+num+'"}}'
                }

                res = self.session.post('http://zrrbs.jsds.gov.cn/Zrr/DzpzAction.do', data=data,
                                        verify=False).json()
                lsh=res["data"]["bizkey_dy"]

                data = {
                    'jsonData': '{"handleCode":"filedownload","downLoadFile":"1","data":{"lsh":"'+lsh+'","uuid":"'+lsh+'"}}'
                }
                res = self.session.post("http://zrrbs.jsds.gov.cn/Zrr/FiledownloadAction.do", data=data,
                                         verify=False).json()
                url = res["data"]["srcUrl"]
                res = base64.b64decode(url)
                fname=str(i)+djxh+".pdf"
                with open("/home/wwwroot/wbsr/python/files/" + str(i)+djxh+".pdf", "wb") as f:
                    f.write(res)
                item={}
                item["name"]=name
                item["fname"]=fname
                item["year"]=str(i)
                item["lists"]=datas
                item=json.dumps(item)
                print(item)

if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # username="17396805504"
    # password="778010A2"

    username=sys.argv[1]
    password=sys.argv[2]
    js=JiangSu()
    js.getyzm()
    code=js.rodecode(js.ntime+".jpg")
    os.remove(js.ntime+".jpg")
    js.login(username,password,code)


