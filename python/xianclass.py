import requests
import time
import io
import re
import json
import base64
import os
import math
import sys
import pytesseract
import random
from urllib import parse
from PIL import ImageOps,Image
class XiAn():
    timeArray = time.localtime(time.time())
    nowtime = time.strftime("%Y-%m-%d", timeArray)
    jname=str(int(random.random()*100000000000))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    session=requests.session()
    ntime=str(int(time.time()*1000))
    def getli(self):
        res = self.session.get(
            "http://etaxs.sn-n-tax.gov.cn/sso/login?service=http://etaxs.sn-n-tax.gov.cn/xxmh/html/index.html?bszmFrom=1&t="+self.ntime,headers=self.headers,verify=False)

        execution = re.search('name="execution" value="(.*?)"', res.text).group(1)
        lt = re.search('name="lt" value="(.*?)"', res.text).group(1)
        return execution,lt
    def getyzm(self):
        res=self.session.get("http://etaxs.sn-n-tax.gov.cn/sso/base/captcha.do?t=1538036065649",headers=self.headers)
        with open(self.jname+".jpg","wb") as f:
            f.write(res.content)
            f.close()

    def pretreat_image(self, image):
       # image = ImageOps.invert(image)
        image.save(self.jname+".jpg")
        image = Image.open(self.jname+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 100)
       # image = ImageOps.invert(image)
        image.save(self.jname+".jpg")

    def iamge2imbw(self, image, threshold):
        # 设置二值化阀值
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, '1')
        image = image.convert('L')
        image = image.resize((120, 30), Image.ANTIALIAS)
        return image

    def readcode(self, path):
        image = Image.open(path)
        self.pretreat_image(image)
        image = Image.open(path)
        code = pytesseract.image_to_string(image).replace(" ", "").replace("\\", "").replace("¥","y")[0:6]
        return code

    def login(self,uname,password,li,code):
        data={
            "lt":li[1],
            "execution":li[0],
            "_eventId":"submit",
            "_llqmc":"Chrome",
            "_llqbb":"63.0.3239.132",
            "_czxt":"Windows",
            "_czxtbb":"Windows 8.1",
            "csessionid":"	",
            "sig":"	",
            "token":"",
            "scene":"",
            "loginType":"0",
            "authencationHandler":"UsernamePasswordAuthencationHandler",
            "userName":uname,
            "passWord":password,
            "sjly":"0",
            "captchCode":code
                    }
        res=self.session.post("http://etaxs.sn-n-tax.gov.cn/sso/login?service=http://etaxs.sn-n-tax.gov.cn/xxmh/html/index.html?bszmFrom=1&is_zrr=true&t=1538035633685",data=data,headers=self.headers)
        resp=self.session.post("http://etaxs.sn-n-tax.gov.cn/sso/auth/checkLoginState.do",headers=self.headers).json()

        return resp["flag"]

    def detail(self):
        # #https://etaxs.sn-n-tax.gov.cn/sxsq-cjpt-web/sxsq/query.do
        # resp = self.session.post("https://etaxs.sn-n-tax.gov.cn/sxsq-cjpt-web/sxsq/query.do",headers=self.headers).json()
        # print(resp)
        """
        zrrbz	Y
djxh	20126100000013645293
skssqq	2018-01-01
skssqz	2018-07-30
gdslxDm	1
swjgDm	0000000
skkjswjg	16101000000
sfzjlxDm	201
sfzjhm	610113197510070029
xm	郭研
sid	dzswj.sxsq.wsinit.grsdswszmkjcxjg
        """
        parme={
        "zrrbz":"Y",
        "gdslxDm":"1",
        "swjgDm":"0000000",
        "sid":"dzswj.sxsq.wsinit.kjgrsdswszmnsrjbxx",
        }
        #resp=self.session.post("http://etaxs.sn-n-tax.gov.cn/sso/auth/checkLoginState.do",headers=self.headers).json()
        resp=self.session.post("http://etaxs.sn-n-tax.gov.cn/sxsq-cjpt-web/sxsq/query.do",data=parme,headers=self.headers).json()

        djxh=resp["taxML"]["body"]["taxML"]["djxh"]
        name=resp["taxML"]["body"]["taxML"]["nsrmc"]
        nsrsbh = resp["taxML"]["body"]["taxML"]["nsrsbh"]
        zgswjDm = resp["taxML"]["body"]["taxML"]["swjgGrid"]["swjgGridlb"]
        timeArray = time.localtime(time.time())
        times = int(time.strftime("%Y", timeArray))
        #for j in range(times-8, times+1):
        for j in range(2018, 2019):
            try:
                for dicts in zgswjDm:
                    num = dicts["swjgDm"]
                    swjgmc = dicts["swjgmc"]

                    datas = {
                        "zrrbz": "Y",
                        "djxh": djxh,
                        "skssqq": str(j) + "-01-01",
                        "skssqz": str(j) + "-12-31",

                        "gdslxDm": "1",
                        "swjgDm	": "0000000",
                        "skkjswjg": "16100000000",
                        "sfzjlxDm": "201",
                        "sfzjhm": nsrsbh,
                        "xm": name,
                        "sid": "dzswj.sxsq.wsinit.grsdswszmkjcxjg"}
                    #https://etaxs.sn-n-tax.gov.cn/sxsq-cjpt-web/sxsq/query.do
                    res = self.session.post("http://etaxs.sn-n-tax.gov.cn/sxsq-cjpt-web/sxsq/query.do", data=datas,headers=self.headers).json()


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
                                      # "rkrqq": "",
                                      # "rkrqz": "",
                                      "dygs": "1",
                                      "skkjswjg": "16100000000",
                                      "gdslxDm": "1",
                                      "hxsj":"N",
                                      "jehj": str(hj)}


                            res=self.session.post("http://etaxs.sn-n-tax.gov.cn/sxsq-cjpt-web/kjsswszm/queryYzqxxBySfsssq.do",
                                         data=datass, headers=self.headers)

                            data1 = {
                                "gdslxDm": "1",
                                "swsxDm": "SXA052001002",
                                "dygs": "1",
                                "skkjswjg": "16100000000",
                                "lcswsxDm": "LCSXA031005001",
                                "slswsxDm": "SLSXA052001002",
                                "pzhmsfcf": "N",
                                "kjnyr": "190305",
                                "kjsfzm": "61证明",
                                "hxsj": "N"
                            }
                            """
                            gdslxDm	1
swsxDm	SXA052001002
dygs	1
skkjswjg	16101000000
lcswsxDm	LCSXA031005001
slswsxDm	SLSXA052001002
pzhmsfcf	N
kjnyr	190305
kjsfzm	61证明
hxsj	N
                            """
                            resp = self.session.post("http://etaxs.sn-n-tax.gov.cn/sxsq-cjpt-web/kjsswszm/queryZdpzhm.do",
                                                data=data1,headers=self.headers).json()
                            ndbc = resp["ndbc"]
                            pzzgDm=resp["pzzgDm"]
                            pzzgmc=resp["pzzgmc"]
                            zgzh = resp["pzhm"]
                            urls = self.nowtime + "," + str(hj) + "," + zgzh + ",2," + ndbc + ",2375012"
                            urls = urls.encode("utf-8")
                            urls = base64.b64encode(urls).decode("utf-8")
                            str1 = "<taxML><wszm><swry>系统管理员</swry><xtsphm></xtsphm><typztprs></typztprs><dygs>1</dygs><sfzjlxxx>居民身份证</sfzjlxxx><sfzjhmxx>"+nsrsbh+"</sfzjhmxx><cxrq></cxrq><pzzgs></pzzgs><swjgs></swjgs><tfrq>" + self.nowtime + "</tfrq><nsrsbh>" + nsrsbh + "</nsrsbh><nsrmc>" + name + "</nsrmc><zgswjmc>" + swjgmc + "</zgswjmc><kjgrsdswszmGrid><kjgrsdswszmGridlb>"
                            for k in shuju:
                                sj = '<sksssq>' + k["sfsssq"] + '</sksssq><jnd>' + k["swjgDm"] + '</jnd><rkrq>' + k[
                                    "rkrq"] + '</rkrq><zspmmc>' + k["zspmmc"] + '</zspmmc><zsxmmc>' + k[
                                         "zsxmmc"] + '</zsxmmc><sjje>' + k["sjje"] + '</sjje><nssbrq>' + k[
                                         "nssbrq"] + '</nssbrq></kjgrsdswszmGridlb><kjgrsdswszmGridlb>'
                                str1 += sj
                            str1 = str1 + '<jehj>¥' + str(hj) + '</jehj><jehjdx>' + self.convertNumToChinese(
                                hj) + '</jehjdx><pzzg>(' + ndbc + ')'+pzzgmc+'</pzzg><ewm>http://etaxs.sn-n-tax.gov.cn/sxsq-cjpt-web/kjsswszm/main.do?cs=' + urls + '</ewm><pzhm>' + zgzh + '</pzhm><wszmrows>2</wszmrows></wszm></taxML>'
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

                                "formData": str1,

                                "skssqq": str(j) + "-01-01",
                                "skssqz": str(j) + "-12-31",
                                "pzhm": zgzh,
                                "tfrq": self.nowtime,
                                "dygs": "1",
                                "rkrqz": "",
                                "rkrqq": "",
                                "jehj": hj,
                                "pzzgDm":pzzgDm,
                                "ndbc": ndbc
                            }
                            res = self.session.post("http://etaxs.sn-n-tax.gov.cn/sxsq-cjpt-web/kjsswszm/kj.do", data=data3,headers=self.headers).json()


                            data5 = {"yzqxxid": res["yzqxxid"],
                                     "ywlxDm": "sxsl",
                                     "dzbzdszlDm": res["dzbzdszlDm"],
                                     "swjgDm": "16100000000",
                                     "test": "false",
                                     "gdslxDm": "1",
                                     "sqbBz": "N",
                                     "dzbzdszlmc": res["dzbzdszlmc"],
                                     "xmldata":str1,
                                     "useFop": "Y"}
                            ss = self.session.post("http://etaxs.sn-n-tax.gov.cn/zlpz-cjpt-web/zlpz/hcPdf.do", data=data5,headers=self.headers)

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
                                "http://etaxs.sn-n-tax.gov.cn/zlpz-cjpt-web/zlpz/showPdfByYzqxxidAndDzbzdszlDm.do",
                                params=data4,headers=self.headers)

                            fname=djxh+str(j)+ str(num)+ ".pdf"
                            with open("/home/wwwroot/wbsr/python/files/" + fname, "wb") as f:
                            #with open(fname, "wb") as f:
                                f.write(res.content)
                            item={}
                            item["year"]=str(j)
                            item["fname"]=fname
                            item["name"]=name
                            item["lists"]=shuju
                            item=json.dumps(item)
                            print(item)
            except Exception as e:
                pass
    def convertNumToChinese(self,totalPrice):
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


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    uname=sys.argv[1]
    uame = parse.unquote(uname)
    password=sys.argv[2]
    password = parse.unquote(password)
    # uname="15902954570"
    # password="Gy123456"
    try:
        xa=XiAn()
        li=xa.getli()
        num=0
        while True:
            xa.getyzm()
            code=xa.readcode(xa.jname+".jpg")
            result=xa.login(uname,password,li,code)
            if result=="ok":
                os.remove(xa.jname+".jpg")
                xa.detail()
                break
            num+=1
            if num==20:
                os.remove(xa.jname+".jpg")
                print(100)
                break
    except Exception as e:
        print(500)
