# -*- coding: utf-8 -*-
import requests
import re
import time
import random
import pymysql
import json
from lxml import etree
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename="/home/wwwlogs/python/caizhengyaowen.txt")
logger = logging.getLogger(__name__)
class CaiZhengxinwen():

    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
    def __init__(self):
        self.nowtime = str(int(time.time()))
    def getindex(self):


        res = requests.get("http://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/",
                               headers=self.headers)

        res.encoding="gb2312"
        html=etree.HTML(res.text)
        urls=html.xpath('.//table[@id="id_bl"]/tr/td/a/@href')

        for url in urls:
            time.sleep(1)
            try:
                if "http" not in url:
                    url=url.replace("../../","http://www.mof.gov.cn/").replace("../","http://www.mof.gov.cn/zhengwuxinxi/").replace("./","http://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/")
                res=requests.get(url,headers=self.headers)
                res.encoding="gb2312"
                html=etree.HTML(res.text)
                title=html.xpath('.//td[@class="font_biao1"]/text()')[0].strip("\n\t\t\t")

                date=re.findall('\d+年\d+月\d+日',res.text)
                if date:
                    date=date[0].replace("年","-").replace("月","-").replace("日","")
                content=html.xpath('.//p[@align="justify"]/text()|.//p[@class="MsoNormal"]|.//p[@align="center"]/text()|.//p/text()')
                lists=[]
                for i in content:
                    if "来源：" in i:
                        continue
                    if "附件下载:" in i:
                        continue
                    if "Element" in str(i):
                        j=i.xpath('.//span/text()')
                        i="".join(j)
                    i=i.strip()
                    lists.append(i)
                content="</p><p>".join(lists)
                content="<p>"+content+"</p>"
                content=content.replace("&ldquo;","").replace("&rdquo;","").replace("&lsquo;","").replace("&rsquo;","").replace("&ensp;","").replace("&hellip;","").replace("&mdash;","").replace("\r\n","")
                uid = str(int(random.random() * 1000000000000))
                item={}
                item["library"] = pymysql.escape_string('[\"11\"]')
                item["url"] = url
                item["title"] = title
                item["content"] = content
                item["describes"] = title
                item["type"] = pymysql.escape_string('[\"39\"]')
                item["need_login"] = 0
                item["status"] = 2
                item["date"] = date
                item["uid"] = uid
                item["create_time"] = self.nowtime
                item["update_at"] = self.nowtime
                item["type_list"]=pymysql.escape_string('[\"3\",\"48\"]')
                item["type_name"]="新闻,财政新闻"
                item["source"]="中华人民共和国财政部"
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
    cz=CaiZhengxinwen()
    cz.getindex()


    #http://www.mof.gov.cn/xinwenlianbo/guangdongcaizhengxinxilianbo/201901/t20190102_3112490.htm
