import requests
import time
import re
import sys
import io
import json
class HeBeiYzm():

    session =requests.session()
    ntime = str(int(time.time() * 10000000))
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    def pk(self):

        resp = self.session.get(
            "https://ybs.he-n-tax.gov.cn:8888/login-web/login?service=https%3A%2F%2Fybs.he-n-tax.gov.cn%3A8888%2Fbase%2FgetRsaPublicKey.do",
            verify=False,headers=self.headers)
        res=self.session.get('https://ybs.he-n-tax.gov.cn:8888/login-web/auth/validServerTime.do?clientTime=2018-10-11',headers=self.headers)
        lt = re.search('name="lt" value="(.*?)"', resp.text).group(1)
        execution = re.search('name="execution" value="(.*?)"', resp.text).group(1)
        res = self.session.get("https://ybs.he-n-tax.gov.cn:8888/login-web/captcha.jpg?0.3556666066059264",
                           verify=False,headers=self.headers)
        cname = self.ntime + ".jpg"
        with open('/home/wwwroot/wbsr/heshuishuju/weixin/web/captcha/'+cname, "wb") as f:
            f.write(res.content)


        #resp=self.session.post("https://ybs.he-n-tax.gov.cn:8888/login-web/login?service=https%3A%2F%2Fybs.he-n-tax.gov.cn%3A8888%2F%2520base%2520%2F%2520getRsaPublicKey.do",headers=self.headers,verify=False)
        #print(resp.text)
        respon = self.session.get("https://ybs.he-n-tax.gov.cn:8888/login-web/base/getRsaPublicKey.do",verify=False,headers=self.headers).json()
        cookies = self.session.cookies.get_dict()
        cookies=str(cookies).replace("'","").replace(",",";").replace(": ","=").replace("{","").replace("}","")

        pubkey=respon["data"]["pk"]
        item={}
        item["cname"]=cname
        item["lt"] =lt
        item["execution"] =execution
        item["pubkey"] =pubkey
        item["cookies"] =cookies
        item=json.dumps(item)
        print(item)



if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    hby=HeBeiYzm()
    hby.pk()
