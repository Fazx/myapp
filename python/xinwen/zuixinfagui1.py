import requests
from lxml import etree
import time
import pymysql
import random
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename="/home/wwwlogs/python/fagui.txt")
logger = logging.getLogger(__name__)
class FaGui():
    nowtime=str(int(time.time()))
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400"
    }
    #http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/index_1.htm
    def getpage(self):


        res = requests.get("http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/", headers=self.headers)

        res.encoding="gb2312"
        html=etree.HTML(res.text)

        urls=html.xpath('.//table[@id="id_bl"]/tr')
        for urll in urls:
            try:
                time.sleep(3)
                url=urll.xpath('.//a/@href')[0].replace("./","http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/")
                date=urll.xpath('.//td/text()')
                date="".join(date).replace("\n","").replace("\t","").replace("（","").replace("）","").strip()
                res=requests.get(url,headers=self.headers)
                res.encoding="gb2312"
                item=self.detail(res)
                item["date"] = date

                Db = Dbmysql()
                res = Db.dbs(item)
                if res == 0:
                    db = dbmysql()
                    db.dbs(item)
                else:
                    pass
            except Exception as e:
                logging.info(e)

    def detail(self,res):
        try:
            html = etree.HTML(res.text)
            content=html.xpath('.//p/text()|.//p/span/text()|.//p/font/text()|.//p/font/span/text()|.//p/font/font/span/text()')
            content="</p><p>".join(content).replace("附件下载:","").replace("\n","").replace("\t","").replace("\xa0","")
            content="<p>"+content+"</p>"
            content=content.replace("&ldquo;","").replace("&rdquo;","").replace("&lsquo;","").replace("&rsquo;","").replace("&ensp;","").replace("&hellip;","").replace("&mdash;","").replace("\r\n","")
            title=html.xpath('.//td[@class="font_biao1"]/text()')[0].replace("\n","").replace("\t","")
            uid = str(int(random.random() * 1000000000000))
            #print(repr(url),repr(title),repr(date))
            item={}
            item["library"] = pymysql.escape_string('[\"5\"]')
            item["url"] = res.url
            item["title"] = title
            item["content"] = content
            item["describes"] = title
            item["type"] =pymysql.escape_string('[\"43\"]')
            item["column_list_id"] = pymysql.escape_string('[\"103\"]')
            item["need_login"] = 0
            item["uid"] = uid
            item["create_time"] = self.nowtime
            item["update_at"] = self.nowtime
            item["type_list"] = pymysql.escape_string('[\"2\",\"6\",\"10\"]')
            item["type_name"] = "法规库,最新文件,最新法规"
            item["source"]="中华人民共和国财政部"
            return item
        except Exception as e:
            logging.info(e)
class dbmysql():

    def __init__(self):
        self.db=pymysql.connect(host ="localhost",user="root",passwd="jKN09L_",db="hssj",charset = "utf8")
        self.cursor=self.db.cursor()
    def dbs(self,item):

        sql='insert into news(url,title,content,describes,type,column_list_id,need_login,date,uid,library,create_time,type_list,type_name,source) values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}")'.format(item["url"],item["title"],item["content"],item["describes"],item["type"],item["column_list_id"],item["need_login"],item["date"],item["uid"],item["library"],item["create_time"],item["type_list"],item["type_name"],item["source"])
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
        sql='insert into news_python_log(url,title,content,describes,type,column_list_id,need_login,date,uid,library,create_time,type_list,type_name,source) values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}")'.format(item["url"],item["title"],item["content"],item["describes"],item["type"],item["column_list_id"],item["need_login"],item["date"],item["uid"],item["library"],item["create_time"],item["type_list"],item["type_name"],item["source"])
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 0
        except Exception as e:
            logging.info(e)
            self.db.rollback()
            return 1

if __name__=="__main__":
    fg=FaGui()
    fg.getpage()