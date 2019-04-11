import requests
import time
import json
import re
import random
import pymysql
import logging
import os
from lxml import etree
import pytesseract
from PIL import Image,ImageOps,ImageEnhance
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename="/home/wwwlogs/python/leshuiszlog.txt")
logger = logging.getLogger(__name__)
class Leshui():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    header={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",

    }
    leixing={'城镇土地使用税': pymysql.escape_string('["2","7","15","126"]'), '个人所得税': pymysql.escape_string('["2","7","15","127"]'), '增值税':pymysql.escape_string('["2","7","15","128"]'), '企业所得税': pymysql.escape_string('["2","7","15","129"]'), '城市维护建设税': pymysql.escape_string('["2","7","15","130"]'), '车辆购置税': pymysql.escape_string('["2","7","15","131"]'), '车船税': pymysql.escape_string('["2","7","15","132"]'), '消费税': pymysql.escape_string('["2","7","15","133"]'), '房产税': pymysql.escape_string('["2","7","15","134"]'), '社保': pymysql.escape_string('["2","7","15","135"]'), '印花税': pymysql.escape_string('["2","7","15","136"]'), '契税': pymysql.escape_string('["2","7","15","137"]'), '出口退税（后台）': pymysql.escape_string('["2","7","15","138"]'), '关税（后台）': pymysql.escape_string('["2","7","15","139"]'), '遗产税（后台）': pymysql.escape_string('["2","7","15","140"]')}
    notime = str(int(time.time()))
    def __init__(self):
        self.session=requests.session()
        self.nowtime=str(int(time.time()*1000))

    def getindex(self):
        self.session.get("https://www.leshui365.com/components/sso-login/loginsuccesspath?_="+self.nowtime,verify=False)
        self.session.get("https://uc.leshui365.com/?system=leshui-2.1&stylesheet=https://cdn2.leshui365.com/fdp_ls2/s_p/components/sso-login/dialog_e52033c.css&logintype=pc-with-thirdparty",verify=False)
        self.session.get("https://www.leshui365.com/servlet/webServlet?serviceName=app.service.commonService&methodName=getUser&requestJson=%7B%7D",verify=False)

    def getyzm(self):
        res=self.session.get("https://uc.leshui365.com/vcode_2_0_0?0.5787612490442933")
        with open(self.nowtime+".png","wb") as f:
            f.write(res.content)

    def readcode(self):
        image = Image.open(self.nowtime+".png")
        image = image.convert('L')
        image = self.iamge2imbw(image, 195)
        # image=image.resize((120, 40), Image.ANTIALIAS)
        # image.show()
        # image.save("text.png")
        # image=Image.open("text.png")
        image=self.pIx(image)
        image = image.resize((120, 30), Image.ANTIALIAS)
        image=self.pIx(image)
        code=pytesseract.image_to_string(image).replace(" ","")[0:4].replace(".","")
        return code
    def iamge2imbw(self,image, threshold):
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



    # image=pytesseract.image_to_string(image)
    # print(image)

    def pIx(self,image):

        """传入二值化后的图片进行降噪"""
        pixdata = image.load()
        w, h = image.size
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                count = 0
                if pixdata[x, y - 1] > 245:  # 上
                    count = count + 1
                if pixdata[x, y + 1] > 245:  # 下
                    count = count + 1
                if pixdata[x - 1, y] > 245:  # 左
                    count = count + 1
                if pixdata[x + 1, y] > 245:  # 右
                    count = count + 1
                if pixdata[x - 1, y - 1] > 245:  # 左上
                    count = count + 1
                if pixdata[x - 1, y + 1] > 245:  # 左下
                    count = count + 1
                if pixdata[x + 1, y - 1] > 245:  # 右上
                    count = count + 1
                if pixdata[x + 1, y + 1] > 245:  # 右下
                    count = count + 1
                if count > 4:
                    pixdata[x, y] = 255

        return image

        #
        # w = image.size[0]
        # h = image.size[1]
        #
        # # data.getpixel((x,y))获取目标像素点颜色。
        # # data.putpixel((x,y),255)更改像素点颜色，255代表颜色。
        #
        # try:
        #     for x in range(1, w - 1):
        #         if x > 1 and x != w - 2:
        #             # 获取目标像素点左右位置
        #             left = x - 1
        #             right = x + 1
        #
        #         for y in range(1, h - 1):
        #             # 获取目标像素点上下位置
        #             up = y - 1
        #             down = y + 1
        #
        #             if x <= 2 or x >= (w - 2):
        #                 data.putpixel((x, y), 255)
        #
        #             elif y <= 2 or y >= (h - 2):
        #                 data.putpixel((x, y), 255)
        #
        #             elif data.getpixel((x, y)) == 0:
        #                 if y > 1 and y != h - 1:
        #                     # 以目标像素点为中心点，获取周围像素点颜色
        #                     # 0为黑色，255为白色
        #                     up_color = data.getpixel((x, up))
        #                     down_color = data.getpixel((x, down))
        #                     left_color = data.getpixel((left, y))
        #                     left_down_color = data.getpixel((left, down))
        #                     right_color = data.getpixel((right, y))
        #                     right_up_color = data.getpixel((right, up))
        #                     right_down_color = data.getpixel((right, down))
        #
        #                     # 去除竖线干扰线
        #                     if down_color == 0:
        #                         if left_color == 255 and left_down_color == 255 and right_color == 255 and right_down_color == 255:
        #                             data.putpixel((x, y), 255)
        #
        #                     # 去除横线干扰线
        #                     elif right_color == 0:
        #                         if down_color == 255 and right_down_color == 255 and up_color == 255 and right_up_color == 255:
        #                             data.putpixel((x, y), 255)
        #
        #                 # 去除斜线干扰线
        #                 if left_color == 255 and right_color == 255 and up_color == 255 and down_color == 255:
        #                     data.putpixel((x, y), 255)
        #             else:
        #                 pass
        #
        #             # 保存去除干扰线后的图片
        #
        #             data.save("test.png", "png")
        #
        # except:
        #     return False


    def verifycode(self,code):
        data={
            "j_authcode":code
        }
        res=self.session.post("https://uc.leshui365.com/vcode_2_0_0",data=data).json()
        return res["isValid"]
    def login(self,code):
        # if cookies=="0":
        #     print("请填写注册信息")
        #     return
        # res=str(cookies)
        # res = res.strip("{").strip("}")
        # res = res.split(",")
        # item1 = {}
        # for i in res:
        #     resu = i.split(":")
        #     item1[resu[0].strip(" ").strip("'").strip('"')] = resu[1].strip(" ").strip("'").strip('"')
        # requests.utils.add_dict_to_cookiejar(self.session.cookies, item1)
        data={
            'serviceName':'portal.login.loginService',
            'methodName':'validatePassword_2_0_0',
            'requestJson':'{"userName":"15600461100","password":"a8050980200"}'
        }

        res=self.session.post("https://uc.leshui365.com/ajax",data=data,headers=self.header,verify=False).json()

        if res["RtnCode"]=="00":
            head={
                #"Host": "www.leshui365.com",
                #"Connection": "keep-alive",
                #"Content-Length": "87",
                #"Cache-Control": "max-age=0",
                #"Origin": "https://uc.leshui365.com",
                #"Upgrade-Insecure-Requests": "1",
                #"Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                #"Referer": "https://uc.leshui365.com/?system=leshui-2.1&stylesheet=https://cdn2.leshui365.com/fdp_ls2/s_p/components/sso-login/dialog_e52033c.css&logintype=pc-with-thirdparty",
                #"Accept-Encoding": "gzip, deflate, br",
                #"Accept-Language": "zh-CN,zh;q=0.9"
                #"Cookie": "Hm_lvt_d00d983c6548bd4a544f7f704be26621=1547785551; LSID=6AF38C3111BA64131B3B6CD7E5A44EF8-n1; CASTGC=TGT-36990-RbjMskL0r4vwJVncT3kT5drs0kgT6SxQ1iYJaxS0JyzGwcNr26-cas01.example.org; LBLS2.1ID=2b12987ee98eaa241d1f84f770d77939; ucenter.leshui.sid=s%3AK0eMGvTl50OtNYAK57HxJJK290BB4JIH.UxWUb1GUOm%2BMPq5utA1B2qDpKppfU14FBkngctJmFMg; LBLSINFOID=c29fda5a6a5a400630c30564d440766c; LBLSID=6becf3b85920e139774092c09dbc30db; SERVERID=4f1a6e744b2e5ffc178172660d2942b8|1548054304|1548054267"
            }
            data={
                "username":"15600461100",
                "j_username":"15600461100",
                "password":"a8050980200",
                "j_password":"a8050980200"
            }
            self.session.post("https://www.leshui365.com/servlet/loginServlet",data=data,headers=head,verify=False)

            self.session.get("https://www.leshui365.com/static/api/js/share.js?v=89860593.js?cdnversion=430014")
            data={
                "serviceName":"app.service.commonService",
                    "methodName":"getUser",
                    "requestJson":"{}"
            }
            self.session.post("https://www.leshui365.com/servlet/webServlet",data=data)
            data={
                "serviceName":"cart.service.goods.goodsService",
                "methodName":"getCartGoodsNumber",
                "requestJson":'{"cartId":"null"}'
            }

            # heade={
            #     "Referer": "https://www.leshui365.com/loginsuccess.html"
            # }
            self.session.post("https://www.leshui365.com/servlet/webServlet",data=data)
            self.session.get("https://www.leshui365.com/")
            data={
                "username":"15600461100",
                "password":"a8050980200",
                "j_authcode":code,
                "system":"leshui-2.1",
                "logintype":"pc-with-thirdparty"
            }
            head={
            "Host": "uc.leshui365.com",
            "Cache-Control": "max-age=0",
            "Origin": "https://uc.leshui365.com",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer": "https://uc.leshui365.com/?system=leshui-2.1&stylesheet=https://cdn2.leshui365.com/fdp_ls2/s_p/components/sso-login/dialog_e52033c.css&logintype=pc-with-thirdparty",

            }
            res=self.session.post("https://uc.leshui365.com/2.0.0",data=data,headers=head,verify=False,allow_redirects=False)

            url=re.search('(https.*)"',res.text).group(1)

            head={
            "Host": "www.leshui365.com",
            "Referer": "https://uc.leshui365.com/?system=leshui-2.1&stylesheet=https://cdn2.leshui365.com/fdp_ls2/s_p/components/sso-login/dialog_e52033c.css&logintype=pc-with-thirdparty",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",

            }
            self.session.get(url,headers=head)
            self.session.get("https://www.leshui365.com/components/login/sessionack?_="+self.nowtime,verify=False)
            self.session.get("https://www.leshui365.com/law/kfg18515018.html")

            return "登录成功"
        else:
            logging.info(res)


    def indexs(self):
        #requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)
        data={"service":"kbs.service.article.articleSearchService","method":"buildLeftTree","data":{"articleType":"001","type":"1","keyword":"","terms":"","filter_class":"","filter_area":"articleArea|全国|156","filter_industry":"","filter_validity":"","tag":"","title":"","number":"","content":"","filter_unit":"","time1":"","time2":""}}
        data=json.dumps(data)
        #print(self.session.cookies.get_dict())
        res=self.session.post("https://www.leshui365.com/ajax",data=data,headers=self.headers,verify=False).json()
        # for i,j in res.items():
        #     print(i,j)
        return res

    def getsindex(self,res):
        lists=[]
        for index,i in enumerate(res["classNodes"]):
            if i["pId"]=="001":
                zhonglei = i["name"]
                zhonglei = re.search('(.*?)\(', zhonglei).group(1)
                if zhonglei in self.leixing:
                    lists.append(i)
        
        return lists

    def getpage(self,lists):
       # print(lists)

        for j in lists:
            item = {}
            zhonglei=j["name"]
            zhonglei=re.search('(.*?)\(',zhonglei).group(1)
            id=j["id"]
            # area=j["click"].replace("navigateArea('","").replace("')","")
            # item["id"]=id
            # item["city"]=city
            # item["area"]=area
            #https://www.leshui365.com/law/c001025/?s10-new.html
            res=self.session.get("https://www.leshui365.com/law/c"+id+"-v0/?s10-new.html",headers=self.header,verify=False)
            html=etree.HTML(res.text)
            urls=html.xpath('.//div[@class="list-content"]//ul//p[@class="title"]/a/@href')
            for url in urls:
                time.sleep(0.3)
                try:
                    res=self.session.get("https://www.leshui365.com"+url,headers=self.header,verify=False)
                    detail_item=self.detail(res)
                    detail_item["type_list"]=self.leixing[zhonglei]
                    detail_item["type_name"]="法规库,全部法规,税种分类,"+zhonglei
                   # print(detail_item)
                    Db = Dbmysql()
                    res = Db.dbs(detail_item)
                    if res == 0:
                        db = dbmysql()
                        db.dbs(detail_item)

                except Exception as e:
                    logging.info(e)
            #链接页
    def detail(self,res):
        try:
            html=etree.HTML(res.text)
            title=html.xpath('.//div[@class="list-content detail-file"]/p[@class="title"]/text()')[0]
            content=re.findall('<div class="content-detaill">(.*?)</div>',res.text,re.S)[0]
            date=html.xpath('.//div[@class="nubcode"]/span[3]/text()')[0]
            uid = str(int(random.random() * 1000000000000))
            item={}
            item["library"] = pymysql.escape_string('[\"5\"]')
            item["url"] = res.url
            item["title"] = title
            item["content"] = content.replace('"',"'").replace("&ldquo;","").replace("&rdquo;","").replace("&lsquo;","").replace("&rsquo;","").replace("&ensp;","").replace("&hellip;","").replace("&mdash;","").replace("\r\n","")
            item["describes"] = title
            item["type"] = pymysql.escape_string('[\"44\"]')
            item["column_list_id"] = pymysql.escape_string('[\"97\"]')
            item["need_login"] = 0
            item["date"] = date
            item["uid"] = uid
            item["create_time"] = self.notime
            item["update_at"] = self.notime
            item["source"]="乐税网"
            return item
        except Exception as e:
            logging.info(e)

