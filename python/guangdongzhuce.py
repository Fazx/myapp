import requests
import time
import io
import sys
import random
import json
from lxml import etree
from urllib import parse

class GuangDongzhuce():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }

    def __init__(self):
        self.session=requests.session()
        self.nowtime=str(int(time.time()*1000))
        self.rtime=str(random.random())
        self.yname=str(int(random.random()*100000000000))

    def zhuce(self,username,password,phone,imagecode,code,cookies):
        res=str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}
        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')

        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
        data3={
            "yhm":username,
            "yhmm":password,
            "zjlxDm":"201",
            "zjhm":"",
            "sjh":phone,
            "verifiCode":imagecode,
            "yzm":code,
            "type":"REGIST_SJH",
            "smzz":"false"
                    }
        response=self.session.post("https://www.etax-gd.gov.cn/yhgl/service/um/user/init/egisteAccount.do",data=data3,headers=self.headers).json()
        if response["flag"]==False:
            print(response["msg"])
            return
        msg=response["msg"]
        yhid=response["yhid"]
        res=self.session.get("https://www.etax-gd.gov.cn/yhgl/service/um/user/init/twoCode2.do?yhid="+yhid,
                         headers=self.headers)
        html=etree.HTML(res.text)
        dsEwmUrl = html.xpath('.//div[@id="dsEwmUrl"]/text()')[0]
        item={}
        item["msg"]=msg
        item["dsEwmUrl"]=dsEwmUrl
        item=json.dumps(item)
        print(item)
        #self.session.get(dsEwmUrl,headers=self.headers)

if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    username=sys.argv[1]
    username=parse.unquote(username)
    password=sys.argv[2]
    phone=sys.argv[3]
    imagecode=sys.argv[4]
    code=sys.argv[5]
    cookies=sys.argv[6]
    gdz=GuangDongzhuce()
    # username="颓废的兔子11"
    # password="Aa8050980200"
    # phone="15600468476"
    # imagecode=""
    # code="213123"
    # cookies=""
    gdz.zhuce(username=username, password=password, phone=phone, imagecode=imagecode, code=code,cookies=cookies)


