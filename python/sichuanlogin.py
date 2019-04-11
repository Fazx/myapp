import requests
import re
import json
import io
import sys

from urllib import parse
class SiChuan():
    # headers={
    #     "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    # }
    session=requests.session()
    def login(self,lt,execution,cookies,sjhm,username,name,cardtype,code):
        if cookies=="0":
            print("请填写信息")
            return
        res = cookies.strip("{").strip("}")
        res = res.split(",")
        item1 = {}
        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        requests.utils.add_dict_to_cookiejar(self.session.cookies, {'DZSWJ_TGC': 'D6739C158C97BA4D4A68F8B9806B0D2F.worker3', 'Qr1B4j3m3iXPAw1X': 'v1LLRGgwSDBFh', 'JSESSIONID': '8E502D273DA0978A7A7F9650EE7872F4.worker3'})
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Accept": "text/plain;charset=UTF-8",
        }
        head={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                    }
        data={
            "sjhm":sjhm,
            "yzm":str(code),
            "bzxx":"zrr"
        }
        res=self.session.post('http://12366.sc-l-tax.gov.cn/sso/loginsms/verificationSms.do',params=data,headers=head).json()

        data={
            "zrrxm":name,
            "zrrsfzjhm":username,
            "sfzldxDm":cardtype
        }
        res=self.session.post("http://12366.sc-l-tax.gov.cn/sso/loginsc/saveJJdjzrr.do",data=data,headers=head)
        data={
            "lt":lt,
            "execution":execution,
            "_eventId":"submit",
            "zrrUxx":'{"sfzldxDm":"201","zrrsfzjhm":"'+username+'","zrrxm":"'+name+'","zrrsjhm":"'+sjhm+'","zrryzmcode":"Y"}',
            "_llqmc":"Chrome",
            "_llqbb":"63.0.3239.132",
            "_czxt":"Windows",
            "_czxtbb":"Windows 8.1",
            "csessionid":"",
            "sig":"",
            "token":"",
            "scene":"",
            "authencationHandler":"UserscdsloginZrrAuthencationHandler",
            "zrrsfzjhm":username,
            "zrrxm":name,
            "zrrsjhm":sjhm,
            "zrryzm":code
        }
        header={
            "Referer": "http://12366.sc-l-tax.gov.cn/sso/login?service=%2Fsso%2Foauth2%2Fauthorize.do%3Fclient_id%3Dcnct%26response_type%3Dcode%26scope%3Dsnsapi_userinfo%26state%3Dlogin%26redirect_uri%3Dhttp%253A%252F%252Fwsbs.sc-n-tax.gov.cn%253A80%252Fskip%252Findex.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            #"Cookie": "JSESSIONID=718AAC6AC80756CE37FB60164F4111BD.worker3; DZSWJ_TGC=B1A43D85E8D15837D0C968BC268010F3.worker3; JSESSIONID=D0037B81E0CF1C0691832BD7C2302F78.worker3; Qr1B4j3m3iXPAw1X=v1KrRGgwSD6Oy"
        }

        res=self.session.post("http://12366.sc-l-tax.gov.cn/sso/login",headers=header,data=data)
        headd={
            "Host": "12366.sc-l-tax.gov.cn",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Cache-Control": "max-age=0",
            "Origin": "http://12366.sc-l-tax.gov.cn",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "http://12366.sc-l-tax.gov.cn/sso/login",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        res=self.session.post("http://12366.sc-l-tax.gov.cn/sso/auth/checkLoginState.do?nsrsbh=undefined&gsuuid=undefined",headers=headd)
        res=self.session.get("http://12366.sc-l-tax.gov.cn/etax/cx/zrrWszm/wszm.do",verify=False)
        title=re.search('<title>完税情况查询</title>',res.text)
        if title:
            data={
                "action":"doCheckSm"
            }
            res=self.session.post("http://12366.sc-l-tax.gov.cn/etax/cx/zrrWszm/wszm.do?",data=data)
            result=re.search('<sid>(.*?)</sid><tid>(.*?)</tid>',res.text,re.S)
            if result:
                data={
                    "tid":result.group(2),
                    "sid":result.group(1)
                }
                res=self.session.post("http://12366.sc-l-tax.gov.cn/etax/cx/zrrWszm/wszm.do",data=data,headers=headers)
                for i in range(2006,2019):
                    data={
                        "action":"doQuery",
                        "start":str(i)+"-01-01",
                        "end":str(i)+"-12-31"
                                    }
                    res=self.session.post("http://12366.sc-l-tax.gov.cn/etax/cx/zrrWszm/wszm.do",data=data,headers=headers)
                    result=re.search('<sid>(.*?)</sid><tid>(.*?)</tid>',res.text,re.S)
                    data={
                        "tid":result.group(2),
                        "sid":result.group(1)
                    }
                    res=self.session.post("http://12366.sc-l-tax.gov.cn/etax/cx/zrrWszm/wszm.do",data=data,headers=headers)
                    shuju1=re.search('<wszInfo>(.*?)</wszInfo>',res.text)
                    if shuju1.group(1):
                        shuju=json.loads(shuju1.group(1))
                        data={
                            "action":"doCreate",
                            "wsmxs":shuju1.group(1)
                        }
                        res=self.session.post("http://12366.sc-l-tax.gov.cn/etax/cx/zrrWszm/wszm.do",data=data,headers=headers)
                        result = re.search('<sid>(.*?)</sid><tid>(.*?)</tid>', res.text, re.S)
                        data = {
                            "tid": result.group(2),
                            "sid": result.group(1)
                        }
                        res=self.session.post("http://12366.sc-l-tax.gov.cn/etax/cx/zrrWszm/wszm.do",data=data,headers=headers)
                        wdmc=re.search('"wdmc":"(.*?)"',res.text).group(1)
                        data={
                            "action": "doDownload",
                            "wsmxs": shuju1.group(1),
                            "wdmc":wdmc
                        }
                        res=self.session.post("http://12366.sc-l-tax.gov.cn/etax/cx/zrrWszm/wszm.do",data=data,headers=headers)
                        result = re.search('<sid>(.*?)</sid><tid>(.*?)</tid>', res.text, re.S)
                        data = {
                            "tid": result.group(2),
                            "sid": result.group(1)
                        }
                        res=self.session.post("http://12366.sc-l-tax.gov.cn/etax/cx/zrrWszm/wszm.do",data=data,headers=headers)
                        url=re.search('<downloadurl>(.*?)</downloadurl>',res.text).group(1)
                        res=self.session.get("http://12366.sc-l-tax.gov.cn"+url,headers=headers)
                        fname=str(i)+username+".pdf"
                        with open("/home/wwwroot/wbsr/python/files/"+ str(i)+username+".pdf","wb") as f:
                            f.write(res.content)
                        items={}
                        items["name"]=name
                        items["years"]=str(i)
                        items["fname"]=fname
                        items["lists"]=shuju
                        items=json.dumps(items)
                        print(items)
                else:
                    print("登录成功咱无数据")
            else:
                print("登录成功咱无数据")
        else:
            print("登录失败")

if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sc=SiChuan()
    lt = sys.argv[1]
    execution = sys.argv[2]
    cookies = sys.argv[3]
    sjhm = sys.argv[4]
    username = sys.argv[5]
    username=parse.unquote(username)
    name = sys.argv[6]
    name=parse.unquote(name)
    cardtype = sys.argv[7]
    code = sys.argv[8]

    # item["lt"] = lt
    # item["execution"] = execution
    # item["cookies"] = cookies
    # item["sjhm"] = sjhm
    # item["username"] = username
    # item["name"] = name
    # item["cardtype"] = self.cardtypes[cardtype]
    # code=input("验证码:")

    sc.login(lt,execution,cookies,sjhm,username,name,cardtype,code)

