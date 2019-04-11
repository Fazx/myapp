import requests
import base64
import json
import pytesseract
import sys
import io
import time
import os
import datetime
import re
from PIL import Image, ImageOps
from urllib import parse
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class ShanXi():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    session = requests.session()
    ntime = str(int(time.time() * 1000000))
    nowtime = str(int(time.time() * 1000))
    timeArray = time.localtime(time.time())
    atime = int(time.strftime("%Y", timeArray))

    def getoken(self):
        res = self.session.get("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/loginForDzswj", headers=self.headers,verify=False)
        html = res.text
        token = re.search('data-param-rsapubkey="(.*?)".*data-param-token="(.*?)"', html,re.S)
        rsapubkey = token.group(1)
        token = token.group(2)
        return rsapubkey, token

    def getyzm(self, token):
        res = self.session.get(
            "https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/captcha/refreshCaptcha?t=0.9968048201575341&token=" + token,
            headers=self.headers)
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
        code = code.replace("?", "7")
        return code

    def verifycode(self, code):
        data = {"captcha": code}
        res = self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/captcha/validateCaptcha", data=data,
                                headers=self.headers).json()
        return res["data"]

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

    def login(self, name, mm, code):
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        data = {"yhm": name, "idType": "201", "idNumber": "", "mm": mm, "authCode": code, "redirect_uri": "",
                "response_type": "", "client_id": "", "sign": "", "st": "", "dllx": "yhm"}
        data = json.dumps(data)
        res=self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/oauth2/login", data=data, headers=headers).json()
        if res["type"] =="ERROR":
            if "密码" in res["content"]:
                print(200)
                return 
            elif "锁" in res["content"]:
                print(400)
                return
            else:
                print(300)
                return
        res = self.session.get("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/biz/home", headers=self.headers,verify=False)
        self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/portals/web/biz/getSt", headers=self.headers)
        name = re.search('<span id="current-user-name">(.*?)<', res.text,re.S)
        #print(name)
        if name:
            return name.group(1).strip()
        else:
            print(100)
            return
    def detail(self, uname):

        for i in range(2007, self.atime + 1):
            try:
            # resp=self.session.get("https://zrrwt.jl-n-tax.gov.cn:10803/wsz-ww-web/web/base/code/list/DM_GY_SRLYSWJG",headers=self.headers).json()
            # res=self.session.post("https://zrrwt.jl-n-tax.gov.cn:10803/wsz-ww-web/web/wszm/getPzkjzl",headers=self.headers).json()
                res = self.session.get(
                    "https://zrrwt.sx-n-tax.gov.cn:8082/wsz-ww-web/web/wszm/mxcxForGdshb?skssqq=" + str(
                        i) + "-01-01&skssqz=" + str(i) + "-12-31&kjfwSwjg=21400000000&pzkjzl=Z99001002&_=" + self.nowtime,
                    headers=self.headers).json()
                if res["data"]["skmxs"]:
                    djxh = res["data"]["skmxs"][0]["djxh"]
                    lists = res["data"]["skmxs"]
                    item_list = []
                    num = 0
                    for item in res["data"]["skmxs"]:
                        item["checked"] = True
                        item["_uid"] = num
                        item["_index"] = num
                        num += 1
                        item_list.append(item)
                    item_list = str(item_list)
                    item_list = item_list.replace("None", "null").replace("'", '"').replace(" ", "").replace("True",
                                                                                                             "true").replace(
                        "False", "false")
                    data1 = {
                        "skssqq": str(i) + "-01-01",
                        "skssqz": str(i) + "-12-31",
                        "kjfwSwjg": "21400900000",
                        "pzkjzl": "Z99001002",
                        "nsmxs": item_list
                    }
                    headers = {
                        #"Host": "zrrwt.sxs-l-tax.gov.cn:8080",
                        "Connection": "keep-alive",
                        #"Origin": "http://zrrwt.sxs-l-tax.gov.cn:8080",
                        "X-Requested-With": "XMLHttpRequest",
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        #"Referer": "http://zrrwt.sxs-l-tax.gov.cn:8080/wsz-ww-web/web/wszm?"

                    }
                    res = self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/wsz-ww-web/web/wszm/wszmSq", data=data1,
                                            headers=headers)
                    # print(res.text)

                    time.sleep(3)

                    data2 = {"tfrqq": self.startime(), "tfrqz": self.endtime(), "pzkjzl": "Z99001002", "pageIndex": 0,
                             "pageSize": 10}
                    data2 = json.dumps(data2)
                    head = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                        "Content-Type": "application/json;charset=UTF-8"
                    }
                    res = self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/wsz-ww-web/web/ysqwszm/ysqwszmCx",
                                            data=data2, headers=head).json()

                    dzwszcymw = res["data"]["records"][0]["dzwszcymw"]
                    pzhm = res["data"]["records"][0]["pzhm"]

                    data3 = {
                        "djxh": djxh,
                        "pzzlDm": "Z99001002",
                        "pzPcZg": "(180)晋地证明",
                        "pzhm": pzhm,
                        "dzwszcymw": dzwszcymw
                    }
                    res = self.session.post("https://zrrwt.sx-n-tax.gov.cn:8082/wsz-ww-web/web/ysqwszm/downloadWszm",
                                            data=data3, headers=self.headers)
                    fname = str(i) + self.ntime + ".pdf"
                    with open("/home/wwwroot/wbsr/python/files/" + fname, "wb") as f:
                        f.write(res.content)
                    item = {}
                    item["year"] = str(i)
                    item["name"] = uname
                    item["fname"] = str(i) + self.ntime + ".pdf"
                    item["lists"] = lists
                    item = json.dumps(item)
                    print(item)
            except:
                pass
    def startime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-30)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d %H:%M:%S')
        timeArray = time.strptime(n_days, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        timeArray = time.localtime(timestamp)
        nowtime = time.strftime("%Y-%m-%dT %H:%M:%S.658Z", timeArray)
        return nowtime

    def endtime(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(hours=3)
        n_days = now + delta
        n_days = n_days.strftime('%Y-%m-%d %H:%M:%S')
        timeArray = time.strptime(n_days, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        timeArray = time.localtime(timestamp)
        nowtime = time.strftime("%Y-%m-%dT %H:%M:%S.658Z", timeArray)
        return nowtime
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    name = sys.argv[1]
    name = parse.unquote(name)
    password = sys.argv[2]
    # jsnum=sys.argv[3]
    # name="孟天羊"
    # password="heixiu110"
    sx = ShanXi()
    tokens = sx.getoken()
    num = 0
    while True:
        sx.getyzm(tokens[1])
        code = sx.readcode(sx.ntime + ".jpg")
        data = sx.verifycode(code)
        num += 1
        if not data:
            os.remove(sx.ntime + ".jpg")
            break
        os.remove(sx.ntime + ".jpg")
        if num == 5:
            print("验证码错误")
            break
    mm = sx.getmm(password, tokens[0])
    uname = sx.login(name, mm, code)
    if uname:
        sx.detail(uname)
    else:
        pass
