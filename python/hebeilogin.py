import requests
import base64
import re
import time
import sys
import io
import json
import binascii
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class HeBei():

    session =requests.session()
    ntime = str(int(time.time() * 10000000))
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    def pk(self):

        resp = self.session.get(
            "https://ybs.he-n-tax.gov.cn:8888/login-web/login?service=https%3A%2F%2Fybs.he-n-tax.gov.cn%3A8888%2Fbase%2FgetRsaPublicKey.do",
            verify=False,headers=self.headers)
        self.session.get('https://ybs.he-n-tax.gov.cn:8888/login-web/auth/validServerTime.do?clientTime=2018-10-11',headers=self.headers)
        lt = re.search('name="lt" value="(.*?)"', resp.text).group(1)
        execution = re.search('name="execution" value="(.*?)"', resp.text).group(1)
        res = self.session.get("https://ybs.he-n-tax.gov.cn:8888/login-web/captcha.jpg?0.3556666066059264",
                           verify=False,headers=self.headers)
        cname = self.ntime + ".jpg"
        with open(cname, "wb") as f:
            f.write(res.content)


        #resp=self.session.post("https://ybs.he-n-tax.gov.cn:8888/login-web/login?service=https%3A%2F%2Fybs.he-n-tax.gov.cn%3A8888%2F%2520base%2520%2F%2520getRsaPublicKey.do",headers=self.headers,verify=False)
        #print(resp.text)
        respon = self.session.get("https://ybs.he-n-tax.gov.cn:8888/login-web/base/getRsaPublicKey.do",verify=False,headers=self.headers).json()
        pubkey=respon["data"]["pk"]
        return pubkey,lt,execution
    def getmm(self, password, pubkey):
        with open('text.txt', 'w') as f:
            f.write("-----BEGIN PUBLIC KEY-----" + "\n")
            f.write(pubkey + "\n")
            f.write("-----END PUBLIC KEY-----")
        with open('text.txt', "r") as f:
            public_key = f.read()
            f.close()
        password = password.encode("utf-8")
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        sign=cipher.encrypt(password)
        cipher_text = binascii.b2a_hex(sign)
        # print(ret)
        # cipher_text = base64.b64encode(cipher.encrypt(password))
        # print(cipher_text)
        cipher_text = cipher_text.decode("utf-8")
        return cipher_text
    def login(self,username,password,lt,execution,code,cookies):
        #cookies=json.loads(cookies)
        #print(cookies)
        headers={
            'Referer': 'https://ybs.he-n-tax.gov.cn:8888/login-web/login',
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Cookie":cookies
        }
        data={
            "userName":username,
            "passWord":password,
            "single":"",
            "authencationHandler":"UsernamePasswordAuthencationHandler",
            "lt":lt,
            "_eventId":"submit",
            "execution":execution,
            "captchCode":code,
            "qd":""
        }
        res=self.session.post("https://ybs.he-n-tax.gov.cn:8888/login-web/login",headers=headers,data=data,verify=False)
        res.encoding="utf-8"
        res=self.session.post("https://ybs.he-n-tax.gov.cn:8888/login-web/auth/checkLoginState.do",headers=headers,verify=False)
        print(res.text)

if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(sys.argv)
    username=sys.argv[1]
    password = sys.argv[2]
    lt = sys.argv[3]
    execution = sys.argv[4]
    code = sys.argv[5]
    pubkey = sys.argv[6]
    cookies = sys.argv[7]

    hb=HeBei()
    # pub=hb.pk()
    # print(pub)
    # pubkey=pub[0]
    # lt=pub[1]
    # execution=pub[2]
    #
    # name="131025198706200076"
    # password="a8050980200"

    name=hb.getmm(username,pubkey)
    password=hb.getmm(password,pubkey)
    hb.login(name,password,lt,execution,code,cookies)




