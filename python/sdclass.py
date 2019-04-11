import requests
from PIL import Image, ImageOps
import re
import json
import sys
import io
import math
import time
import base64
from urllib import parse


class ShanDong():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    session = requests.session()
    timeArray = time.localtime(time.time())
    nowtime = time.strftime("%Y-%m-%d", timeArray)
    timeArray = time.localtime(time.time())
    ntime = time.strftime("%Y", timeArray)
    proxy={"http": "http://37.59.35.174:1080", "https": "http://37.59.35.174:1080"}
    def login(self, name, password):
        res=self.session.get("http://wb.taxcloud.sdds.gov.cn/xxmh/portalSer/checkLogin.do",headers=self.headers).json()
       # print(res.text)
       # return
        url=res["ssoXxmhUrl"]
        self.session.post("http://wb.taxcloud.sdds.gov.cn/sso/auth/getLastPctx.do",headers=self.headers)
        res=self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/viewsControlController/getShowGdsbz.do",headers=self.headers)
        res=self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/viewsControlController/getGolobalTitle.do",headers=self.headers)
        res=self.session.get(url=url,headers=self.headers)
        execution = re.search('name="execution" value="(.*?)"', res.text).group(1)
        lt = re.search('name="lt" value="(.*?)"', res.text).group(1)
        code = ""
        data = {
            "lt": lt,
            "execution": execution,
            "_eventId": "submit",
            "_llqmc": "Chrome",
            "_llqbb": "63.0.3239.132",
            "_czxt": "Windows",
            "_czxtbb": "Windows 8.1",
            "sjly": "0",
            "userName": name,
            "loginType": "0",
            "authencationHandler": "UsernamePasswordAuthencationHandler",
            "csessionid":"",
            "sig":"",
            "token":"",
            "scene":"",
            "RadioGroup1":"0",
            "userNameYhm":name,
            "userNameSjh":"",
            "zjlxDm":"201",
            "userNameZjhm":"",
            "passWord": password,
            "captchCode": code,
        }

        # http://wb.taxcloud.sdds.gov.cn/sso/login?service=http://wb.taxcloud.sdds.gov.cn/xxmh/html/index.html?bszmFrom=1&t=1508399396431&flag=casLoginView4SD
        #http://wb.taxcloud.sdds.gov.cn/sso/login?service=http://wb.taxcloud.sdds.gov.cn/xxmh/html/index.html?bszmFrom=1&t=1545019769583
        res = self.session.post(
            url=url,data=data,headers=self.headers)
        if "登录成功" in res.text:
            return url
        else:
            return

    def detail(self,url):
        resp = self.session.post("http://wb.taxcloud.sdds.gov.cn/sso/auth/checkLoginState.do").json()

        # {'flag': 'ok', 'nsr': None, 'xm': '贾浩', 'yhm': '颓废的兔子', 'zjhm': '131022198806100719', 'zjlx': '居民身份证', 'nsrQysqVos': [], 'sjly': '0'}
        # {'flag': 'ok', 'nsr': None, 'xm': None, 'yhm': '颓废的兔子11', 'nsrQysqVos': [], 'sjly': '0', 'needToSmz': 'true'}
        # {'flag': 'ok', 'nsr': None, 'xm': None, 'yhm': '漫步_0216', 'zjhm': '220622198512201016', 'zjlx': '居民身份证', 'nsrQysqVos': [{'yhnsrsfid': None, 'yhid': None, 'nsrztid': None, 'zzNsrztid': None, 'yhsfdm': '08', 'yhsfmc': '自然人', 'glqxbz': None, 'qybdid': None, 'yhqymc': None, 'zzNsrmc': None, 'ssdabh': None, 'shxydm': None, 'gszdjxh': None, 'dszdjxh': '29923700000050310936', 'gsnsrsbh': None, 'dsnsrsbh': '220622198512201016', 'nsrmc': '宋涛', 'dsNsrmc': '宋涛', 'gdsywsx': None, 'zjjgbz': None, 'sxqybz': None, 'hyyhbz': None, 'tybz': 'N', 'gsZgSwjgDm': None, 'dsZgSwjgDm': '23701000000', 'gsZgSwkfjDm': None, 'dsZgSwkfjDm': '23701000000', 'gdghlxdm': None, 'gsSsdabh': None, 'dsSsdabh': None, 'gsDjzclxDm': None, 'dsDjzclxDm': None, 'gsKzztdjlxDm': None, 'dsKzztdjlxDm': None}], 'sjly': '0'}
        #{"flag":"ok","nsr":null,"xm":"贾浩","yhm":"颓废的兔子","zjhm":"131022198806100719","zjlx":"居民身份证","nsrQysqVos":[{"yhnsrsfid":null,"yhid":null,"nsrztid":null,"zzNsrztid":null,"yhsfdm":"08","yhsfmc":"自然人","glqxbz":null,"qybdid":null,"yhqymc":null,"zzNsrmc":null,"ssdabh":null,"shxydm":null,"gszdjxh":null,"dszdjxh":"20123700100018517276","gsnsrsbh":null,"dsnsrsbh":"131022198806100719","nsrmc":"贾浩","dsNsrmc":"贾浩","gdsywsx":null,"zjjgbz":null,"sxqybz":null,"hyyhbz":null,"tybz":"N","gsZgSwjgDm":null,"dsZgSwjgDm":"23700000000","gsZgSwkfjDm":null,"dsZgSwkfjDm":"23700000000","gdghlxdm":null,"gsSsdabh":null,"dsSsdabh":null,"gsDjzclxDm":null,"dsDjzclxDm":null,"gsKzztdjlxDm":null,"dsKzztdjlxDm":null}],"sjly":"0"}
        if "needToSmz" in resp.keys():
            print(300)
        elif resp["nsrQysqVos"] == []:
            print(400)
        else:
            djxh = resp["nsrQysqVos"][0]["dszdjxh"]
            name = resp["nsrQysqVos"][0]["nsrmc"]
            nsrsbh = resp["nsrQysqVos"][0]["dsnsrsbh"]
            data={"djxh":""}
            self.session.post("http://wb.taxcloud.sdds.gov.cn/sso/auth/changeGrSf.do",data=data,headers=self.headers)
            res = self.session.post(url=url,headers=self.headers)
            res=self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/portalSer/checkLogin.do",headers=self.headers)
            res = self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/viewsControlController/getShowGdsbz.do",
                                    headers=self.headers)
            res = self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/viewsControlController/getGolobalTitle.do",
                                    headers=self.headers)
            res = self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/viewsControlController/getGolobalTitle.do",
                                    headers=self.headers)
            res = self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/viewsControlController/getShowGdsbz.do",
                                    headers=self.headers)
            res = self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/viewsControlController/getShowGdsbz.do",
                                    headers=self.headers)
            res=self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/portalSer/checkLogin.do",headers=self.headers)
            res=self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/sycdController/getCd.do",headers=self.headers)
            res=self.session.get("http://wb.taxcloud.sdds.gov.cn/xxmh/portalSer/getRootMenu.do?t=1545025632192",headers=self.headers)
            res=self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/portalSer/isZrrsfJr.do?t=1545025632311",headers=self.headers)
            res = self.session.post("http://wb.taxcloud.sdds.gov.cn/xxmh/cygnController/getCygncdDetail.do",
                                    headers=self.headers)
            parme = {
                "zrrbz": "Y",
                "gdslxDm": "1",
                "swjgDm": "0000000",
                "sid": "dzswj.sxsq.wsinit.kjgrsdswszmnsrjbxx",
            }
            respon = self.session.post("http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/sxsq/query.do", data=parme)
            zgswjDm = re.findall('"swjgDm":"(.*?)",', respon.text, re.S)
            for j in range(2006, 2019):
                time.sleep(1)
                for num in zgswjDm:
                    datas = {
                        "zrrbz": "Y",
                        "djxh": djxh,
                        "skssqq": str(j) + "-01-01",
                        "skssqz": str(j) + "-12-31",
                        "rkrqz": "",
                        "rkrqq": "",
                        "gdslxDm": "1",
                        "swjgDm	": "0000000",
                        "skkjswjg": num,
                        "sfzjlxDm": "",
                        "sfzjhm": "",
                        "xm": name,
                        "sid": "dzswj.sxsq.wsinit.grsdswszmkjcxjg"}
                    res = self.session.post("http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/sxsq/query.do",
                                            data=datas).json()
                    if res["taxML"]["body"]:
                        shuju = res["taxML"]["body"]["wszmGrid"]["wszmGridlb"]
                        if shuju:
                            swjgmc = shuju[0]["swjgmc"]
                            hj = 0
                            for heji in shuju:
                                hj += float(heji["sjje"])
                            hj = round(hj, 2)


                            datass = {"djxh": djxh,
                                      "skssqq": str(j) + "-01-01",
                                      "skssqz": str(j) + "-12-31",
                                      "pzzlDm": "",
                                      "dygs": "1",
                                      "skkjswjg": num,
                                      "gdslxDm": "1",
                                      "jehj": str(hj)}
                            # djxh=29923700000050310936&skssqq=2017-01-01&skssqz=2017-12-31&pzzlDm=000005012&rkrqq=&rkrqz=&dygs=1&skkjswjg=23701930000&gdslxDm=2&jehj=203.58
                            # djxh=29923700000050310936&skssqq=2018-01-01&skssqz=2018-12-10&pzzlDm=000005012&rkrqq=&rkrqz=&dygs=1&skkjswjg=23701930000&gdslxDm=2&jehj=354.92
                            # http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/queryYzqxxBySfsssq.do
                            # headers = {
                            #     "Cookie": "JSESSIONID=744A11C439603F6AC5C6C82BE9085468; DZSWJ_TGC=503BE4868CCA3436C4B4AEB3DBC89F79; route=3f18f3ae8a843670a42a1fea00f08e84; TGC=TGT-951-9ofCToOK5fBR0rPAdpGpGd9vKvA1VLTBbMWKjZKTOs5bCEw3lM-gddzswj; SYS_CHANNEL_ID=A01"}

                            heade = {
                                "X-Requested-With": "XMLHttpRequest",
                                "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                                # "Accept": "application/json, text/javascript, */*; q=0.01",
                                # "Cookie": "JSESSIONID=CD3DE4D8B075C15423F75B6BF8E5D2C0; route=3f18f3ae8a843670a42a1fea00f08e84; SYS_CHANNEL_ID=A01; DZSWJ_TGC=9BBD64FA794027535DBA3EDAE39F0F50; TGC=TGT-353-bk0ZOxX9ensOapz5FcabGcJSEFBtmrqN4Nmr19bMeOcepxIibJ-gddzswj"
                                # {'DZSWJ_TGC': 'F0F06BDC7B972F5B08B74DCAF0F772B3', 'TGC': 'TGT-961-oiJx7lr1kDM7VnVzyM0gfea13egIkv2I9DwcJOmcg6SAOojSza-gddzswj', 'SYS_CHANNEL_ID': 'A01', 'route': '3f18f3ae8a843670a42a1fea00f08e84', 'JSESSIONID': '8C6224D334E0513A0C4A0C9A2590662D'}
                            }
                            # http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/queryYzqxxBySfsssq.do

                            res = self.session.post(
                                "http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/queryYzqxxBySfsssq.do",data=datass, headers=heade)
                            """
                            gdslxDm	1
swsxDm	SXA052001002
dygs	1
skkjswjg	13701000000
lcswsxDm	LCSXA031005001
slswsxDm	SLSXA052001002
pzhmsfcf	N
kjnyr	190410
kjsfzm	37证明
                            """
                            dates=self.nowtime.replace("-","")[2:]
                            data1 = {
                                "gdslxDm": "1",
                                "swsxDm": "SXA052001002",
                                "dygs": "1",
                                "skkjswjg": num,
                                "lcswsxDm": "LCSXA031005001",
                                "slswsxDm": "SLSXA052001002",
                                "pzhmsfcf": "N",
                                "kjnyr":dates,
                                "kjsfzm":"37证明"
                            }
                            resp = self.session.post("http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/queryZdpzhm.do",
                                                     data=data1).json()
                            ndbc = resp["ndbc"]
                            zgzh=resp["pzhm"]
                            data2 = {
                                "gdslxDm": "2",
                                "nsrsbh": nsrsbh
                            }
                            res = self.session.post(
                                "http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/sddskjsswszm/queryPzhm.do",
                                data=data2).json()
                            urls = self.nowtime + "," + str(hj) + "," + zgzh + ",2," + ndbc + ",2375012"
                            urls = urls.encode("utf-8")
                            urls = base64.b64encode(urls).decode("utf-8")
                            str1 = "<taxML><wszm><swry></swry><xtsphm></xtsphm><typztprs>纳税人网上开具</typztprs><dygs>1</dygs><sfzjlxxx></sfzjlxxx><sfzjhmxx></sfzjhmxx><cxrq></cxrq><pzzgs>税收完税证明（文书式）"+dates[2:4]+"("+dates[4:8]+")37证明60001476</pzzgs><swjgs></swjgs><tfrq>" + self.nowtime + "</tfrq><nsrsbh>" + nsrsbh + "</nsrsbh><nsrmc>" + name + "</nsrmc><zgswjmc>" + swjgmc + "</zgswjmc><kjgrsdswszmGrid><kjgrsdswszmGridlb>"
                            for k in shuju:
                                sj = '<sksssq>' + k["sfsssq"] + '</sksssq><jnd>' + k["swjgDm"] + '</jnd><rkrq>' + k[
                                    "rkrq"] + '</rkrq><zspmmc>' + k["zspmmc"] + '</zspmmc><zsxmmc>' + k[
                                         "zsxmmc"] + '</zsxmmc><sjje>' + k["sjje"] + '</sjje><nssbrq>' + k[
                                         "nssbrq"] + '</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb>'
                                str1 += sj
                            str1 = str1 + '<jehj>¥' + str(hj) + '</jehj><jehjdx>' + self.convertNumToChinese(
                                hj) + '</jehjdx><pzzg>(' + ndbc + ')鲁税证明</pzzg><ewm>http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/main.do?cs=' + urls + '</ewm><pzhm>' + zgzh + '</pzhm><wszmrows>4</wszmrows></wszm></taxML>'
                            str1 = str1.replace("<kjgrsdswszmGridlb><jehj>", "</kjgrsdswszmGrid><jehj>")
                            data3 = {
                                "djxh": djxh,
                                "nsrsbh": nsrsbh,
                                "nsrmc": parse.quote(name),
                                "gdslxDm": "1",
                                "zgswjgDm": num,
                                "zgswjgmc": parse.quote(swjgmc),
                                "ywbm": "grsdswszmkj",
                                "swsxDm": "SXA052001002",
                                "slswsxDm": "SLSXA052001002",
                                "lcswsxDm": "LCSXA031005001",
                                # "formData":"<taxML><wszm><sfzjlxxx></sfzjlxxx><sfzjhmxx></sfzjhmxx><cxrq></cxrq><pzzgs>税收完税证明（文书式）(180)鲁税证明00055337</pzzgs><swjgs></swjgs><tfrq>2018年09月21日</tfrq><nsrsbh>220622198512201016</nsrsbh><nsrmc>宋涛</nsrmc><zgswjmc>国家税务总局济南高新技术产业开发区税务局</zgswjmc><kjgrsdswszmGrid><kjgrsdswszmGridlb><sksssq>2018-03-31至2018-03-01</sksssq><jnd>23701930000</jnd><rkrq>2018-04-11</rkrq><zspmmc>工资薪金所得</zspmmc><zsxmmc>个人所得税</zsxmmc><sjje>37.85</sjje><nssbrq>2018-04-10</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-02-28至2018-02-01</sksssq><jnd>23701930000</jnd><rkrq>2018-03-06</rkrq><zspmmc>工资薪金所得</zspmmc><zsxmmc>个人所得税</zsxmmc><sjje>82.00</sjje><nssbrq>2018-03-03</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-01-31至2018-01-01</sksssq><jnd>23701930000</jnd><rkrq>2018-02-07</rkrq><zspmmc>工资薪金所得</zspmmc><zsxmmc>个人所得税</zsxmmc><sjje>161.66</sjje><nssbrq>2018-02-06</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-06-30至2018-06-01</sksssq><jnd>23701930000</jnd><rkrq>2018-07-17</rkrq><zspmmc>工资薪金所得</zspmmc><zsxmmc>个人所得税</zsxmmc><sjje>6.00</sjje><nssbrq>2018-07-15</nssbrq></kjgrsdswszmGridlb></kjgrsdswszmGrid><jehj>¥287.51</jehj><jehjdx>贰佰捌拾柒元伍角壹分</jehjdx><pzzg>(180)鲁税证明</pzzg><ewm>http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/main.do?cs=MjAxOC0wOS0yMSwyODcuNTEsMDAwNTUzMzcsMiwxODAsMjM3NTAxMg==</ewm><pzhm>00055337</pzhm><wszmrows>4</wszmrows></wszm></taxML>",
                                "formData": str1,
                                # "<taxML><wszm><sfzjlxxx></sfzjlxxx><sfzjhmxx></sfzjhmxx><cxrq></cxrq><pzzgs>税收完税证明（文书式）(180)鲁税证明00055337</pzzgs><swjgs></swjgs><tfrq>2018年09月21日</tfrq><nsrsbh>220622198512201016</nsrsbh><nsrmc>宋涛</nsrmc><zgswjmc>国家税务总局济南高新技术产业开发区税务局</zgswjmc><kjgrsdswszmGrid><kjgrsdswszmGridlb><sksssq>2018-03-31至2018-03-01</sksssq><jnd>23701930000</jnd><rkrq>2018-04-11</rkrq><zspmmc>工资薪金所得</zspmmc><zsxmmc>个人所得税</zsxmmc><sjje>37.85</sjje><nssbrq>2018-04-10</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-02-28至2018-02-01</sksssq><jnd>23701930000</jnd><rkrq>2018-03-06</rkrq><zspmmc>工资薪金所得</zspmmc><zsxmmc>个人所得税</zsxmmc><sjje>82.00</sjje><nssbrq>2018-03-03</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-01-31至2018-01-01</sksssq><jnd>23701930000</jnd><rkrq>2018-02-07</rkrq><zspmmc>工资薪金所得</zspmmc><zsxmmc>个人所得税</zsxmmc><sjje>161.66</sjje><nssbrq>2018-02-06</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-06-30至2018-06-01</sksssq><jnd>23701930000</jnd><rkrq>2018-07-17</rkrq><zspmmc>工资薪金所得</zspmmc><zsxmmc>个人所得税</zsxmmc><sjje>6.00</sjje><nssbrq>2018-07-15</nssbrq></kjgrsdswszmGridlb></kjgrsdswszmGrid><jehj>¥287.51</jehj><jehjdx>贰佰捌拾柒元伍角壹分</jehjdx><pzzg>(180)鲁税证明</pzzg><ewm>http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/main.do?cs=MjAxOC0wOS0yMSwyODcuNTEsMDAwNTUzMzcsMiwxODAsMjM3NTAxMg==</ewm><pzhm>00055337</pzhm><wszmrows>4</wszmrows></wszm></taxML>"
                                "skssqq": str(j) + "-01-01",
                                "skssqz": str(j) + "-12-31",
                                "pzhm": zgzh,
                                "tfrq": self.nowtime,
                                "dygs": "1",
                                "rkrqz": "",
                                "rkrqq": "",
                                "jehj": hj,
                                "ndbc": ndbc,
                            }
                            res = self.session.post("http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/kj.do",
                                                    data=data3).json()
                            """
                            yzqxxid	07075B958C0C1C7E3D767972147D3322
ywlxDm	sxsl
dzbzdszlDm	GDA0510106
swjgDm	13701000000
test	false
gdslxDm	1
sqbBz	N
dzbzdszlmc	%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%E5%AE%8C%E7%A8%8E%E8%AF%81%E6%98%8E%E5%BC%80%E5%85%B7
xmldata	%3CtaxML%3E%3Cwszm%3E%3Cswry%3E%3C/swry%3E%3Cxtsphm%3E%3C/xtsphm%3E%3Ctypztprs%3E%E7%BA%B3%E7%A8%8E%E4%BA%BA%E7%BD%91%E4%B8%8A%E5%BC%80%E5%85%B7%3C/typztprs%3E%3Cdygs%3E1%3C/dygs%3E%3Csfzjlxxx%3E%3C/sfzjlxxx%3E%3Csfzjhmxx%3E%3C/sfzjhmxx%3E%3Ccxrq%3E%3C/cxrq%3E%3Cpzzgs%3E%E7%A8%8E%E6%94%B6%E5%AE%8C%E7%A8%8E%E8%AF%81%E6%98%8E%EF%BC%88%E6%96%87%E4%B9%A6%E5%BC%8F%EF%BC%8919(0410)37%E8%AF%81%E6%98%8E60001476%3C/pzzgs%3E%3Cswjgs%3E%3C/swjgs%3E%3Ctfrq%3E2019%E5%B9%B404%E6%9C%8810%E6%97%A5%3C/tfrq%3E%3Cnsrsbh%3E220622198512201016%3C/nsrsbh%3E%3Cnsrmc%3E%E5%AE%8B%E6%B6%9B%3C/nsrmc%3E%3Czgswjmc%3E%E5%9B%BD%E5%AE%B6%E7%A8%8E%E5%8A%A1%E6%80%BB%E5%B1%80%E6%B5%8E%E5%8D%97%E5%B8%82%E7%A8%8E%E5%8A%A1%E5%B1%80%3C/zgswjmc%3E%3CkjgrsdswszmGrid%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-01-01%E8%87%B32018-01-31%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-02-07%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E161.66%3C/sjje%3E%3Cnssbrq%3E2018-02-06%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-02-01%E8%87%B32018-02-28%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-03-06%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E82.00%3C/sjje%3E%3Cnssbrq%3E2018-03-03%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-03-01%E8%87%B32018-03-31%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-04-11%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E37.85%3C/sjje%3E%3Cnssbrq%3E2018-04-10%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-06-01%E8%87%B32018-06-30%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-07-17%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E6.00%3C/sjje%3E%3Cnssbrq%3E2018-07-15%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-08-01%E8%87%B32018-08-31%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-09-17%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E35.28%3C/sjje%3E%3Cnssbrq%3E2018-09-14%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-09-01%E8%87%B32018-09-30%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-10-24%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E32.13%3C/sjje%3E%3Cnssbrq%3E2018-10-23%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3C/kjgrsdswszmGrid%3E%3Cjehj%3E%C2%A5354.92%3C/jehj%3E%3Cjehjdx%3E%E5%8F%81%E4%BD%B0%E4%BC%8D%E6%8B%BE%E8%82%86%E5%85%83%E7%8E%96%E8%A7%92%E8%B4%B0%E5%88%86%3C/jehjdx%3E%3Cpzzg%3E19(0410)37%E8%AF%81%E6%98%8E%3C/pzzg%3E%3Cewm%3Ehttp://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/main.do?cs=MjAxOS0wNC0xMCwzNTQuOTIsNjAwMDE0NzYsMSwxOTAsMjM3NTAxMiwzNw==%3C/ewm%3E%3Cpzhm%3E60001476%3C/pzhm%3E%3Cwszmrows%3E6%3C/wszmrows%3E%3C/wszm%3E%3C/taxML%3E
useFop	Y
                            """
                            data5 = {"yzqxxid": res["yzqxxid"],
                                     "ywlxDm": "sxsl",
                                     "dzbzdszlDm": res["dzbzdszlDm"],
                                     "swjgDm": num,
                                     "test": "false",
                                     "gdslxDm": "1",
                                     "sqbBz": "N",
                                     "dzbzdszlmc": parse.quote(res["dzbzdszlmc"]),
                                     "xmldata": parse.quote(str1),
                                     "useFop": "Y"}
                            ss = self.session.post("http://wb.taxcloud.sdds.gov.cn/zlpz-cjpt-web/zlpz/hcPdf.do", data=data5)
                            """
                            djxh	29923700000050310936
skssqq	2018-01-01
skssqz	2018-12-31
pzzlDm	
dygs	1
skkjswjg	13701000000
gdslxDm	1
jehj	354.92
                            """

                            #self.session.post("http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/queryYzqxxBySfsssq.do",data=data)
                            """
                            gdslxDm	1
swsxDm	SXA052001002
dygs	1
skkjswjg	13701000000
lcswsxDm	LCSXA031005001
slswsxDm	SLSXA052001002
pzhmsfcf	N
kjnyr	190410
kjsfzm	37证明
                            """

                            #self.session.post("http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/queryZdpzhm.do",data=data)
                            data4 = {
                                "dzbzdszlDm": res["dzbzdszlDm"],
                                "gdslxDm": "1",
                                "sqbBz": "N",
                                "swjgDm": res["swjgDm"],
                                "test": "false",
                                "useFop": "Y",
                                "ywlxDm": "sxsl",
                                "yzqxxid": res["yzqxxid"]
                            }
                            res = self.session.get(
                                "http://wb.taxcloud.sdds.gov.cn/zlpz-cjpt-web/zlpz/showPdfByYzqxxidAndDzbzdszlDm.do",
                                params=data4)
                            #GET http://wb.taxcloud.sdds.gov.cn/zlpz-cjpt-web/zlpz/showPdfByYzqxxidAndDzbzdszlDm.do?yzqxxid=069F3A84FFFFFF80013A2B42E1224338&ywlxDm=sxsl&dzbzdszlDm=GDA0510106&swjgDm=13701000000&test=false&gdslxDm=1&sqbBz=N&useFop=Y HTTP/1.1
                            #GET http://wb.taxcloud.sdds.gov.cn/zlpz-cjpt-web/zlpz/showPdfByYzqxxidAndDzbzdszlDm.do?dzbzdszlDm=GDA0510106&gdslxDm=1&sqbBz=N&swjgDm=13701911200&test=false&useFop=Y&ywlxDm=sxsl&yzqxxid=069D2825FFFFFF846EA0009A554BA51D HTTP/1.1

                            fname = djxh + str(j) + ".pdf"
                            with open("/home/wwwroot/wbsr/python/files/"+fname, "wb") as f:
                                f.write(res.content)
                            item = {}
                            item["year"] = str(j)
                            item["fname"] = fname
                            item["name"] = name
                            item["lists"] = shuju
                            item = json.dumps(item)
                            print(item)

    def convertNumToChinese(self, totalPrice):
        dictChinese = [u'零', u'壹', u'贰', u'叁', u'肆', u'伍', u'陆', u'柒', u'捌', u'玖']
        unitChinese = [u'', u'拾', u'佰', u'仟', '', u'拾', u'佰', u'仟']
        # 将整数部分和小数部分区分开
        partA = int(math.floor(totalPrice))
        partB = round(totalPrice - partA, 2)
        strPartA = str(partA)
        strPartB = ''
        if partB != 0:
            strPartB = str(partB)[2:]

        singleNum = []
        if len(strPartA) != 0:
            i = 0
            while i < len(strPartA):
                singleNum.append(strPartA[i])
                i = i + 1
        # 将整数部分先压再出，因为可以从后向前处理，好判断位数
        tnumChinesePartA = []
        numChinesePartA = []
        j = 0
        bef = '0'
        if len(strPartA) != 0:
            while j < len(strPartA):
                curr = singleNum.pop()
                if curr == '0' and bef != '0':
                    tnumChinesePartA.append(dictChinese[0])
                    bef = curr
                if curr != '0':
                    tnumChinesePartA.append(unitChinese[j])
                    tnumChinesePartA.append(dictChinese[int(curr)])
                    bef = curr
                if j == 3:
                    tnumChinesePartA.append(u'万')
                    bef = '0'
                j = j + 1

            for i in range(len(tnumChinesePartA)):
                numChinesePartA.append(tnumChinesePartA.pop())
        A = ''
        for i in numChinesePartA:
            A = A + i
        # 小数部分很简单，只要判断下角是否为零
        B = ''
        if len(strPartB) == 1:
            B = dictChinese[int(strPartB[0])] + u'角'
        if len(strPartB) == 2 and strPartB[0] != '0':
            B = dictChinese[int(strPartB[0])] + u'角' + dictChinese[int(strPartB[1])] + u'分'
        if len(strPartB) == 2 and strPartB[0] == '0':
            B = dictChinese[int(strPartB[0])] + dictChinese[int(strPartB[1])] + u'分'

        if len(strPartB) == 0:
            S = A + u'圆整'
        if len(strPartB) != 0:
            S = A + u'圆' + B
        if S[0] == "万":
            S = S[1:len(S)]
        return S


if __name__ == "__main__":

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    #
    name = parse.unquote(sys.argv[1])
    password = sys.argv[2]
    #name = "漫步_0216"
    #password = "Song4tao7"
    #name = "颓废的兔子"
    # phone="13718798132"
    # password = "aA123456789"
    try:
        sd = ShanDong()
        result = sd.login(name, password)
        if result:
            sd.detail(result)
     
        else:
            print(100)
    except Exception as e:
        print(500)
#yzqxxid=069DC76EFFFFFF817D6B7C1DF7317753&ywlxDm=sxsl&dzbzdszlDm=GDA0510106&swjgDm=13701000000&test=false&gdslxDm=1&sqbBz=N&dzbzdszlmc=%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%25E5%25AE%258C%25E7%25A8%258E%25E8%25AF%2581%25E6%2598%258E%25E5%25BC%2580%25E5%2585%25B7&xmldata=%253CtaxML%253E%253Cwszm%253E%253Csfzjlxxx%253E%253C%2Fsfzjlxxx%253E%253Csfzjhmxx%253E%253C%2Fsfzjhmxx%253E%253Ccxrq%253E%253C%2Fcxrq%253E%253Cpzzgs%253E%25E7%25A8%258E%25E6%2594%25B6%25E5%25AE%258C%25E7%25A8%258E%25E8%25AF%2581%25E6%2598%258E%25EF%25BC%2588%25E6%2596%2587%25E4%25B9%25A6%25E5%25BC%258F%25EF%25BC%2589%2528190%2529%25E9%25B2%2581%25E7%25A8%258E%25E8%25AF%2581%25E6%2598%258E90000001%253C%2Fpzzgs%253E%253Cswjgs%253E%253C%2Fswjgs%253E%253Ctfrq%253E2019-04-10%253C%2Ftfrq%253E%253Cnsrsbh%253E220622198512201016%253C%2Fnsrsbh%253E%253Cnsrmc%253E%25E5%25AE%258B%25E6%25B6%259B%253C%2Fnsrmc%253E%253Czgswjmc%253E%25E5%259B%25BD%25E5%25AE%25B6%25E7%25A8%258E%25E5%258A%25A1%25E6%2580%25BB%25E5%25B1%2580%25E6%25B5%258E%25E5%258D%2597%25E9%25AB%2598%25E6%2596%25B0%25E6%258A%2580%25E6%259C%25AF%25E4%25BA%25A7%25E4%25B8%259A%25E5%25BC%2580%25E5%258F%2591%25E5%258C%25BA%25E7%25A8%258E%25E5%258A%25A1%25E5%25B1%2580%253C%2Fzgswjmc%253E%253CkjgrsdswszmGrid%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2017-12-01%25E8%2587%25B32017-12-31%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2018-01-03%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E43.66%253C%2Fsjje%253E%253Cnssbrq%253E2018-01-02%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2017-11-01%25E8%2587%25B32017-11-30%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2017-12-04%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E84.03%253C%2Fsjje%253E%253Cnssbrq%253E2017-12-01%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2017-10-01%25E8%2587%25B32017-10-31%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2017-11-07%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E38.37%253C%2Fsjje%253E%253Cnssbrq%253E2017-11-04%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2017-09-01%25E8%2587%25B32017-09-30%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2017-10-12%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E17.11%253C%2Fsjje%253E%253Cnssbrq%253E2017-10-11%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2017-08-01%25E8%2587%25B32017-08-31%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2017-09-04%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E20.41%253C%2Fsjje%253E%253Cnssbrq%253E2017-09-01%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253C%2FkjgrsdswszmGrid%253E%253Cjehj%253E%25C2%25A5203.58%253C%2Fjehj%253E%253Cjehjdx%253E%25E8%25B4%25B0%25E4%25BD%25B0%25E9%259B%25B6%25E5%258F%2581%25E5%259C%2586%25E4%25BC%258D%25E8%25A7%2592%25E6%258D%258C%25E5%2588%2586%253C%2Fjehjdx%253E%253Cpzzg%253E%2528190%2529%25E9%25B2%2581%25E7%25A8%258E%25E8%25AF%2581%25E6%2598%258E%253C%2Fpzzg%253E%253Cewm%253Ehttp%253A%2F%2Fwb.taxcloud.sdds.gov.cn%2Fsxsq-cjpt-web%2Fkjsswszm%2Fmain.do%253Fcs%253DMjAxOS0wNC0xMCwyMDMuNTgsOTAwMDAwMDEsMiwxOTAsMjM3NTAxMg%253D%253D%253C%2Fewm%253E%253Cpzhm%253E90000001%253C%2Fpzhm%253E%253Cwszmrows%253E4%253C%2Fwszmrows%253E%253C%2Fwszm%253E%253C%2FtaxML%253E&useFop=Y
#yzqxxid=069F4AEAFFFFFF80013A2B42591E927F&ywlxDm=sxsl&dzbzdszlDm=GDA0510106&swjgDm=13701000000&test=false&gdslxDm=1&sqbBz=N&dzbzdszlmc=%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%25E5%25AE%258C%25E7%25A8%258E%25E8%25AF%2581%25E6%2598%258E%25E5%25BC%2580%25E5%2585%25B7&xmldata=%253CtaxML%253E%253Cwszm%253E%253Cswry%253E%253C%2Fswry%253E%253Cxtsphm%253E%253C%2Fxtsphm%253E%253Ctypztprs%253E%25E7%25BA%25B3%25E7%25A8%258E%25E4%25BA%25BA%25E7%25BD%2591%25E4%25B8%258A%25E5%25BC%2580%25E5%2585%25B7%253C%2Ftypztprs%253E%253Cdygs%253E1%253C%2Fdygs%253E%253Csfzjlxxx%253E%253C%2Fsfzjlxxx%253E%253Csfzjhmxx%253E%253C%2Fsfzjhmxx%253E%253Ccxrq%253E%253C%2Fcxrq%253E%253Cpzzgs%253E%25E7%25A8%258E%25E6%2594%25B6%25E5%25AE%258C%25E7%25A8%258E%25E8%25AF%2581%25E6%2598%258E%25EF%25BC%2588%25E6%2596%2587%25E4%25B9%25A6%25E5%25BC%258F%25EF%25BC%258919(0410)37%25E8%25AF%2581%25E6%2598%258E60001448%253C%2Fpzzgs%253E%253Cswjgs%253E%253C%2Fswjgs%253E%253Ctfrq%253E2019%25E5%25B9%25B404%25E6%259C%258810%25E6%2597%25A5%253C%2Ftfrq%253E%253Cnsrsbh%253E220622198512201016%253C%2Fnsrsbh%253E%253Cnsrmc%253E%25E5%25AE%258B%25E6%25B6%259B%253C%2Fnsrmc%253E%253Czgswjmc%253E%25E5%259B%25BD%25E5%25AE%25B6%25E7%25A8%258E%25E5%258A%25A1%25E6%2580%25BB%25E5%25B1%2580%25E6%25B5%258E%25E5%258D%2597%25E5%25B8%2582%25E7%25A8%258E%25E5%258A%25A1%25E5%25B1%2580%253C%2Fzgswjmc%253E%253CkjgrsdswszmGrid%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2018-01-01%25E8%2587%25B32018-01-31%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2018-02-07%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E161.66%253C%2Fsjje%253E%253Cnssbrq%253E2018-02-06%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2018-02-01%25E8%2587%25B32018-02-28%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2018-03-06%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E82.00%253C%2Fsjje%253E%253Cnssbrq%253E2018-03-03%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2018-03-01%25E8%2587%25B32018-03-31%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2018-04-11%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E37.85%253C%2Fsjje%253E%253Cnssbrq%253E2018-04-10%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2018-06-01%25E8%2587%25B32018-06-30%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2018-07-17%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E6.00%253C%2Fsjje%253E%253Cnssbrq%253E2018-07-15%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2018-08-01%25E8%2587%25B32018-08-31%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2018-09-17%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E35.28%253C%2Fsjje%253E%253Cnssbrq%253E2018-09-14%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253CkjgrsdswszmGridlb%253E%253Csksssq%253E2018-09-01%25E8%2587%25B32018-09-30%253C%2Fsksssq%253E%253Cjnd%253E13701910000%253C%2Fjnd%253E%253Crkrq%253E2018-10-24%253C%2Frkrq%253E%253Czspmmc%253E%25E5%25B7%25A5%25E8%25B5%2584%25E8%2596%25AA%25E9%2587%2591%25E6%2589%2580%25E5%25BE%2597%253C%2Fzspmmc%253E%253Czsxmmc%253E%25E4%25B8%25AA%25E4%25BA%25BA%25E6%2589%2580%25E5%25BE%2597%25E7%25A8%258E%253C%2Fzsxmmc%253E%253Csjje%253E32.13%253C%2Fsjje%253E%253Cnssbrq%253E2018-10-23%253C%2Fnssbrq%253E%253C%2FkjgrsdswszmGridlb%253E%253C%2FkjgrsdswszmGrid%253E%253Cjehj%253E%25C2%25A5354.92%253C%2Fjehj%253E%253Cjehjdx%253E%25E5%258F%2581%25E4%25BD%25B0%25E4%25BC%258D%25E6%258B%25BE%25E8%2582%2586%25E5%2585%2583%25E7%258E%2596%25E8%25A7%2592%25E8%25B4%25B0%25E5%2588%2586%253C%2Fjehjdx%253E%253Cpzzg%253E19(0410)37%25E8%25AF%2581%25E6%2598%258E%253C%2Fpzzg%253E%253Cewm%253Ehttp%3A%2F%2Fwb.taxcloud.sdds.gov.cn%2Fsxsq-cjpt-web%2Fkjsswszm%2Fmain.do%3Fcs%3DMjAxOS0wNC0xMCwzNTQuOTIsNjAwMDE0NDgsMSwxOTAsMjM3NTAxMiwzNw%3D%3D%253C%2Fewm%253E%253Cpzhm%253E60001448%253C%2Fpzhm%253E%253Cwszmrows%253E6%253C%2Fwszmrows%253E%253C%2Fwszm%253E%253C%2FtaxML%253E&useFop=Y

#{"slswsxDm":"SLSXA052001002","ysqxxid":"89eb1f0884a14385ac4bb83af2b06d4e","skssqq":"2018-01-01","gdslxDm":"1","nsrmc":"宋涛","nsrsbh":"220622198512201016","dygs":"1","lcswsxDm":"LCSXA031005001","jehj":"354.92","swsxDm":"SXA052001002","ywbm":"GRSDSWSZMKJ","swjgDm":"13701000000","zgswjgmc":"国家税务总局济南市税务局","djxh":"29923700000050310936","formData":"<taxML><wszm><swry></swry><xtsphm></xtsphm><typztprs>???????</typztprs><dygs>1</dygs><sfzjlxxx></sfzjlxxx><sfzjhmxx></sfzjhmxx><cxrq></cxrq><pzzgs>???????????19(0410)37??60001448</pzzgs><swjgs></swjgs><tfrq>2019?04?10?</tfrq><nsrsbh>220622198512201016</nsrsbh><nsrmc>??</nsrmc><zgswjmc>????????????</zgswjmc><kjgrsdswszmGrid><kjgrsdswszmGridlb><sksssq>2018-01-01?2018-01-31</sksssq><jnd>13701910000</jnd><rkrq>2018-02-07</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>161.66</sjje><nssbrq>2018-02-06</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-02-01?2018-02-28</sksssq><jnd>13701910000</jnd><rkrq>2018-03-06</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>82.00</sjje><nssbrq>2018-03-03</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-03-01?2018-03-31</sksssq><jnd>13701910000</jnd><rkrq>2018-04-11</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>37.85</sjje><nssbrq>2018-04-10</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-06-01?2018-06-30</sksssq><jnd>13701910000</jnd><rkrq>2018-07-17</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>6.00</sjje><nssbrq>2018-07-15</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-08-01?2018-08-31</sksssq><jnd>13701910000</jnd><rkrq>2018-09-17</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>35.28</sjje><nssbrq>2018-09-14</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-09-01?2018-09-30</sksssq><jnd>13701910000</jnd><rkrq>2018-10-24</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>32.13</sjje><nssbrq>2018-10-23</nssbrq></kjgrsdswszmGridlb></kjgrsdswszmGrid><jehj> 354.92</jehj><jehjdx>??????????</jehjdx><pzzg>19(0410)37??</pzzg><ewm>http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/main.do?cs=MjAxOS0wNC0xMCwzNTQuOTIsNjAwMDE0NDgsMSwxOTAsMjM3NTAxMiwzNw==</ewm><pzhm>60001448</pzhm><wszmrows>6</wszmrows></wszm></taxML>","tfrq":"2019-04-10","ndbc":"190","pzzgDm":"2375012","dzbzdszlmc":"个人所得税完税证明开具","dzbzdszlDm":"GDA0510106","yzqxxid":"069F4AEAFFFFFF80013A2B42591E927F","pzhm":"60001448","skssqz":"2018-12-10","zgswjgDm":"13701000000"}
#{"slswsxDm":"SLSXA052001002","gdslxDm":"1","nsrsbh":"220622198512201016","lcswsxDm":"LCSXA031005001","dygs":"1","swsxDm":"SXA052001002","jehj":"73.41","djxh":"29923700000050310936","formData":"<taxML><wszm><sfzjlxxx></sfzjlxxx><sfzjhmxx></sfzjhmxx><cxrq></cxrq><pzzgs>???????????(190)????90000001</pzzgs><swjgs></swjgs><tfrq>2019-04-10</tfrq><nsrsbh>220622198512201016</nsrsbh><nsrmc>??</nsrmc><zgswjmc>????????????????????</zgswjmc><kjgrsdswszmGrid><kjgrsdswszmGridlb><sksssq>2018-09-01?2018-09-30</sksssq><jnd>13701910000</jnd><rkrq>2018-10-24</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>32.13</sjje><nssbrq>2018-10-23</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-08-01?2018-08-31</sksssq><jnd>13701910000</jnd><rkrq>2018-09-17</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>35.28</sjje><nssbrq>2018-09-14</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-06-01?2018-06-30</sksssq><jnd>13701910000</jnd><rkrq>2018-07-17</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>6.00</sjje><nssbrq>2018-07-15</nssbrq></kjgrsdswszmGridlb></kjgrsdswszmGrid><jehj> 73.41</jehj><jehjdx>????????</jehjdx><pzzg>(190)????</pzzg><ewm>http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/main.do?cs=MjAxOS0wNC0xMCw3My40MSw5MDAwMDAwMSwyLDE5MCwyMzc1MDEy</ewm><pzhm>90000001</pzhm><wszmrows>4</wszmrows></wszm></taxML>","yzqxxid":"069D2825FFFFFF846EA0009A554BA51D","dzbzdszlDm":"GDA0510106","skssqz":"2018-12-31","rkrqq":"","skssqq":"2018-01-01","ysqxxid":"848dceeda77947a3af413e1be71bd3b6","nsrmc":"宋涛","rkrqz":"","ywbm":"GRSDSWSZMKJ","zgswjgmc":"国家税务总局济南高新技术产业开发区税务局","swjgDm":"13701911200","tfrq":"2019-04-10","ndbc":"190","dzbzdszlmc":"个人所得税完税证明开具","zgswjgDm":"13701911200","pzhm":"90000001"}
#{"slswsxDm":"SLSXA052001002","gdslxDm":"1","nsrsbh":"220622198512201016","lcswsxDm":"LCSXA031005001","dygs":"1","swsxDm":"SXA052001002","jehj":"281.51","djxh":"29923700000050310936","formData":"<taxML><wszm><sfzjlxxx></sfzjlxxx><sfzjhmxx></sfzjhmxx><cxrq></cxrq><pzzgs>???????????(190)????90000001</pzzgs><swjgs></swjgs><tfrq>2019-04-10</tfrq><nsrsbh>220622198512201016</nsrsbh><nsrmc>??</nsrmc><zgswjmc>????????????????????</zgswjmc><kjgrsdswszmGrid><kjgrsdswszmGridlb><sksssq>2018-03-01?2018-03-31</sksssq><jnd>13701910000</jnd><rkrq>2018-04-11</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>37.85</sjje><nssbrq>2018-04-10</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-02-01?2018-02-28</sksssq><jnd>13701910000</jnd><rkrq>2018-03-06</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>82.00</sjje><nssbrq>2018-03-03</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb><sksssq>2018-01-01?2018-01-31</sksssq><jnd>13701910000</jnd><rkrq>2018-02-07</rkrq><zspmmc>??????</zspmmc><zsxmmc>?????</zsxmmc><sjje>161.66</sjje><nssbrq>2018-02-06</nssbrq></kjgrsdswszmGridlb></kjgrsdswszmGrid><jehj> 281.51</jehj><jehjdx>??????????</jehjdx><pzzg>(190)????</pzzg><ewm>http://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/main.do?cs=MjAxOS0wNC0xMCwyODEuNTEsOTAwMDAwMDEsMiwxOTAsMjM3NTAxMg==</ewm><pzhm>90000001</pzhm><wszmrows>4</wszmrows></wszm></taxML>","yzqxxid":"069E5A288C0C1C7D6FAE37AE56D80594","dzbzdszlDm":"GDA0510106","skssqz":"2018-12-31","rkrqq":"","skssqq":"2018-01-01","ysqxxid":"3997fcbb27e148e8ac8685daecd3a374","nsrmc":"宋涛","rkrqz":"","ywbm":"GRSDSWSZMKJ","zgswjgmc":"国家税务总局济南高新技术产业开发区税务局","swjgDm":"13701911100","tfrq":"2019-04-10","ndbc":"190","dzbzdszlmc":"个人所得税完税证明开具","zgswjgDm":"13701911100","pzhm":"90000001"}

#%3CtaxML%3E%3Cwszm%3E%3Cswry%3E%3C/swry%3E%3Cxtsphm%3E%3C/xtsphm%3E%3Ctypztprs%3E%E7%BA%B3%E7%A8%8E%E4%BA%BA%E7%BD%91%E4%B8%8A%E5%BC%80%E5%85%B7%3C/typztprs%3E%3Cdygs%3E1%3C/dygs%3E%3Csfzjlxxx%3E%3C/sfzjlxxx%3E%3Csfzjhmxx%3E%3C/sfzjhmxx%3E%3Ccxrq%3E%3C/cxrq%3E%3Cpzzgs%3E%E7%A8%8E%E6%94%B6%E5%AE%8C%E7%A8%8E%E8%AF%81%E6%98%8E%EF%BC%88%E6%96%87%E4%B9%A6%E5%BC%8F%EF%BC%8919(0410)37%E8%AF%81%E6%98%8E60001476%3C/pzzgs%3E%3Cswjgs%3E%3C/swjgs%3E%3Ctfrq%3E2019%E5%B9%B404%E6%9C%8810%E6%97%A5%3C/tfrq%3E%3Cnsrsbh%3E220622198512201016%3C/nsrsbh%3E%3Cnsrmc%3E%E5%AE%8B%E6%B6%9B%3C/nsrmc%3E%3Czgswjmc%3E%E5%9B%BD%E5%AE%B6%E7%A8%8E%E5%8A%A1%E6%80%BB%E5%B1%80%E6%B5%8E%E5%8D%97%E5%B8%82%E7%A8%8E%E5%8A%A1%E5%B1%80%3C/zgswjmc%3E%3CkjgrsdswszmGrid%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-01-01%E8%87%B32018-01-31%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-02-07%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E161.66%3C/sjje%3E%3Cnssbrq%3E2018-02-06%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-02-01%E8%87%B32018-02-28%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-03-06%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E82.00%3C/sjje%3E%3Cnssbrq%3E2018-03-03%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-03-01%E8%87%B32018-03-31%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-04-11%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E37.85%3C/sjje%3E%3Cnssbrq%3E2018-04-10%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-06-01%E8%87%B32018-06-30%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-07-17%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E6.00%3C/sjje%3E%3Cnssbrq%3E2018-07-15%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-08-01%E8%87%B32018-08-31%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-09-17%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E35.28%3C/sjje%3E%3Cnssbrq%3E2018-09-14%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2018-09-01%E8%87%B32018-09-30%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-10-24%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E32.13%3C/sjje%3E%3Cnssbrq%3E2018-10-23%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3C/kjgrsdswszmGrid%3E%3Cjehj%3E%C2%A5354.92%3C/jehj%3E%3Cjehjdx%3E%E5%8F%81%E4%BD%B0%E4%BC%8D%E6%8B%BE%E8%82%86%E5%85%83%E7%8E%96%E8%A7%92%E8%B4%B0%E5%88%86%3C/jehjdx%3E%3Cpzzg%3E19(0410)37%E8%AF%81%E6%98%8E%3C/pzzg%3E%3Cewm%3Ehttp://wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/main.do?cs=MjAxOS0wNC0xMCwzNTQuOTIsNjAwMDE0NzYsMSwxOTAsMjM3NTAxMiwzNw==%3C/ewm%3E%3Cpzhm%3E60001476%3C/pzhm%3E%3Cwszmrows%3E6%3C/wszmrows%3E%3C/wszm%3E%3C/taxML%3E
#%3CtaxML%3E%3Cwszm%3E%3Csfzjlxxx%3E%3C/sfzjlxxx%3E%3Csfzjhmxx%3E%3C/sfzjhmxx%3E%3Ccxrq%3E%3C/cxrq%3E%3Cpzzgs%3E%E7%A8%8E%E6%94%B6%E5%AE%8C%E7%A8%8E%E8%AF%81%E6%98%8E%EF%BC%88%E6%96%87%E4%B9%A6%E5%BC%8F%EF%BC%89%28190%29%E9%B2%81%E7%A8%8E%E8%AF%81%E6%98%8E90000001%3C/pzzgs%3E%3Cswjgs%3E%3C/swjgs%3E%3Ctfrq%3E2019-04-10%3C/tfrq%3E%3Cnsrsbh%3E220622198512201016%3C/nsrsbh%3E%3Cnsrmc%3E%E5%AE%8B%E6%B6%9B%3C/nsrmc%3E%3Czgswjmc%3E%E5%9B%BD%E5%AE%B6%E7%A8%8E%E5%8A%A1%E6%80%BB%E5%B1%80%E6%B5%8E%E5%8D%97%E9%AB%98%E6%96%B0%E6%8A%80%E6%9C%AF%E4%BA%A7%E4%B8%9A%E5%BC%80%E5%8F%91%E5%8C%BA%E7%A8%8E%E5%8A%A1%E5%B1%80%3C/zgswjmc%3E%3CkjgrsdswszmGrid%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2017-12-01%E8%87%B32017-12-31%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2018-01-03%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E43.66%3C/sjje%3E%3Cnssbrq%3E2018-01-02%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2017-11-01%E8%87%B32017-11-30%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2017-12-04%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E84.03%3C/sjje%3E%3Cnssbrq%3E2017-12-01%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2017-10-01%E8%87%B32017-10-31%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2017-11-07%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E38.37%3C/sjje%3E%3Cnssbrq%3E2017-11-04%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2017-09-01%E8%87%B32017-09-30%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2017-10-12%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E17.11%3C/sjje%3E%3Cnssbrq%3E2017-10-11%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3CkjgrsdswszmGridlb%3E%3Csksssq%3E2017-08-01%E8%87%B32017-08-31%3C/sksssq%3E%3Cjnd%3E13701910000%3C/jnd%3E%3Crkrq%3E2017-09-04%3C/rkrq%3E%3Czspmmc%3E%E5%B7%A5%E8%B5%84%E8%96%AA%E9%87%91%E6%89%80%E5%BE%97%3C/zspmmc%3E%3Czsxmmc%3E%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E%3C/zsxmmc%3E%3Csjje%3E20.41%3C/sjje%3E%3Cnssbrq%3E2017-09-01%3C/nssbrq%3E%3C/kjgrsdswszmGridlb%3E%3C/kjgrsdswszmGrid%3E%3Cjehj%3E%C2%A5203.58%3C/jehj%3E%3Cjehjdx%3E%E8%B4%B0%E4%BD%B0%E9%9B%B6%E5%8F%81%E5%9C%86%E4%BC%8D%E8%A7%92%E6%8D%8C%E5%88%86%3C/jehjdx%3E%3Cpzzg%3E%28190%29%E9%B2%81%E7%A8%8E%E8%AF%81%E6%98%8E%3C/pzzg%3E%3Cewm%3Ehttp%3A//wb.taxcloud.sdds.gov.cn/sxsq-cjpt-web/kjsswszm/main.do%3Fcs%3DMjAxOS0wNC0xMCwyMDMuNTgsOTAwMDAwMDEsMiwxOTAsMjM3NTAxMg%3D%3D%3C/ewm%3E%3Cpzhm%3E90000001%3C/pzhm%3E%3Cwszmrows%3E4%3C/wszmrows%3E%3C/wszm%3E%3C/taxML%3E