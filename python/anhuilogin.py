import requests
import re
import time
import hashlib
import json
import random
import sys
import io
from urllib import parse

class AnHui():

    session=requests.session()
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    nowtime=str(int(time.time()*1000))
    pname=str(int(random.random()*100000000000000))
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))
    def getindex(self):
        res=self.session.get("http://etax.ah-n-tax.gov.cn/cas/login",headers=self.headers)
        html=res.text
        lt=re.search('name="lt" value="(.*?)"',html).group(1)
        execution=re.search('name="execution" value="(.*?)"',html).group(1)

        return lt,execution
    def getyzm(self):

        res=self.session.post("http://etax.ah-n-tax.gov.cn/cas/yzmToken?r="+self.nowtime).json()

        return res["token"]

    def md5password(self,password):
        m=hashlib.md5()
        m.update(password.encode())
        mm=m.hexdigest()
        return mm

    def login(self,name,password,lt,execution,token):
        data={
            "username":name,
            "password":password,
            "usertype":"zrr",
            "lt":lt,
            "execution":execution,
            "_eventId":"submit",
            "yzmtoken":token
        }

        res=self.session.post("http://etax.ah-n-tax.gov.cn/cas/login",data=data,headers=self.headers,verify=False)
        if "您的密码已输错" in res.text:
            return "300"
        if "未注册户" in res.text:
            return "100"
        uname=re.search('class="username" title="(.*?)">',res.text)
        if uname:
            return uname
        return
    def detail(self,uname):
        self.session.get("http://etax.ah-n-tax.gov.cn/gx/sswszmkj/getgsList?0.03434020498170631",headers=self.headers)
        #print(res.text)
        for i in range(2006,self.atime+1):
            data={
                "kjlb":"ds_zrr",
                "kjms":"mxkj",
                "skssqq":str(i)+"/01/01",
                "skssqz":str(i)+"/12/31",
                "kpsjq":"",
                "kpsjz":"",
                "skkjfw":"",
                "skkjfwdm":""
            }

            res=self.session.post("http://etax.ah-n-tax.gov.cn/gx/sswszmkj/getGrsListByConditions",data=data,headers=self.headers).json()
            if res["data"]:
                lists=res["data"]
                swjgdm=res["data"][0]["swjgdm"]
                data=lists
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
                }
                data=json.dumps(data)
                res=self.session.post("http://etax.ah-n-tax.gov.cn/gx/sswszmkj/addYkj?kjms=mxkj&gdsbz=ds_zrr&skkjfwdm="+str(swjgdm),data=data,headers=headers).json()
                id=res["data"]["id"]
                nsrsbh=res["data"]["nsrsbh"]
                skfwdm=res["data"]["swjgDm"]
                data1={
                    "id":id,
                    "formName":"YkjwszmMxds",
                    "printName":"YkjwszmMxds",
                    "nsrsbh":nsrsbh,
                    "gdsbz":"ds_zrr",
                    "skfwdm":skfwdm
                }
                resp=self.session.get("http://etax.ah-n-tax.gov.cn/print/reportServlet3",params=data1,headers=self.headers)
                fname=str(i)+self.pname+".pdf"
                with open("/home/wwwroot/wbsr/python/files/" + fname, "wb") as f:
                # with open(str(i)+self.pname+".pdf","wb") as f:
                    f.write(resp.content)
                    f.close()
                item={}
                item["year"]=str(i)
                item["name"]=uname
                item["fname"]=fname
                item["lists"]=lists
                item=json.dumps(item)
                print(item)

       





if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    name=sys.argv[1]
    password=sys.argv[2]
    # password="wj19910528"
    # name="341021199105284209"
    # password="a123456789"
    # name="34040419691108021X"

    try:
        ah=AnHui()
        index=ah.getindex()
        token=ah.getyzm()
        mm=ah.md5password(password)
        uname=ah.login(name,mm,index[0],index[1],token)
        if uname=="100":
            print(100)
        elif uname=="300":
            print(300)
        elif uname:
            uname=uname.group(1)
            ah.detail(uname)
        else:
            print(400)
    except Exception as e:
        print(500)
