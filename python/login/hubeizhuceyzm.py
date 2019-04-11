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

    def getyzm(self,name,bankid,idnum,banknum,phone,username):
        res=self.session.get("https://www.ehbds.gov.cn/webroot/register/register.jsp",headers=self.headers,verify=False)
        #print(res.text)
        res=self.session.get("https://www.ehbds.gov.cn/webroot/wsbs/pages/zrrdjn/smzPage.jsp",headers=self.headers,verify=False)
        #print(res.text)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "Content-Type": "text/plain;charset=UTF-8"
        }

        data='&zjhm='+idnum+'&xm='+name+'&smz=1'
        data=data.encode()
        res=self.session.post("https://www.ehbds.gov.cn/webroot/wsbs/DjFirstAction.do?method=zjxmValidate&isPartlyRefresh=true",data=data,headers=headers)
        if res.text=="3":
            print("您已完成实名制注册，请找回密码！")
            return
        if res.text=="1":
            print("您的信息与人口库比对失败，请确认信息后重试！")
            return
        res=self.session.post("https://www.ehbds.gov.cn/webroot/wsbs/DjFirstAction.do?method=CheckByAccount&acount="+username+"&isPartlyRefresh=true",headers=self.headers)
        if res.text!="0":
            print("登录名已被占用！请更换登录名")
            return

        res=self.session.post("https://www.ehbds.gov.cn/webroot/wsbs/DjFirstAction.do?method=checkByUnion&zjhm="+idnum+"&sjhm="+phone+"&yhkh="+banknum+"&yhxx="+self.bankids[bankid]+"&isPartlyRefresh=true",headers=self.headers)
        if res.text!="0":
            print("姓名或卡号或手机号输入有误，不匹配，请重新录入！")
            return
        res=self.session.post("https://www.ehbds.gov.cn/webroot/wsbs/DjFirstAction.do?method=fsYzm&sjhm="+phone+"&jymlx=1&isPartlyRefresh=true",headers=self.headers)
        if res.text == "true":
            item={}
            item["msg"]="校验码已成功发送,请注意查收!"
            item["cookies"]=str(self.session.cookies.get_dict())
            item=json.dumps(item)
            print(item)
            return
        print("发送失败")


if __name__=="__main__":
    sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
    # print(sys.argv)
    name=sys.argv[1]
    name=parse.unquote(name)
    bankid=sys.argv[2]
    bankid=parse.unquote(bankid)
    idnum=sys.argv[3]
    banknum=sys.argv[4]
    phone=sys.argv[5]
    username=sys.argv[6]

    try:
        hbz=HuBeizhuce()
        hbz.getyzm(name=name,bankid=bankid,idnum=idnum,banknum=banknum,phone=phone,username=username)
    except Exception as e:
        print("系统维护中")
