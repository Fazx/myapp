import requests
import json
import os
import sys
import time
import io
import re


class Hanzhou():
    citys={
        "杭州":"330100"
    }
    session=requests.session()

    def getkey(self):
        res=self.session.get("https://www.igeshui.com/taxQuery.html",verify=False)
        apikey=re.search('apiKey=(.*?)"',res.text).group(1)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Content-Type": "application/json"
            #"Gssq-Authorization-openID": "e3a245e0dc8d4ffca807860e8de46068"
        }
        data={"apiKey":apikey,"deviceInfo":"","userId":""}
        data=json.dumps(data)
        resp=self.session.post("https://api.igeshui.com/platform/api/h5Invoking/checkH5Authorization",data=data,headers=headers,verify=False).json()
        openid=resp["openId"]
        return openid
    def login(self,name,password,openid):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Content-Type": "application/json",
            "Gssq-Authorization-openID":openid
        }
        data={"cityId":"330100","userId":""}
        data=json.dumps(data)
        res=self.session.post("https://api.igeshui.com/platform/api/taxSite/info",data=data,headers=headers,verify=False).json()
        njxh=res["orderNo"]
        data={"dIQsSGtNUOcCaNoITaZiROtHUa":"","cityId":"330100","formId":"52","loginParams":{"287":name,"288":password,"289":"code"},"iDQsSGtSEuqERNoITaZiROtHUa":njxh}
        data=json.dumps(data)
        res=self.session.post("https://api.igeshui.com/platform/api/taxSite/submitLogin",data=data,headers=headers,verify=False)
        num=0
        while True:
            data={"iDQsSGtSEuqERNoITaZiROtHUa":njxh}
            data=json.dumps(data)
            res=self.session.post("https://api.igeshui.com/platform/api/tax/allDetailH5",data=data,headers=headers).json()
            
            time.sleep(1)
            if res["code"]=="0000":
                lists=res["taxDetails"]
                for item in lists:
                    item["fname"]=name+str(item["year"])+".pdf"
                    item["name"]=res["taxPerson"]
                    item=json.dumps(item)
                    print(item)
                break
            num+=1
            if num==40:
                print("登录失败")
                break


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    name = sys.argv[1]
    password = sys.argv[2]

   # name = "43061119920906560X"
   # password = "liuxin19920810"
    hz=Hanzhou()

    openid=hz.getkey()
    hz.login(name,password,openid)



