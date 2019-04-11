import requests
import io
import sys
import random
import json
import re
import base64
import time
import pytesseract
from PIL import Image,ImageOps


class HuBei():

    session=requests.session()
    nowtime = str(int(time.time() * 1000))
    #ntime = str(int(random.random() * 100000000000000))
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }


    def __init__(self):
        self.ntime=str(int(random.random() * 100000000000000))
        timeArray = time.localtime(time.time())
        self.atime = int(time.strftime("%Y", timeArray))

    def index(self):
        res=self.session.get("https://wsswj.hb-n-tax.gov.cn/portal/",headers=self.headers,verify=False)
        csrf=re.search('var csrfPreventionSalt = "(.*?)"',res.text).group(1)
        self.session.post("https://wsswj.hb-n-tax.gov.cn/portal/tzgg/loadTips.c",headers=self.headers,verify=False).json()
        return csrf
    def getyzm(self,csrf):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "X-CSRF-Token": csrf,
            "c-token": csrf
        }
        res=self.session.post("https://wsswj.hb-n-tax.gov.cn/portal/vCode.c",headers=headers,verify=False).json()
        image=res["repData"]["image"]
        with open("/home/wwwroot/wbsr/heshuishuju/weixin/web/captcha/"+self.ntime+".jpg","wb") as f:
            f.write(base64.b64decode(image))
        cookies=self.session.cookies.get_dict()
        file=self.ntime+".jpg"
        item={}
        item["file"]=file
        item["csrf"]=csrf
        item["cookies"]=str(cookies)
        item=json.dumps(item)
        print(item)


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    hb = HuBei()
    csrf = hb.index()
    hb.getyzm(csrf)

