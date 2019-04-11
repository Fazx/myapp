import requests
import time
import io
import random
import json
import sys
from urllib import parse

class GuangDongphone():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }

    def __init__(self):
        self.session=requests.session()
        self.nowtime=str(int(time.time()*1000))
        self.rtime=str(random.random())
        self.yname=str(int(random.random()*100000000000))

    def getphone(self,username,phone,imagecode,cookies):
        res=str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}
        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        # print(item1)
        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
        username1=parse.quote(username)
        res=self.session.get("https://www.etax-gd.gov.cn/yhgl/service/um/user/init/existsYhm.do?clientid=yhm&rand="+self.nowtime+"&yhm="+username1+"&verifiCode=&_="+self.nowtime,headers=self.headers).json()
        #res=self.session.get("https://www.etax-gd.gov.cn/yhgl/service/um/user/init/existsYhm.do?clientid=yhm&rand="+self.nowtime+"&yhm="+username1+"&verifiCode=&_="+self.nowtime,headers=self.headers)

        if res["flag"] == False:
            print(res["msg"])
            return
        res=self.session.get("https://www.etax-gd.gov.cn/yhgl/service/um/user/compareVerifiCode.do?clientid=verificode&rand="+self.nowtime+"&yhm=&verifiCode="+imagecode+"&verifiCode="+imagecode+"&_="+self.nowtime,headers=self.headers).json()
        # print(res)
        if res["code"] != "0":
            print("图片验证码错误")
            return

        resp=self.session.get("https://www.etax-gd.gov.cn/yhgl/service/um/user/init/existsSjh.do?clientid=sjh&rand="+self.nowtime+"&yhm=&verifiCode=&sjh="+phone+"&_="+self.nowtime,headers=self.headers).json()
        if resp["flag"] == "0":
            print(resp["msg"])
            return
        data={
            "sjh":phone,
            "type":"REGIST_SJH"
                    }
        respon=self.session.post("https://www.etax-gd.gov.cn/yhgl/service/um/user/init/sendCheckCodeRegist.do",data=data).json()
        #{'uuid': '0C243E9C665A4621A1DF4D6930407CCF', 'rtnCode': '0', 'rtncode': 0, 'message': '手机验证码发送成功'}
        #{"msg":"验证码已经发送","flag":true}
        if respon["flag"] == False:
            print("验证码发送失败")
            return
        msg="验证码发送成功"
        cookies=str(self.session.cookies.get_dict())
        item={}
        item["msg"]=msg
        item["cookies"]=cookies
        item=json.dumps(item)
        print(item)


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    username=sys.argv[1]
    username=parse.unquote(username)
    phone=sys.argv[2]
    imagecode=sys.argv[3]
    cookies=sys.argv[4]
    gdz=GuangDongphone()
    # username="颓废的兔子11"
    # phone="15600468476"
    # imagecode="243"
    # cookies="{'DZSWJ_TGC': '5065E205C7C6491B81B0CF84FE7DC039', 'SERVERID': 'cc95b21e869bbe5355ab9aeadbeb3be7|1542610013|1542610011', 'acw_tc': '276aedce15426100110456326e5d3bc763bcdafa44b1e042dc0c416846cb4f', 'JSESSIONID': 'AACCC4E6A1F60EE3A82EE3B1C057750B'}"
    gdz.getphone(username=username,phone=phone,imagecode=imagecode,cookies=cookies)



