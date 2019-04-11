import requests
import re
import os
import time
import random
import pymysql
from lxml import etree
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename="/home/wwwlogs/python/shebaoxinwen.txt")
logger = logging.getLogger(__name__)
class SheBaoxinwen():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
    def __init__(self):
        self.nowtime = str(int(time.time()))
    def getindex(self):

        res = requests.get("http://www.mohrss.gov.cn/SYrlzyhshbzb/dongtaixinwen/buneiyaowen/",
                               headers=self.headers)

        html=etree.HTML(res.text)
        urls=html.xpath('.//div[@class="serviceMainListConType"]//div[@class="serviceMainListTxt"]/span/a/@href')


        for url in urls:
            try:
                if "http" not in url:
                    url=url.replace("./","http://www.mohrss.gov.cn/SYrlzyhshbzb/dongtaixinwen/buneiyaowen/")
                res=requests.get(url,headers=self.headers)
                res.encoding="utf-8"
                html=etree.HTML(res.text)
                title=html.xpath('.//div[@class="insMainConTitle_b"]/text()')[0]
                date=re.findall('发布日期：(.*?)&nbsp;',res.text)
                time.sleep(2)
                content=re.findall('<div class=TRS_Editor>(.*?)<script language="javascript">',res.text,re.S)[0].replace("\n","").replace("\u3000\u3000","")
                bname=os.path.dirname(url)
                if "img src" in content:

                    content=content.replace('src="./','src="'+bname+'/')

                uid = str(int(random.random() * 1000000000000))
                item={}
                item["library"] = pymysql.escape_string('[\"11\"]')
                item["url"] = url
                item["title"] = title
                item["content"] = content.replace('"',"'").replace("&ldquo;","").replace("&rdquo;","").replace("&lsquo;","").replace("&rsquo;","").replace("&ensp;","").replace("&hellip;","").replace("&mdash;","").replace("\r\n","")
                item["describes"] = title
                item["type"] = pymysql.escape_string('[\"37\"]')
                item["status"] = 2
                item["need_login"] = 0
                item["date"] = date[0]
                item["uid"] = uid
                item["create_time"] = self.nowtime
                item["update_at"] = self.nowtime
                item["type_list"] = pymysql.escape_string('[\"3\",\"46\"]')
                item["type_name"] = "新闻,社保新闻"
                item["source"]="中华人名共和国人力资源和社会保障部"
                logging.info(url)
                try:
                    Db=Dbmysql()
                    res=Db.dbs(item)
                    if res==0:
                        db=dbmysql()
                        db.dbs(item)
                except Exception as e:
                    logging.info(e)
            except Exception as e:
                logging.info(e)

class dbmysql():

    def __init__(self):
        self.db=pymysql.connect(host ="localhost",user="root",passwd="jKN09L_",db="hssj",charset = "utf8")
        self.cursor=self.db.cursor()
    def dbs(self,item):

        sql='insert into news(url,title,content,describes,type,status,need_login,date,uid,library,create_time,type_list,type_name,source) values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}")'.format(item["url"],item["title"],item["content"],item["describes"],item["type"],item["status"],item["need_login"],item["date"],item["uid"],item["library"],item["create_time"],item["type_list"],item["type_name"],item["source"])
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

        sql='insert into news_python_log(url,title,content,describes,type,status,need_login,date,uid,library,create_time,type_list,type_name,source) values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}")'.format(item["url"],item["title"],item["content"],item["describes"],item["type"],item["status"],item["need_login"],item["date"],item["uid"],item["library"],item["create_time"],item["type_list"],item["type_name"],item["source"])
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 0
        except Exception as e:
            logging.info(e)
            self.db.rollback()
            return 1

if __name__=="__main__":

    cz=SheBaoxinwen()
    cz.getindex()



    #http://www.mof.gov.cn/xinwenlianbo/guangdongcaizhengxinxilianbo/201901/t20190102_3112490.htm
