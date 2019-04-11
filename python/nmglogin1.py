import requests
import re
import json
import time
import datetime
import random
import os
import sys
import io
import base64
import pytesseract
from urllib import parse
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from PIL import Image, ImageOps


class NeiMengGu():
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))
    session = requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    filename=str(int(random.random()*10000000000000))
    ntime = str(int(time.time() * 100000))
    nowtime = str(int(time.time() * 1000))
    cardtypes = {
        "身份证": "201",
        "军官证": "202",
        "武警警官证": "203",
        "士兵证": "204",
        "外国护照": "208",
        "港澳居民来往内地通行证": "210",
        "台湾居民来往大陆通行证": "213",
        "香港身份证": "219",
        "台湾身份证": "220",
        "澳门身份证": "221",
        "中国护照": "227",
        "外国人永久居留证": "233"
    }

    def getlt(self):
        res = self.session.get(
            "https://csfw.nmds.gov.cn/portals/web/loginForNmsw", headers=self.headers, verify=False)

        lt = re.search('data-param-rsapubkey="(.*?)" data-param-token="(.*?)">', res.text)
        execution = lt.group(1)
        lt = lt.group(2)
        return execution, lt

    def getyzm(self, lt):
        res = self.session.get(
            "https://csfw.nmds.gov.cn/portals/web/captcha/refreshCaptcha?t=0.24949178832857077&token=" + lt[1],
            headers=self.headers, verify=False)
        with open(self.ntime + ".jpg", "wb") as f:
            f.write(res.content)
            f.close()

    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save(self.ntime + ".jpg")
        image = Image.open(self.ntime + ".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 160)
        image = ImageOps.invert(image)
        image.save(self.ntime + ".jpg")
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

    def getmm(self, password, pubkey):
        with open(self.ntime + '.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(pubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open(self.ntime + '.txt', "r") as f:
            public_key = f.read()
            f.close()
        os.remove(self.ntime + '.txt')
        password = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(password))
        cipher_text = cipher_text.decode("utf-8")
        return cipher_text

    def login(self,  name, mm, code):
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        data = {"yhm": name, "idType": "201", "idNumber":"", "mm": mm, "authCode": code,
                "redirect_uri": "", "response_type": "", "client_id": "", "sign": "", "st": "", "dllx": "yhm"}
        data = json.dumps(data)
        # https://csfw.nmds.gov.cn/portals/web/oauth2/login
        res = self.session.post("https://csfw.nmds.gov.cn/portals/web/oauth2/login", data=data, headers=headers).json()

        if res["type"]=="ERROR":
            if "账户不存在" in res["content"]:
                return 100
            if "身份证件号码或密码错误" in res["content"]:
                return 300
            if "锁" in res["content"]:
                return 400
            if "验证码错误" in res["content"]:
                return 3
        data = {"url": "https://csfw.nmds.gov.cn/portals/web/biz/home"}
        res = self.session.post("https://csfw.nmds.gov.cn/portals/web/oauth2/afterLoginRedirect", data=data,
                                headers=self.headers, verify=False)
        # https://csfw.nmds.gov.cn/portals/web/oauth2/afterLoginRedirect
        res = self.session.get("https://csfw.nmds.gov.cn/portals/web/biz/home", headers=self.headers, verify=False)
        uname = re.search('<span id="current-user-name">(.*?)<', res.text, re.S)
        if uname:
            return uname.group(1).strip()
        else:
            return 600

    def detail(self, uname):

        for j in range(2006, self.atime + 1):
            data = {
                "skssqq": str(j) + "-01-01",
                "skssqz": str(j) + "-12-31",
                "kjfwjg": "21500000000",
               # "pzkjzl": "Z99001002",
                "_": self.nowtime
            }
            res = self.session.get("https://csfw.nmds.gov.cn/wsz-ww-web/web/taxInfo/search", params=data,
                                   headers=self.headers).json()
            if res["data"]:
                djxh = res["data"][0]["djxh"]
                lists = res["data"]
                data = {
                    "skssqq": str(j) + "-01-01",
                    "skssqz": str(j) + "-12-31",
                    "kjfwjg": "21500000000",
                    "sendEmail": "false",
                    "sbfs": "[]",
                    "kjqy": "[]"
                }
                res = self.session.post("https://csfw.nmds.gov.cn/wsz-ww-web/web/taxInfo/applyMakeNsqd", data=data,
                                        headers=self.headers).json()
                if res["data"]:
                    self.session.get("https://csfw.nmds.gov.cn/wsz-ww-web/web/taxBill?autoSearch=true",
                                     headers=self.headers)
                    nums = 0
                    while True:
                        times = str(int(time.time() * 1000 + 100))
                        res = self.session.get(
                            "https://csfw.nmds.gov.cn/wsz-ww-web/web/taxBill/search?fromDate=" + self.startime() + "&toDate=" + self.endtime() + "&_=" + times).json()
                        if res["data"][0]["zzztMc"] == "制作成功":
                            num = res["data"][0]["nsqdxh"]
                            res = self.session.get(
                                "https://csfw.nmds.gov.cn/wsz-ww-web/web/taxBill/download/" + str(num))
                            fname = str(j) + self.filename + ".pdf"
                            with open("/home/wwwroot/wbsr/python/files/"+fname, "wb") as f:
                                f.write(res.content)
                                break
                        if nums == 3:
                            fname = ""
                            break
                        time.sleep(2)
                        nums += 1
                    item = {}
                    item["name"] = uname
                    item["year"] = str(j)
                    item["fname"] = fname
                    item["lists"] = lists
                    item = json.dumps(item)
                    print(item)

    def startime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-7)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d %H:%M:%S')
        timeArray = time.strptime(n_days, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        timeArray = time.localtime(timestamp)
        nowtime = time.strftime("%Y-%m-%d", timeArray)
        return nowtime

    def endtime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(hours=1)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d %H:%M:%S')
        timeArray = time.strptime(n_days, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        timeArray = time.localtime(timestamp)
        nowtime = time.strftime("%Y-%m-%d", timeArray)
        return nowtime


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    name=sys.argv[1]
    password=sys.argv[2]
    # name = "wangyu_nm"
    # password = "23032X"
    # 100 账户不存在
    # 300 密码错误
    # 400 账户已被锁定,请30分钟后登录
    # 500 脚本错误
    # 600 未知错误
    # 3 验证码错误
    try:
        nmg = NeiMengGu()
        token = nmg.getlt()
        num = 0
        while True:
            nmg.getyzm(lt=token)
            mm = nmg.getmm(password, token[0])
            code = nmg.readcode(nmg.ntime + ".jpg")
            if code:
                os.remove(nmg.ntime + ".jpg")
                uname = nmg.login(name, mm, code)
                if uname == 100:
                    print(100)
                    break
                elif uname == 300:
                    print(300)
                    break
                elif uname == 3:
                    continue
                elif uname == 400:
                    print(uname)
                    break
                elif uname == 600:
                    print(600)
                    break
                else:
                    nmg.detail(uname)
                    break
            num += 1
            if num == 10:
                print(3)
                os.remove(nmg.ntime + ".jpg")
                break
    except Exception as e:
        print(e)






