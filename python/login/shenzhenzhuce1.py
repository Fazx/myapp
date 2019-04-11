import requests
import re
import json
import io
import time
import sys
import pytesseract
import random
from urllib import parse
from PIL import Image,ImageOps
class ShenZhenzhuce2():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    bankcardtypes={
        "招商银行":["0009","b2cBANKTYPE_CMB"],
        "中国银行":["0004","b2cBANKTYPE_BC"],
        "中信银行":["0007","b2cBANKTYPE_CITIC"],
        "中国工商银行":["0002","b2cBANKTYPE_ICBC"],
        "中国农业银行":["0003","b2cBANKTYPE_ABC"],
        "交通银行":["0006","b2cBANKTYPE_BCM"],
        "平安银行":["0008","b2cBANKTYPE_PINGAN"],
        "中国建设银行":["0005","b2cBANKTYPE_CCB"]
    }
    def __init__(self):
        self.session=requests.session()
        self.nowtime=str(int(time.time()*1000))
        self.imagename=str(int(random.random()*1000000000000))

    def zhuce(self,phone,banktypenum,banknum,merChkBillSn,vertiyId,code,cookies):
        if cookies=="0":
            print("请输入信息")
            return
        res=str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}

        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
        data={
            "param":code,
            "name":vertiyId+"|"+phone
        }
        res=self.session.post("http://pay.szfesc.cn/wyzf-gateway/RealNameVerification/vertiySmsCode",data=data,headers=self.headers).json()

        #{"status":"n","info":"短信验证码错误"}
        if res["status"]=="n":
            print("短信验证码错误")
            return
        data1={
            "merChkBillSn":merChkBillSn,
            "acctId":banknum,
            "phoneNm":phone,
            "smsCodeId":vertiyId,
            "smsCodeValue":code,
            "bankType":banktypenum
        }

        #{"status":"1","errMsg":"失败原因：实名认证信息不正确","merChkBillSn":"20181119100004501747"}
        #{"custCertType":"身份证","status":"2","checkType":"3","checkDate":"2018-11-19","custCertNo":"131******806100719","phoneNm":"15****61100","custName":"贾浩","merChkBillSn":"20181119100004502148"}
        #                           http://pay.szfesc.cn/wyzf-gateway/RealNameVerification/checkConfirm
        res=self.session.post("http://pay.szfesc.cn/wyzf-gateway/RealNameVerification/checkConfirm",data=data1,headers=self.headers).json()
        if res["status"] != "2":
            print("实名认证信息不正确")
            return
        data2={
            "status":res["status"],
            "custCertNo":res["custCertNo"],
            "custName":parse.quote(res["custName"]),
            "phoneNm":res["phoneNm"],
            "checkDate":res["checkDate"],
            "checkType":res["checkType"],
            "certTypeName":parse.quote(res["custCertType"]),
            "merChkBillSn":res["merChkBillSn"]
                    }
        res=self.session.get("http://pay.szfesc.cn/wyzf-gateway/RealNameVerification/showMsgPage",params=data2,headers=self.headers)
        if "恭喜您已完成实名认证" not in res.text:
            print("实名认证失败")
            return
        url=re.search('name="toMerFormId" action="(.*?)"',res.text).group(1)
        Packet=re.search('name="Packet" value=\'(.*?)\'',res.text,re.S).group(1)
        CheckValue=re.search('name="CheckValue"value=\'(.*?)\'',res.text,re.S).group(1)
        Sender=re.search('name="Sender" value=\'(.*?)\'(.*?)/>',res.text,re.S).group(1).strip()
        #print(url,Packet,CheckValue,Sender)
        data3={
            "Packet":Packet,
            "CheckValue":CheckValue,
            "Sender":Sender
        }
        res=self.session.post(url,data=data3,headers=self.headers)
        strRom=re.search('id="strRom" value="(.*?)"',res.text).group(1)
        return strRom
    def getyzm(self):
        # res=self.session.get("https://dzswj.szds.gov.cn/dzswj/forLoginCode.do?method=getCode&nsrLgRanNum="+strRom,headers=self.headers)
        # with open(self.imagename+".jpg","wb") as f:
        #     f.write(res.content)
        resp = self.session.get("https://dzswj.szds.gov.cn/dzswj/forLoginCode.do?method=getCode&timestamp=" + self.nowtime,
                           verify=False)
        # resp=session.get("https://dzswj.szds.gov.cn/dzswj/forLoginCode.do?method=getCode&nsrLgRanNum=34332",verify=False)
        with open(self.imagename+".jpg", "wb") as f:
            f.write(resp.content)
    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save(self.imagename+".jpg")
        image = Image.open(self.imagename+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 160)
        image = ImageOps.invert(image)
        image.save(self.imagename+".jpg")
        # return image


        # 灰度图像二值化,返回0/255二值图像

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

        return image

    def readcode(self, path):
        image = Image.open(path)
        self.pretreat_image(image)
        image = Image.open(path)
        x_s = 100  # define standard width
        y_s = 40  # calc height based on standard width
        out = image.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
        out.save(path)
        code = pytesseract.image_to_string(out).replace(" ", "").replace("\\", "")[0:4]
        return code

    def zhuce1(self, idcard, phone, username, strRom, swjgDm, jsdz, imagecode):
        data={
            "zjlxDm":"201",
            "sfzzhm":idcard,
            "rzsjhm":phone,
            "gjDm":"156",
            "xm":username,
            "checkFlag":"Y",
            "strRom":strRom,
            "jszxSjhm":phone,
            "yddh":phone,
            "swjgDm":swjgDm,
            "jzdz":jsdz,
            "veryCode":imagecode,
            "dtm":""
                    }
        #https://dzswj.szds.gov.cn/dzswj/wykt.json?method=jszxyzKh&strRom=45700
        res=self.session.post("https://dzswj.szds.gov.cn/dzswj/wykt.json?method=getDtmJxzxKh&strRom="+strRom,data=data,headers=self.headers)
        if "手机动态码已经发送到手机" in res.text:
            item={}
            item["cookies"]=str(self.session.cookies.get_dict())
            item["strRom"]=strRom
            item=json.dumps(item)
            print(item)
            return 200
        else:
            return 100


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    phone=sys.argv[1]
    banktypenum=sys.argv[2]
    banknum=sys.argv[3]
    merChkBillSn=sys.argv[4]
    vertiyId=sys.argv[5]
    code=sys.argv[6]
    cookies=sys.argv[7]
    idcard=sys.argv[8]
    username=sys.argv[9]
    username=parse.unquote(username)
    swjgDm=sys.argv[10]
    jsdz=sys.argv[11]
    jsdz=parse.unquote(jsdz)

    szz=ShenZhenzhuce2()
    strRom=szz.zhuce(phone=phone,banktypenum=banktypenum,banknum=banknum,merChkBillSn=merChkBillSn,vertiyId=vertiyId,code=code,cookies=cookies)

    if strRom:
        try:
            num = 0
            while True:
                szz.getyzm()
                imagecode=szz.readcode(szz.imagename+".jpg")
                if imagecode:
                    res=szz.zhuce1(idcard=idcard, phone=phone, username=username, strRom=strRom, swjgDm=swjgDm, jsdz=jsdz, imagecode=imagecode)
                    if res==200:
                        break
                if num==20:
                    # 图片效验码识别错误
                    print(100)
                    break
                num+=1
        except Exception as e:
            print(500)