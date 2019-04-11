import requests
import json
import io
import sys
from urllib import parse
class HuBeizhuce():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    bankids={
        "中国银行":"01",
        "中国农业银行":"04",
        "交通银行":"16",
        "中国建设银行":"17",
        "中国工商银行":"18",
        "中国民生银行":"02",
        "中信实业银行":"15"
    }
    def __init__(self):
        self.session=requests.session()
    def getcookies(self,cookies):
        if cookies=="0":
            print("请填写注册信息")
            return 100
        res=str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}
        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
    def zhuce(self,name,idnum,phone,username,password,code):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "Content-Type": "text/plain;charset=UTF-8"
        }
        data="&yzm="+code+"&zjhm="+idnum+"&sjhm="+phone+"&dlmm="+password+"&account="+username+"&xm="+name+"&certify_type=0"
        data=data.encode()
        res=self.session.post("https://www.ehbds.gov.cn/webroot/wsbs/DjFirstAction.do?method=zjxmSave&isPartlyRefresh=true",data=data,headers=headers,verify=False)
        if res.text=="3":
            print("验证码输入错误")
            return
        if res.text==username:
            print("注册成功")
            return
        print(res.text)

if __name__=="__main__":
    sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
    # print(sys.argv)
    hbz=HuBeizhuce()
    name=sys.argv[1]
    name=parse.unquote(name)
    bankid=sys.argv[2]
    bankid=parse.unquote(bankid)
    idnum=sys.argv[3]
    banknum=sys.argv[4]
    phone=sys.argv[5]
    username=sys.argv[6]
    password=sys.argv[7]
    cookies=sys.argv[8]
    code = sys.argv[9]
 
    try:
        res=hbz.getcookies(cookies=cookies)
        if not res:
            hbz.zhuce(name=name,idnum=idnum,phone=phone,username=username,password=password,code=code)
    except Exception as e:
        print("系统维护中")