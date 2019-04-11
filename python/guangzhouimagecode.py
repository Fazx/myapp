import requests
import time
import random
import json
import io
import sys
from urllib import parse
class GuangDongimage():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }

    def __init__(self):
        self.session=requests.session()
        self.nowtime=str(int(time.time()*1000))
        self.rtime=str(random.random())
        self.yname=str(int(random.random()*100000000000))
    def getyanzhengma(self):
        res=self.session.get("https://www.etax-gd.gov.cn/yhgl/service/um/user/init",headers=self.headers,verify=False)
        time.sleep(2)
        res=self.session.get("https://www.etax-gd.gov.cn/yhgl/service/um/user/verificode.do?t="+self.nowtime,headers=self.headers)
        with open('/home/wwwroot/wbsr/heshuishuju/weixin/web/captcha/'+self.yname+".jpg","wb") as f:
            f.write(res.content)
        cookies=str(self.session.cookies.get_dict())
        item={}
        item["image"]=self.yname+".jpg"
        item["cookies"]=cookies
        item=json.dumps(item)
        print(item)


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    gdz=GuangDongimage()
    gdz.getyanzhengma()

    #gdz.zhuce(username=username, password=password, phone=phone, imagecode=imagecode, code=code)


