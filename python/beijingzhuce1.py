# -*-coding:utf-8-*-
import requests
import re
import json
import sys
import io
import hashlib
from urllib import parse

class BeiJingzhuce1():
    headers={

        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",

    }
    def __init__(self):
        self.session = requests.session()


    def zhuce(self,card,username,phone,password,yinhangcard,code,cookies,time0,time1,time2):
        if cookies == "0":
            print("请获取短信验证码")
            return
        res=str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}
        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')

        # print(item1)
        # requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
        # print(self.session.cookies.get_dict())
        m2 = hashlib.md5()
        m2.update(password.encode("utf-8"))
        mm=m2.hexdigest()
        data4='<ClientMsg><RequestAction Type="com.lscdz.ylrz.sfhz.handler.YlrzHandler" Action="sfhz" Privilege="" /><cardNo>'+yinhangcard+'</cardNo><phoneNo>'+phone+'</phoneNo><smsCode>'+code+'</smsCode><rzlx>'+time2+'</rzlx><customerNm>'+username+'</customerNm><certifId>'+card+'</certifId><rzmm>'+mm+'</rzmm><dataSource>30</dataSource><rzfsdm>04</rzfsdm><lxdh>'+phone+'</lxdh><orderId>'+time0+'</orderId><txnTime>'+time1+'</txnTime></ClientMsg>'
        #print(data4)
        res=self.session.post("https://gt3sfhz.tax861.gov.cn/Gt3Gszxnssb/ClientActionServlet",data=data4.encode("utf-8"),headers=self.headers)
        massage=re.search('<Message>(.*?)</Message>',res.text).group(1)
        if '用户注册成功' in massage:
            print("注册成功")
        else:
            print(massage.replace("<![CDATA[","").replace("]]>",""))



if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # print(sys.argv)
    card=sys.argv[1]
    username=sys.argv[2]
    username=parse.unquote(username)
    phone=sys.argv[3]
    password=sys.argv[4]
    code=sys.argv[5]
    yinhangcard=sys.argv[6]
    cookies=sys.argv[7]
    time0=sys.argv[8]
    time1=sys.argv[9]
    time2=sys.argv[10]
    bjz=BeiJingzhuce1()
    # card="43061119920906560X"
    # username="刘昕"
    # phone="15600461100"
    # password = "a8050980200"
    # code="·"
    # yinhangcard="6228481000884523118"
    # cookies="{'JSESSIONID': 'B696A6071FFF340946D2C5D1A5C19EA5', 'BIGipServerwx_pool': '1593901322.22811.0000'}"
    # time0="20181113125721576"
    # time1="20181113125721"
    # time2="00"
    bjz.zhuce(card=card,username=username,phone=phone,password=password,yinhangcard=yinhangcard,code=code,cookies=cookies,time0=time0,time1=time1,time2=time2)