class dbmysql():

    def __init__(self):
        self.db=pymysql.connect(host ="localhost",user="root",passwd="jKN09L_",db="hssj",charset = "utf8")
        self.cursor=self.db.cursor()
    def dbs(self,item):

        sql='insert into news(url,title,type_list,type_name,content,describes,type,column_list_id,need_login,date,uid,library,create_time,source) values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}")'.format(item["url"],item["title"],item["type_list"],item["type_name"],item["content"],item["describes"],item["type"],item["column_list_id"],item["need_login"],item["date"],item["uid"],item["library"],item["create_time"],item["source"])
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("插入成功")
        except Exception as e:
            logging.info(e)
            self.db.rollback()
        self.db.close()
class Dbmysql():

    def __init__(self):
        self.db=pymysql.connect(host ="localhost",user="root",passwd="jKN09L_",db="hssj",charset = "utf8")
        self.cursor=self.db.cursor()
    def dbs(self,item):
        sql='insert into news_python_log(url,title,type_list,type_name,content,describes,type,column_list_id,need_login,date,uid,library,create_time,source) values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}")'.format(item["url"],item["title"],item["type_list"],item["type_name"],item["content"],item["describes"],item["type"],item["column_list_id"],item["need_login"],item["date"],item["uid"],item["library"],item["create_time"],item["source"])
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("成功")
            return 0
        except Exception as e:
            print(e)
            logging.info(e)
            self.db.rollback()
            return 1

if __name__=="__main__":
    try:
        ls=Leshui()
        ls.getindex()
        num=0
        while True:
            ls.getyzm()
            code=ls.readcode()
            result=ls.verifycode(code)
            if result==True:
                os.remove(ls.nowtime+".png")
                ls.login(code)
                res = ls.indexs()
                lists = ls.getsindex(res)
                ls.getpage(lists)
                break
            time.sleep(1)
            if num==100:
                break
            num+=1


    except Exception as e:
        logging.info(e)


    #ls.login(code)




#Location: https://uc.leshui365.com/?system=leshui-2.1&stylesheet=https://cdn2.leshui365.com/fdp_ls2/s_p/components/sso-login/dialog_e52033c.css&logintype=pc-with-thirdparty
#Location: https://www.leshui365.com/components/login/loginNotice?token=3e1bd2b0-1d2f-11e9-9536-516174bfc8e3
