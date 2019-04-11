import requests
import pytesseract
import os
import sys
import io
import json
import random
from PIL import Image,ImageOps,ImageEnhance

class AnHuizhuce():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }
    def __init__(self):
        self.ntime=str(int(random.random()*1000000000000))
        self.session=requests.session()
        self.rnum1=str(random.random())
        self.rnum2=str(random.random()*1000)
        self.rnum3 = str(random.random() * 100)

    def getimage(self):
        self.session.get("https://etax.ah-n-tax.gov.cn/anon/view/registerxx?userType=zrr&"+self.rnum1,headers=self.headers,verify=False)
        res=self.session.get("https://etax.ah-n-tax.gov.cn/anon/validateImgAndNum?randomNum="+self.rnum2,headers=self.headers,verify=False)
        with open(self.ntime+".jpg","wb") as f:
            f.write(res.content)
    def pretreat_image(self, image):
        image = ImageOps.invert(image)
        image.save( self.ntime+".jpg")
        image = Image.open(self.ntime+".jpg")
        image = image.convert("L")
        image = self.iamge2imbw(image, 230)
        image = ImageOps.invert(image)
        image.save(self.ntime+".jpg")
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
        code = pytesseract.image_to_string(image).replace(" ", "").replace("\\", "")[0:6]
        return code
    def check(self,idnum,imagecode):
        data={
            "zclxdm":"zrr",
            "code":imagecode,
            "nsrsbh":idnum
                    }
        res=self.session.post("https://etax.ah-n-tax.gov.cn/anon/register/checkNsrsbh?"+self.rnum1,data=data,headers=self.headers,verify=False).json()
        if not res["data"]:
            if res["message"]:

                return 3
            else:

                return 100
        if "uuid" in res["data"]:
            uuid=res["data"]["uuid"]
        #{'code': 442, 'error': '', 'data': '', 'message': '请输入正确的图片验证码!', 'encrypType': '', 'encrypKey': '', 'encrypData': '', 'userToken': '', 'invalidArgs': ''}
        #{'code': 200, 'error': '', 'data': {'uuid': 'fb1ea488e7e441549eb0fd34b10781e1'}, 'message': '', 'encrypType': '', 'encrypKey': '', 'encrypData': '', 'userToken': '', 'invalidArgs': ''}
        #{'code': 200, 'error': '', 'data': {}, 'message': '', 'encrypType': '', 'encrypKey': '', 'encrypData': '', 'userToken': '', 'invalidArgs': ''}
            self.session.get("https://etax.ah-n-tax.gov.cn/anon/view/zrrSubmit?uuid="+uuid+"&userType=zrr",headers=self.headers)
            res=self.session.get("https://etax.ah-n-tax.gov.cn/anon/validateImgAndNum?randomNum="+self.rnum3,headers=self.headers)
            with open(self.ntime+".jpg","wb") as f:
                f.write(res.content)
            return uuid
        return 300
    def phonecode(self,phone,imagecode2,resp):
        data={
            "zclxdm":"zrr",
            "tel":phone,
            "tpyzm":imagecode2
                    }
        res=self.session.post("https://etax.ah-n-tax.gov.cn/anon/register/sendDxyzm?"+self.rnum1,data=data,headers=self.headers).json()
        if not res["message"]:
            item={}
            item["uuid"]=resp
            item["cookies"]=str(self.session.cookies.get_dict())
            item=json.dumps(item)
            print(item)
            return 200
        if res["message"]=="短信发送失败":
            return 400
        if res["message"]=="请输入正确的图片验证码!":
            return 3
        return res["message"]
        #{"code":442,"error":"","data":"","message":"请输入正确的图片验证码!","encrypType":"","encrypKey":"","encrypData":"","userToken":"","invalidArgs":""}
        #{"code":200,"error":"","data":"","message":"","encrypType":"","encrypKey":"","encrypData":"","userToken":"","invalidArgs":""}
        #{"code":503,"error":"","data":"","message":"短信发送失败","encrypType":"","encrypKey":"","encrypData":"","userToken":"","invalidArgs":""}


        #{"code":442,"error":"","data":"","message":"请输入正确的图片验证码!","encrypType":"","encrypKey":"","encrypData":"","userToken":"","invalidArgs":""}
if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    idnum=sys.argv[1]
    phone=sys.argv[2]
    # idnum="130705198912281569"
    # #phone="15611570802"
    # phone="15600461100"
    ahz=AnHuizhuce()
    num=0
    while True:
        ahz.getimage()
        imagecode=ahz.readcode(ahz.ntime+".jpg")
        res=ahz.check(idnum,imagecode)
        if res==3:
            continue
        if res==100:
            print("身份份证号错误")
            os.remove(ahz.ntime + ".jpg")
            break
        if res==300:
            print("证件号已注册")
            os.remove(ahz.ntime + ".jpg")
            break
        imagecode2 = ahz.readcode(ahz.ntime + ".jpg")
        result=ahz.phonecode(phone,imagecode2,res)
        if result==3:
            continue
        if result==200:
            os.remove(ahz.ntime + ".jpg")
            break
        if result==400:
            print("验证码发送错误,请检查手机号")
            os.remove(ahz.ntime + ".jpg")
            break
        if result:
            os.remove(ahz.ntime + ".jpg")
            print(result)
            break
        if num ==30:
            print("验证码错误")
            os.remove(ahz.ntime + ".jpg")
            break
        num+=1