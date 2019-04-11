# -*-coding:utf-8-*-
import requests
import re
import json
import sys
import io
import hashlib
from urllib import parse

class BeiJingzhuce():
    headers={

        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",

    }
    cardtypes={
        "居民身份证":"201",
        "军官证":"202",
        "武警警官证":"203",
        "士兵证":"204",
        "外国护照":"208",
        "港澳居民来往内地通行证":"210",
        "台湾居民来往大陆通行证":"213",
        "香港身份证":"219",
        "台湾身份证":"220",
        "澳门身份证":"221",
        "中国护照":"227",
        "外国人永久居留证":"233"
    }
    def __init__(self):
        self.session = requests.session()

    def yanzheng(self,cardtype,card,username,phone):
        res=self.session.get("http://yidong.tax861.gov.cn/bsfw/gscx.htm",headers=self.headers)
        res.encoding="utf-8"
        data='<ClientMsg><RequestAction Type="com.lscdz.grsds.application.yhgl.handler.YhglHandler" Action="doQueryZrrxx" Privilege="" /><xm>'+username+'</xm><sfzjlx>'+self.cardtypes[cardtype]+'</sfzjlx><sfzjhm>'+card+'</sfzjhm></ClientMsg>'
        resp=self.session.get("https://gt3sfhz.tax861.gov.cn/Gt3Gszxnssb/gsrzwx/nocheck/register.html?actionLoginType=0",headers=self.headers)
        data1='<ClientMsg><RequestAction Type="com.lscdz.grsds.application.yhgl.handler.YhglHandler" Action="Init" Privilege="" /></ClientMsg>'#130705198912281569
        resp=self.session.post("https://gt3sfhz.tax861.gov.cn/Gt3Gszxnssb/ClientActionServlet",data=data1,headers=self.headers)
        res=self.session.post("https://gt3sfhz.tax861.gov.cn/Gt3Gszxnssb/ClientActionServlet",data=data.encode("utf-8"),headers=self.headers)

        djxh=re.search('<Djxh>',res.text)
        id=re.search('<Id>',res.text)
        if id:
            print("该用户已注册")
            return
        if not djxh:
            # print(djxh)
            print("姓名、证件号错误")
            return
        data2='<ClientMsg><RequestAction Type="com.lscdz.grsds.application.sfxxhz.handler.SkhzHandler" Action="init" Privilege="" /></ClientMsg>'
        res=self.session.post('https://gt3sfhz.tax861.gov.cn/Gt3Gszxnssb/ClientActionServlet',data=data2,headers=self.headers)
        data3='<ClientMsg><RequestAction Type="com.lscdz.ylrz.sfhz.handler.YlrzHandler" Action="sendms" Privilege="" /><phoneNo>'+phone+'</phoneNo></ClientMsg>'
        res=self.session.post('https://gt3sfhz.tax861.gov.cn/Gt3Gszxnssb/ClientActionServlet',data=data3,headers=self.headers)
        times=re.findall(r'\[(\d+)\]',res.text)
        if times:
            item={}
            item["cookies"]=str(self.session.cookies.get_dict())
            item["time0"]=times[0]
            item["time1"]=times[1]
            item["time2"]=times[2]
            item=json.dumps(item)
            print(item)

        else:
            print("验证码验证频繁或达到最大次数")




if __name__=="__main__":
    # sys.argv = ["D:/wamp/www/python/bjsw1.py", "居民身份证", "43061119920906560X", "刘昕","156004611001"]

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cardtype=sys.argv[1]
    cardtype = parse.unquote(cardtype)
    card=sys.argv[2]
    username=sys.argv[3]
    username=parse.unquote(username)
    phone=sys.argv[4]
    # cardtype="居民身份证"
    # card="43061119920906560X"#43061119920906560X
    # username="刘昕"
    # phone="156004611001"


    bjz=BeiJingzhuce()
    bjz.yanzheng(cardtype=cardtype,card=card,username=username,phone=phone)


