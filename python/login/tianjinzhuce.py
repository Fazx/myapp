import requests
import pytesseract
import re
import time
import os
import random
import json
import io
import sys
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from PIL import Image, ImageOps
from urllib import parse


class TianJingyzm():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }

    def __init__(self):
        self.session = requests.session()
        self.rname = str(int(random.random() * 10000000000000))
        self.nowtime = str(int(time.time() * 1000000))


    def yanzhengma1(self):
        res = self.session.get("https://itswt.tjsat.gov.cn/portals/web/captcha/captcha?t=0.33031739148675654",
                               headers=self.headers,verify=False)
        with open(self.rname+".jpg", "wb") as f:
            f.write(res.content)

    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save(self.rname + ".jpg")
        image = Image.open(self.rname + ".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 160)
        image = ImageOps.invert(image)
        image.save(self.rname + ".jpg")
        # image.show()
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
        code = pytesseract.image_to_string(image).replace(" ", "").replace("\\", "")[0:4]
        return code

    def yanzheng(self, code):
        data = {
            "captcha": code

        }
        res = self.session.post("https://itswt.tjsat.gov.cn/portals/web/captcha/validateCaptcha", data=data,
                                headers=self.headers, verify=False).json()
        return res["data"]

    def getcookies(self,cookies):
        if cookies=="0":
            print("请填写注册信息")
            return
        res=str(cookies)
        res = res.strip("{").strip("}")
        res = res.split(",")
        item1 = {}
        for i in res:
            resu = i.split(":")
            item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
    def zhuce(self, username, password, idcard, bankcard, phone, code, phonecode):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "Cookie": "JSESSIONID=v1gzb01FtRtLJbthPybGT9S4ZM25yjYVkDTnqQl8DdS8XN88LQJn!-394056994; sto-id-47873=FOAHBEKMFAAA; _gscu_949898263=42279209o5schj47; _gscbrs_949898263=1"
            "X-Requested-With": "XMLHttpRequest"
        }
        try:
            data = {"xm": username,
                    "sfzjhm": idcard,
                    "gjhdqdm": "156",
                    "yhkh": bankcard,
                    "sjhm": phone,
                    "sjyzm": phonecode,
                    "yzm": code,
                    "sftyxy": "true",
                    "sfzjlxDm": "201"}
            # https://itswt.tjsat.gov.cn/portals/web/register/verifyBankcardWithHlj
            res = self.session.post("https://itswt.tjsat.gov.cn/portals/web/register/verifyBankcardWithHlj", data=data,
                                    headers=headers, verify=False).json()
            if res["type"] == "ERROR":
                print(res["content"])
                return
            if "sfzjlxMc" not in res["data"]:
                print(res["data"])
                return

        except Exception as e:
            print("系统繁忙,请重新注册")
            return

        data1 = {
            "xm": username,
            "sfzjhm": idcard,
            "gjhdqdm": "156",
            "yhkh": bankcard,
            "sjhm": phone,
            "sjyzm": phonecode,
            "yzm": code,
            "sftyxy": "true",
            "sfzjlxDm": "201"
        }
        res = self.session.post("https://itswt.tjsat.gov.cn/portals/web/register/editBaseInfo", data=data1,
                                headers=self.headers)
        if username not in res.text:
            print("网络繁忙,请重新注册")
            return
        rsapubkey = re.search('id="st" data-param-rsapubkey="(.*?)"', res.text).group(1)
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json;charset=UTF-8"

        }
        mm = self.getmm(password, rsapubkey)
        data3 = {"mm": mm, "qrmm": password, "needSjhm": "", "st": ""}
        data3 = json.dumps(data3)
        res = self.session.post("https://itswt.tjsat.gov.cn/portals/web/register/registerUser", data=data3,
                                headers=head)
        if username in res.text:
            self.session.get("https://itswt.tjsat.gov.cn/portals/web/pwdProtect", headers=self.headers)
            print("注册成功")
        else:
            print("注册失败,请重新注册")

    def getmm(self, password, pubkey):
        with open(self.nowtime + '.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(pubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open(self.nowtime + '.txt', "r") as f:
            public_key = f.read()
            f.close()
        os.remove(self.nowtime + '.txt')
        password = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(password))
        cipher_text = cipher_text.decode("utf-8")
        return cipher_text


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    #姓名
    username=sys.argv[1]
    username=parse.unquote(username)
    #手机号
    phone=sys.argv[2]
    #密码
    password=sys.argv[3]
    #身份证号
    idcard=sys.argv[4]
    #银行卡号
    bankcard=sys.argv[5]
    # 手机验证码
    phonecode=sys.argv[6]
    cookies=sys.argv[7]
    # username = "贾浩"
    # phone = "15600461100"
    # password = "a8050980200"
    # idcard = ""
    # bankcard = "6228481000884523118"
    # phonecode="206288"
    # cookies="{'sto-id-47873': 'FNAHBEKMFAAA', 'JSESSIONID': 'yz3TcLGSdTkBCXln8S0GJht5GCwzTD4TdBxQT61HLsWsNT0Zhg8f!-1081633354'}"
    try:
        tjz = TianJingyzm()
        tjz.getcookies(cookies=cookies)
        num = 0
        while True:
            tjz.yanzhengma1()
            code = tjz.readcode(tjz.rname + ".jpg")
            data = tjz.yanzheng(code)
            if not data:
                os.remove(tjz.rname + ".jpg")
                break

            if num == 10:
                os.remove(tjz.rname + ".jpg")

                break
            num += 1
            os.remove(tjz.rname + ".jpg")

        tjz.zhuce(username=username, password=password, idcard=idcard, bankcard=bankcard, phone=phone, code=code,phonecode=phonecode)
    except Exception as e:
        print("网络错误,请重试")