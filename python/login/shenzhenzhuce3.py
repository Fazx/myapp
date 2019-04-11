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
class ShenZhenzhuce4():

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

        #{"result":{"code":"0","msg":"手机动态码已经发送到手机156XXXXX00。","obj":"","resultlist":[]}}
        #{"result":{"code":"1","msg":"验证码不正确，请重新输入！(错误代码:9002003)","obj":"","resultlist":[]}}
        #https://dzswj.szds.gov.cn/dzswj/qyUserLogin.do?method=logout&fwbs=zrrLogin&kbcs=0.14100475848028804
    def getcookies(self,cookies):

        res = str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}

        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
    def getyzm(self):
        resp = self.session.get(
            "https://dzswj.szds.gov.cn/dzswj/forLoginCode.do?method=getCode&timestamp=" + self.nowtime,
            headers=self.headers)
        with open(self.imagename + ".jpg", "wb") as f:
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
    def zhuce2(self, idcard, phone, username, strRom, swjgDm, jsdz, imagecode, phonecode,cookies):
        res = str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}

        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)

        data = {
            "zjlxDm": "201",
            "sfzzhm": idcard,
            "rzsjhm": phone,
            "gjDm": "156",
            "xm": username,
            "checkFlag": "Y",
            "strRom": strRom,
            "jszxSjhm": phone,
            "yddh": phone,
            "swjgDm": swjgDm,
            "jzdz": jsdz,
            "veryCode": imagecode,
            "dtm": phonecode
        }
        # https://dzswj.szds.gov.cn/dzswj/wykt.json?method=jszxyzKh&strRom=45700
        res = self.session.post("https://dzswj.szds.gov.cn/dzswj/wykt.json?method=jszxyzKh&strRom=" + strRom,
                                data=data, headers=self.headers).json()

        return res["result"]
        # if res["result"]["code"]=="0":
        #     return 200
        # elif "校证码不正确" in res["result"]["msg"]:
        #     return 100
        # else:
        #     print(res["result"])
        #     return 400
        # resp = self.session.get(
        #     "https://dzswj.szds.gov.cn/dzswj/forLoginCode.do?method=getCode&timestamp=" + self.nowtime,
        #     headers=self.headers)
        # with open(self.imagename + ".jpg", "wb") as f:
        #     f.write(resp.content)
        # file = self.imagename + ".jpg"


if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    szz=ShenZhenzhuce4()
    idcard=sys.argv[1]
    phone=sys.argv[2]
    username=sys.argv[3]
    username=parse.unquote(username)
    strRom=sys.argv[4]
    swjgDm=sys.argv[5]
    jsdz=sys.argv[6]
    jsdz=parse.unquote(jsdz)
    phonecode=sys.argv[7]
    cookies=sys.argv[8]
    try:
        num=0
        while True:
            szz.getyzm()
            imagecode=szz.readcode(szz.imagename+".jpg")
            if imagecode:
                res=szz.zhuce2(idcard=idcard, phone=phone, username=username, strRom=strRom, swjgDm=swjgDm, jsdz=jsdz, imagecode=imagecode,phonecode=phonecode,cookies=cookies)
                if res["code"]=="0":
                    # 注册成功
                    print(200)
                    break
                else:
                    if "校证码不正确" in res["msg"]:
                        pass
                    else:
                        print(res["msg"])
                        break
            if num==20:
                # 验证码错误,脚本失败，跳转
                print("效验码不正确")
                break
            num+=1

    except Exception as e:
        print("请求超时")
