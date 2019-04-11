import requests
import random
import sys
import io
import re
import time
import json
from urllib  import parse
class ShenZhen():

    session=requests.session()
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    num=str(int(random.random()*10000))
    randomnum=str(int(random.random()*100000))
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))
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
    def login(self,cardtype,username,password,code):
        data={
            'gyptFlag':'Y',
            'zrrGj':'156',
            'zrrZjlx':self.cardtypes[cardtype],
            'zrrZjhm':username,
            'zrrPssw':password,
            'zrrSjdtm':code,
            'zrrCode':'',
            'pdwmmFlag':'N',
            'strRandom':self.randomnum,
            'fwbs':'zrrLogin',
            'gjDm':'156',
            'zjlx':self.cardtypes[cardtype],
            'zjhm':username,
            'dtm':code
        }

        res=self.session.post("https://dzswj.szds.gov.cn/dzswj/zrrUserLogin.do?method=zzrLogin&kbcs="+self.randomnum,data=data,headers=self.headers,verify=False)
        if "帐户将被锁定" in res.text:

            return 100
        if "您输入的手机动态码已超时" in res.text:

            return 300
        if "手机动态码不正确" in res.text:

            return 304
        if "密码修改页面" in res.text:
            # item={}
            # item["cookies"]=str(self.session.cookies.get_dict())
            # item=json.dumps(item)
            # print(item)
            return 200
            #https://dzswj.szds.gov.cn/dzswj/zrrUserLogin.do?method=savePsslw
            #omm	mz37vp  nmm	a8050980200   nmm2	a8050980200
        if username in res.text:
            return 200

        return 500
    def detail(self):
        # headers={
        #     'Cookie': 'mk=dzswj_real3; SZDS_NOLOGIN_JSESSION_ID=aee62e03-e6af-4439-9428-0c584bec0313; REDIS_JSESSION=28d99105-5c1d-4c47-acd0-e8ec2f944eb4`20124403100008622786'
        # }
        res=self.session.get("https://dzswj.szds.gov.cn/dzswj/zrrMain.do?method=toContent",headers=self.headers,verify=False)
        uname = re.search('<td style="width: 30%" class="text-left">(.*?)</td>', res.text).group(1)
        for i in range(2006,self.atime+1):
            data={
                'flag':'DY',
                    'sssq_q':str(i)+'-01-01',
                    'sssq_z':str(i)+'-12-31'
            }
            res=self.session.post("https://dzswj.szds.gov.cn/dzswj/zrrWszm.json?method=queryWszm",data=data,headers=self.headers,verify=False).json()
            if res["result"]["resultlist"]:
                shuju=res["result"]["resultlist"]
                nsrdzdah=shuju[0]["nsrdzdah"]
                res=self.session.post("https://dzswj.szds.gov.cn/dzswj/zrrWszm.do?method=printWszm&id="+self.num,data=data,headers=self.headers,verify=False)
                fname=str(i)+str(nsrdzdah)+".pdf"
                with open(str(i)+str(nsrdzdah)+".pdf","wb") as f:
                    f.write(res.content)
                item={}
                item["year"]=str(i)
                item["name"]=uname
                item["fname"]=fname
                item["lists"]=shuju
                item=json.dumps(item)
                print(item)



if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cardtype = sys.argv[1]
    username = sys.argv[2]
    password=sys.argv[3]
    code=sys.argv[4]
    cardtype = parse.unquote(cardtype)
    # cardtype="身份证"
    # username="131022198806100719"
    # password="100719"
    # password="a8050980200"
    # code="308556"
    try:
        sz=ShenZhen()
        result=sz.login(cardtype,username,password,code)

        if result==100:
            #"纳税人国籍、证件类型、证件号码、密码错误，请重新输入"
            print(100)
        elif result==200:
            #登录成功
            sz.detail()
        elif result==300:
            #"您输入的手机动态码已超时(有效时间3分钟，请重新获取手机动态验证码"
            print(300)
        elif result==304:
            #您输入的手机动态码不正确，请重新输入动态码
            print(304)
        # else:
        #     print(500)
    except:
        print(500)