import requests
import time
import io
import sys
import re
import json


ntime=str(int(time.time()*10000000))
def getyzm():
    resp=requests.get("https://ybs.he-n-tax.gov.cn:8888/login-web/login?service=https%3A%2F%2Fybs.he-n-tax.gov.cn%3A8888%2Fbase%2FgetRsaPublicKey.do",verify=False)
    lt=re.search('name="lt" value="(.*?)"',resp.text).group(1)
    execution = re.search('name="execution" value="(.*?)"', resp.text).group(1)
    res=requests.get("https://ybs.he-n-tax.gov.cn:8888/login-web/captcha.jpg?0.3556666066059264",verify=False)
    cname=ntime+".jpg"
    with open('/home/wwwroot/wbsr/heshuishuju/weixin/web/captcha/'+cname,"wb") as f:
        f.write(res.content)
        item = {}
        item["lt"] = lt
        item['execution'] = execution
        item["cname"] = cname
        shuju = json.dumps(item)
        print(shuju)
if __name__=="__main__":

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    getyzm()
