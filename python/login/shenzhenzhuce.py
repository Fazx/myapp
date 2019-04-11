import requests
import re
import json
import io
import time
import sys
import random
from urllib import parse

class ShenZhenzhuce1():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    bankcardtypes={
        "招商银行":["0009","b2cBANKTYPE_CMB"],
        "中国银行":["0004","b2cBANKTYPE_BC"],
        "中信银行":["0007","b2cBANKTYPE_CITIC"],
        "中国工商银行":["0002","b2cBANKTYPE_ICBC"],
        "中国农业银行":["0003","b2cBANKTYPE_ABC"],
        "交通银行":["0006","b2cBANKTYPE_BCM"],
        "平安银行":["0008","b2cBANKTYPE_PINGAN"],
        "中国建设银行":["0005","b2cBANKTYPE_CCB"]
    }
    def __init__(self):
        self.session=requests.session()
        self.nowtime=str(int(time.time()*1000))
        self.imagename=str(int(random.random()*1000000000000))
    def yanzheng(self,username,idcard,banktype,phone):
        self.session.get("https://dzswj.szds.gov.cn/dzswj/wykt.do?method=init",headers=self.headers,verify=False)
        res=self.session.get("https://dzswj.szds.gov.cn/dzswj/indexPage.jsp?fwbs=zrrLogin&gyptBdsjBz=Y&tamp="+self.nowtime,headers=self.headers)
        #print(res.text)
        res=self.session.get("https://dzswj.szds.gov.cn/dzswj/wykt.do?method=toxyz&fwbs=",headers=self.headers)
        rid=re.search('id="strRandom" value="(.*?)">',res.text).group(1)
        res=self.session.get("https://dzswj.szds.gov.cn/dzswj/wykt.do?method=toWykt&fwbs=&id="+rid,headers=self.headers)
        data={
            "MerSeqId":"",
            "strRom":rid,
            "zjlxDm":"	201",
            "sfzzhm":idcard,
            "gjDm":"156",
            "xm":username
        }
        head={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        res=self.session.post("https://dzswj.szds.gov.cn/dzswj/wykt.json?method=sfyz&randonNum="+rid,data=data,headers=head).json()
        # print(res)
        if "CheckValue" not in res.keys():
            if not res["result"]["msg"]:
                print("该账号已开通请直接登录")
                return
            print(res["result"]["msg"])
            return

        #{'result': {'code': '1', 'msg': '用户名称不能为空！(错误代码:9002001)', 'obj': '', 'resultlist': []}}
        #{'result': {'code': '1', 'msg': '确认认证申请异常:报文格式错误[证件号码不正确！](错误代码:9002003)', 'obj': '', 'resultlist': []}}{'result': {'code': '1', 'msg': '确认认证申请异常:报文格式错误[证件号码不正确！](错误代码:9002003)', 'obj': '', 'resultlist': []}}
        PaymentUrl=res["PaymentUrl"]
        Packet=res["Packet"]
        Sender=res["Sender"]
        CheckValue=res["CheckValue"]

        data1={
            "PaymentUrl":PaymentUrl,
            "Packet":Packet,
            "Sender":Sender,
            "CheckValue":CheckValue
        }
        res=self.session.post("https://dzswj.szds.gov.cn/dzswj/wykt.do?method=postToWyzfPage&dzswjRandonNum="+rid,data=data1,headers=self.headers)
        url=re.search('method="post" action="(.*?)"',res.text).group(1)
        nowdate=re.search('(\d+)',url).group(1)
        data2={
            "Packet": Packet,
            "Sender": Sender,
            "CheckValue": CheckValue
        }
        #action="http://pay.szfesc.cn/wyzf-access/deal?merChkBillSn=20181119100004501586"
        res=self.session.post(url,data=data2,headers=self.headers)
        baseurl=re.search("location.href='(.*?)'",res.text).group(1)
        res=self.session.get(baseurl,headers=self.headers)

        data3={
            "merChkBillSn":nowdate,
            "bankType":self.bankcardtypes[banktype][0],
            "custName":username,
            "custCertNo":idcard,
            "bankCodeb2c":self.bankcardtypes[banktype][1],
            "x":"37",
            "y":"15"
        }
        res=self.session.post("http://pay.szfesc.cn/wyzf-gateway/RealNameVerification/showConfirm",data=data3,headers=self.headers)
        data4={
            "phone":phone
        }
        res=self.session.post("http://pay.szfesc.cn/wyzf-gateway/RealNameVerification/sendVertiy",data=data4,headers=self.headers).json()
        if res["success"] ==False:
            print("验证码发送失败")
            return
        vertiyId=res["vertiyId"]
        #{"success": true, "vertiyId": "201811196546448"}
        #print(vertiyId)
        item = {}
        item["vertiyId"]=vertiyId
        item["banktypenum"]=self.bankcardtypes[banktype][0]
        item["merChkBillSn"]=nowdate
        item["cookies"]=str(self.session.cookies.get_dict())
        item=json.dumps(item)
        print(item)

# 获取短信验证码
if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # username="杜宏飞11"
    # idcard="622621199205113213"
    # banktype="中国工商银行"
    # banknum="621226020008867893900"
    # phone="13718798132000"
    username=sys.argv[1]
    username=parse.unquote(username)
    idcard=sys.argv[2]
    banktype=sys.argv[3]
    banktype=parse.unquote(banktype)
    phone=sys.argv[4]
    # username="庞俐娟"
    # idcard="130705198912281569"
    # banktype="中国工商银行"
    # banknum="6210676862060205049"
    # phone="15611570802"
    szz=ShenZhenzhuce1()
    szz.yanzheng(username=username,idcard=idcard,banktype=banktype,phone=phone)
