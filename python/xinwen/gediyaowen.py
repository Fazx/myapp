import requests
from lxml import etree
import re
import time
import json
import random
import pymysql
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename="/home/wwwlogs/python/gediyaowen.txt")
logger = logging.getLogger(__name__)
class YaoWen():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }

    def __init__(self):
        self.session=requests.session()
        self.nowtime=str(int(time.time()))
        self.proxy={"http": "http://37.59.35.174:1080", "https": "http://37.59.35.174:1080"}
    def getpage(self):
        res=self.session.get("http://www.chinatax.gov.cn/n810219/n810739/index.html",headers=self.headers)
        html=etree.HTML(res.text)
        urls=html.xpath('.//span[@id="comp_831221"]/dl/dd/a/@href')
        for url in urls:
            time.sleep(5)
            url = url.replace("../..", "http://www.chinatax.gov.cn")
            res = self.session.get(url, headers=self.headers)
            res.encoding = "utf-8"
            htmls=res.text
            try:

                item=self.detail(htmls,url)
                Db=Dbmysql()
                res=Db.dbs(item)
                if res==0:
                    db=dbmysql()
                    db.dbs(item)
            except Exception as e:
                logging.info(e)

    def detail(self,htmls,url):
        item={}
        html = etree.HTML(htmls)
        url=url

        title=html.xpath('.//li[@class="sv_texth1"]/text()')[0]

        content=re.search('<li class="sv_texth3" id="tax_content">(.*?)</li>',htmls,re.S).group(1)
        date=re.search('<div class="zuo1">(.*?)&',htmls,re.S).group(1).replace("年","-").replace("月","-").replace("日","")
        uid=str(int(random.random()*1000000000000))
        '''
           describe:描述
       library：栏目类别【新闻库、法规库、专题库、】
       type:栏目类型【法规库-按税种】
       column_list_id：类型名【法规库-按税种-个税库】
       is_recommend：是否推荐【默认1】
       is_top：是否置顶【默认1】
       is_notice：是否公告【默认1】
       need_login：是否登陆阅读
       is_special：是否专题【默认1】
       uid：文章id
        '''
        item["library"]=pymysql.escape_string('[\"11\"]')
        item["url"]=url
        item["title"]=title
        item["content"]=content.replace('"',"'").replace("../../..","http://www.chinatax.gov.cn").replace("&ldquo;","").replace("&rdquo;","").replace("&lsquo;","").replace("&rsquo;","").replace("&ensp;","").replace("&hellip;","").replace("&mdash;","").replace("\r\n","")
        item["describes"]=title
        item["type"]=pymysql.escape_string('[\"36\"]')
        #item["column_list_id"]=pymysql.escape_string('[\"2\"]')
        item["status"]=2
        item["need_login"]=0
        item["date"]=date
        item["uid"]=uid
        item["create_time"]=self.nowtime
        item["update_at"]=self.nowtime
        item["type_list"] = pymysql.escape_string('[\"3\",\"45\"]')
        item["type_name"] = "新闻,各地新闻"
        item["source"]="国家税务总局"
        return item
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

    yw=YaoWen()
    yw.getpage()


#grant all PRIVILEGES on hssj.* to root@'10.19.20.209'  identified by 'jKN09L_';
