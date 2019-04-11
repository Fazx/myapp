import requests
import pytesseract
import os
import sys
import io
import random
from urllib import parse

class AnHuizhuce():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    def __init__(self):
        self.ntime=str(int(random.random()*1000000000000))
        self.session=requests.session()
        self.rnum1=str(random.random())
        self.rnum2=str(random.random()*1000)
        self.rnum3 = str(random.random() * 100)
    def zhuce(self,idnum,name,password,phone,phonecode,uuid,cookies):

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
        data={
            "zclxdm":"zrr",
            "uuid":uuid,
            "zclxmc":"自然人注册",
            "yzlxdm":"jmsfz",
            "yzlxmc":"居民身份证",
            "nsrsbh":idnum,
            "nsrmc":name,
            "pwd":password,
            "qrpwd":password,
            "code":"njsptr",
            "tel":phone,
            "dxyzm":phonecode
                    }

        res=self.session.post("https://etax.ah-n-tax.gov.cn/anon/register/submit?"+self.rnum1,data=data,headers=self.headers).json()
        #{"code":200,"error":"","data":"","message":"","encrypType":"","encrypKey":"","encrypData":"","userToken":"","invalidArgs":""}
        if res["code"]==200:
            print("注册成功")
        else:
            print(res["message"])
        #{"code":442,"error":"","data":"","message":"请输入正确的图片验证码!","encrypType":"","encrypKey":"","encrypData":"","userToken":"","invalidArgs":""}
if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    idnum=sys.argv[1]
    name=sys.argv[2]
    name=parse.unquote(name)
    password=sys.argv[3]
    phone=sys.argv[4]
    phonecode=sys.argv[5]
    uuid=sys.argv[6]
    cookies=sys.argv[7]
    # idnum="130705198912281569"
    # name="庞俐娟"
    # #phone="15611570802"
    # #数字字母组合
    # password="a8050980200"
    # phone="15600461100"
    # phonecode=""
    # uuid=""
    # cookies=""
    ahz=AnHuizhuce()

    ahz.zhuce(idnum,name,password,phone,phonecode,uuid,cookies)
