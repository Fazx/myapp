import requests
import pytesseract
import sys
import io
from PIL import Image
from PIL import ImageOps,ImageDraw
from urllib import parse
#from loggers import logger
import ssl
import random
import os
import re
import time
import json
import subprocess
ssl._create_default_https_context=ssl._create_unverified_context
class Beijing():
    times=str(int(time.time()*10000000000))
    session=requests.session()
    rname=str(int(random.random()*10000000000))
    cardtype={
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
    def yanzhengma(self):
        self.session.get("https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/YhdlAction.action?code=login",verify=False)
        res=self.session.get("https://gt3app9.tax861.gov.cn/Gt3GsWeb/RandomCode?a=0.22584400113792769",verify=False)
        with open("/home/wwwroot/wbsr/python/images/"+self.times+".jpg","wb") as f:
            f.write(res.content)


    def pretreat_image(self,image):
        inverted_image = ImageOps.invert(image)
        inverted_image.save("/home/wwwroot/wbsr/python/images/"+self.times+".jpg")
        image = Image.open("/home/wwwroot/wbsr/python/images/"+self.times+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image,180)

        inverted_image = ImageOps.invert(image)
        # 保存图片
        inverted_image.save("/home/wwwroot/wbsr/python/images/"+self.times+".jpg")
        return image

    # 灰度图像二值化,返回0/255二值图像
    def iamge2imbw(self,image,threshold):
        # 设置二值化阀值
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table,'1')
        image = image.convert('L')

        return image

    def yanzheng(self,cardtype,name,card,password,yzm):

        #print(yzm)
        data={"zjlx":self.cardtype[cardtype],
        "zzhm":card,
        "xm":name,
        "password":password,
        "mmhg":"1",
        "yzm":yzm[:4],
        "oldMm":"",
        "newMm":"",
        "mmComf":""}
        respon=self.session.post("https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/YhdlAction.action?code=login",data=data,verify=False)
        #logger.info(respon)
        if "验证码错误" in respon.text:
            return "验证码错误"
        if "调用服务失败" in respon.text:
            return "调用服务失败"
        title=re.search('<title>个人纳税信息查询</title>',respon.text)
        if title:
            return 200
        pwd=re.search('您输入的密码有误，请重新输入密码，您还有(.*?)次机会，如机会用完将锁定您的账户30分钟',respon.text)
        if pwd:
            if pwd.group(1).strip()=="1":
                return 101
            elif pwd.group(1).strip()=="2":
                return 102
            elif pwd.group(1).strip()=="3":
                return 103
            elif pwd.group(1).strip()=="4":
                return 104
            else:
                return 100
        if "您输入的密码有误，请30分钟后重试" in respon.text:
            return 600
        if "已被系统限制登录" in respon.text:
            return 600
        if "未获取到该用户信息，请注册核准后查询" in respon.text:
            return 300
        return 400
    def detail(self,name):
        headers={
        "Host": "gt3app9.tax861.gov.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action?code=query",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        }
        atime = time.asctime()
        lang = len(atime)
        year = int(atime[lang - 4:lang + 1])

        for i in range(2006,year+1):
           # print(i)
            data={
            "tijiao":"grsbxxcx",
            "skssksrqY":"1",
            "skssksrqN":str(i),
            "skssjsrqY":"12",
            "skssjsrqN":str(i),
            "sbbmc"	:"",
            "index"	:"",
            "actionType":"query"
            }

            response=self.session.post("https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action?code=query",headers=headers,data=data,verify=False)
            html=response.text
            shuju=re.search('<textarea id="dyJson" style="display: none;">(.*?)</textarea>',html,re.S)
           
            if shuju.group(1):
               # print(shuju.group(1))
                try:
                    xiazai = re.search('<div class="dyan" onclick="window.location.href=(.*?)">', html, re.S)

                    url = "https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/" + xiazai.group(1).strip("'")
                   # print(url)
                    ress = self.session.get(url, headers=headers, verify=False)
                    fname=self.rname+ str(i) + ".pdf"
                    #print(fname)
                    bname="/home/wwwroot/wbsr/python/files/"+fname
                    #print(bname)
                    #print(ress.content)
                    try:
                        with open(bname, "wb") as f:

                            f.write(ress.content)
                    except Exception as e:
                        pass
                    item={}
                   
                    item["year"]=str(i)
                    item["fname"]=fname
                    item["lists"]=shuju.group(1)
                    shuju = json.dumps(item)
                    print(shuju)
                    
                       
                except Exception as e:
                    pass

            else:
                pass

        # html=etree.HTML(html)
        # total=html.xpath('.//tr[@class="change"]')
        # if total:
        #     for j in total:
        #         xuhao=j.xpath(".//td[1]/text()")[0].strip()
        #         laiyuan = j.xpath(".//td[2]/text()")[0].strip()
        #         times = j.xpath(".//td[3]/text()")[0].strip()
        #         num = j.xpath(".//td[4]/text()")[0].strip()
        #         shuilv = j.xpath(".//td[5]/text()")[0].strip()
        #         shuikuan = j.xpath(".//td[6]/text()")[0].strip()
        #         jiaoshuishijian = j.xpath(".//td[7]/text()")[0].strip()
        #         company = j.xpath(".//td[8]/text()")[0].strip()
        #         item={}
        #         item["xuhao"]=xuhao
        #         item["laiyuan"] = laiyuan
        #         item["times"]=times
        #         item["num"] = num
        #         item["shuilv"] = shuilv
        #         item["shuikuan"] = shuikuan
        #         item["jiaoshuishijian"] = jiaoshuishijian
        #         item["company"] = company
        #
        #         print(item)
if __name__=="__main__":
    
    bj = Beijing()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        # print(sys.argv)
    data1 = parse.unquote(sys.argv[1])
    data2 = parse.unquote(sys.argv[2])
        # print(sys.argv[1].encode("utf-8"))
        # print(data1)
    try:
        post_num=0
        while True:
            bj.yanzhengma()
            image = Image.open("/home/wwwroot/wbsr/python/images/"+bj.times+'.jpg')
            image = bj.pretreat_image(image)
            yzm = pytesseract.image_to_string("/home/wwwroot/wbsr/python/images/"+bj.times+".jpg")
            post_num+=1
            if post_num==10:
                os.remove("/home/wwwroot/wbsr/python/images/"+bj.times+".jpg")
                print(3)
                break
            if yzm:
                title = bj.yanzheng(data1, data2, sys.argv[3], sys.argv[4], yzm)
                
                os.remove("/home/wwwroot/wbsr/python/images/"+bj.times+".jpg")
                if title=="验证码错误":
                    pass
                elif title=="调用服务失败":
                    print(700)
                    break
                elif title==200:
                    bj.detail(data2)
                    break
                elif title==101:
                    print(101)
                    break
                elif title==102:
                    print(102)
                    break
                elif title==103:
                    print(103)
                    break
                elif title==104:
                    print(104)
                    break
                elif title==100:
                    print(100)
                    break
                elif title==600:
                    print(600)
                    break
                elif title==300:
                    print(300)
                    break
                else:
                    print(400)
                    break
            
    except Exception as e:
        print(500)

