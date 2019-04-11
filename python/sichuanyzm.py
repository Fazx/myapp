import requests
import re
import io
import sys
import json
from urllib import parse
class SiChuanyzm():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    session=requests.session()
    cardtypes={
        "身份证":"201",
        "军官证":"202",
        "武警警官证":"203",
        "士兵证":"204",
        "外国护照":"208",
        "港澳居民来往内地通行证":"210",
        "台湾居民来往大陆通行证":"213",
        "香港身份证":"219",
        "台湾身份证":"220",
        "澳门身份证":"221",
        "中国护照":"227",
        "外国人永久居留证":"233"
    }

    def getyzm(self,cardtype,username,name):
        self.session.get("http://12366.sc-l-tax.gov.cn/")
        res=self.session.get("http://12366.sc-l-tax.gov.cn/resource/html/scds/tzgg.json",headers=self.headers)
        resp=self.session.get("http://12366.sc-l-tax.gov.cn/sso/login",headers=self.headers)
        lt=re.search('name="lt" value="(.*?)"',resp.text).group(1)
        execution=re.search('name="execution" value="(.*?)"',resp.text).group(1)
        data={
                "sfzldxDm":self.cardtypes[cardtype],
                "zrrxm":name,
                "zrrsfzjhm":username
            }
        res=self.session.post("http://12366.sc-l-tax.gov.cn/sso/loginsc/queryZrrxx.do",data=data,headers=self.headers).json()
        if res["getzrrxxMap"]:
            sjhm=res["getzrrxxMap"]["sjhm"]
            data={
                "bzxx":"zrr"
            }
            res=self.session.post("http://12366.sc-l-tax.gov.cn/sso/loginsms/sendSms.do",data=data,headers=self.headers).json()
            cookies = self.session.cookies.get_dict()
            #cookies=str(cookies).replace("'","").replace(",",";").replace(": ","=").replace("{","").replace("}","")
            item={}
            item["lt"] =lt
            item["execution"] =execution
            item["cookies"] =str(cookies)
            item["sjhm"]=sjhm
            item["username"]=username
            item["name"]=name
            item["cardtype"]=self.cardtypes[cardtype]
            item=json.dumps(item)
            print(item)

        else:
            print("未查询到网报开户信息和实名认证信息，请进行实名认证")


if __name__=="__main__":
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cardtype=sys.argv[1]
    cardtype=parse.unquote(cardtype)
    username=sys.argv[2]
    username=parse.unquote(username)
    name=sys.argv[3]
    name=parse.unquote(name)
    # cardtype="身份证"
    # username="511524199412125070"
    # name="梁杰"
    sc=SiChuanyzm()
    sc.getyzm(cardtype,username,name)