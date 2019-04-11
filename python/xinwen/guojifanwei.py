# coding=gbk
import requests
import json
import re
import random
import time
import pytesseract
import pymysql
from lxml import etree
from PIL import Image,ImageOps
from selenium import webdriver
from pyvirtualdisplay import Display
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename="/home/wwwlogs/python/guojifanweilog.txt")
logger = logging.getLogger(__name__)
class GuoJi():

    proxy={"http": "http://37.59.35.174:1080", "https": "http://37.59.35.174:1080"}
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400"
    }
    nowtime = str(int(time.time()))
    cuntrylist= {'���˰����Լ': pymysql.escape_string('[\"2\",\"7\",\"308\",\"309\"]'),
              '�ձ�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"310\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"311\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"312\"]'),
              'Ӣ��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"313\"]'),
              '����ʱ':pymysql.escape_string('[\"2\",\"7\",\"308\",\"314\"]'),
              '�¹�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"315\"]'),
              '��������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"316\"]'),
              'Ų��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"317\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"318"])'),
              '�¼���': pymysql.escape_string('[\"2\",\"7\",\"308\",\"319\"]'),
              '���ô�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"320\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"321\"]'),
              '���':pymysql.escape_string('[\"2\",\"7\",\"308\",\"322\"]'),
              '������':pymysql.escape_string('[\"2\",\"7\",\"308\",\"323\"]'),
              '̩��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"324\"]'),
              '�����':pymysql.escape_string('[\"2\",\"7\",\"308\",\"325\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"326\"]'),
              '�ݿ�˹�工�ˣ�������˹�工�ˣ�':pymysql.escape_string('[\"2\",\"7\",\"308\",\"327\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"328\"]'),
              '�Ĵ�����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"329\"]'),
              '��˹���������ڲ�˹���Ǻͺ�����ά�ǣ�':pymysql.escape_string('[\"2\",\"7\",\"308\",\"330\"]'),
              '��������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"331\"]'),
              '�ͻ�˹̹':pymysql.escape_string('[\"2\",\"7\",\"308\",\"332\"]'),
              '������':pymysql.escape_string('[\"2\",\"7\",\"308\",\"333\"]'),
              '��ʿ': pymysql.escape_string('[\"2\",\"7\",\"308\",\"334\"]'),
              '����·˹':pymysql.escape_string('[\"2\",\"7\",\"308\",\"335\"]'),
              '������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"336\"]'),
              '��������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"337\"]'),
              '�µ���': pymysql.escape_string('[\"2\",\"7\",\"308\",\"338\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"339\"]'),
              '�ɹ�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"340\"]'),
              '������':pymysql.escape_string('[\"2\",\"7\",\"308\",\"341\"]'),
              '�����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"342\"]'),
              '������':pymysql.escape_string('[\"2\",\"7\",\"308\",\"343\"]'),
              '¬ɭ��':pymysql.escape_string('[\"2\",\"7\",\"308\",\"344\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"345\"]'),
              '����˹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"346\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"347\"]'),
              'ӡ��':pymysql.escape_string('[\"2\",\"7\",\"308\",\"348\"]'),
              'ë����˹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"349\"]'),
              '���޵���': pymysql.escape_string('[\"2\",\"7\",\"308\",\"350\"]'),
              '�׶���˹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"351\"]'),
              '˹��������':pymysql.escape_string('[\"2\",\"7\",\"308\",\"352\"]'),
              '��ɫ��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"353\"]'),
              'Խ��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"354\"]'),
              '������':pymysql.escape_string('[\"2\",\"7\",\"308\",\"355\"]'),
              '�ڿ���': pymysql.escape_string('[\"2\",\"7\",\"308\",\"356\"]'),
              '��������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"357\"]'),
              '�����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"358\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"359\"]'),
              '������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"360\"]'),
              '����ά��':pymysql.escape_string('[\"2\",\"7\",\"308\",\"361\"]'),
              '���ȱ��˹̹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"362\"]'),
              '�ϼ�����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"363\"]'),
              '��˹�������ˣ�����������ά�Ǻͺ�ɽ��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"364\"]'),
              '�յ�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"365\"]'),
              '�����':pymysql.escape_string('[\"2\",\"7\",\"308\",\"366\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"367\"]'),
              '������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"368\"]'),
              '��ɳ����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"369\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"370\"]'),
              '�����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"371\"]'),
              '���ɱ�THE': pymysql.escape_string('[\"2\",\"7\",\"308\",\"372\"]'),
              '������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"373\"]'),
              '�Ϸ�':pymysql.escape_string('[\"2\",\"7\",\"308\",\"374\"]'),
              '�ͰͶ�˹':pymysql.escape_string('[\"2\",\"7\",\"308\",\"375\"]'),
              'Ħ������':pymysql.escape_string('[\"2\",\"7\",\"308\",\"376\"]'),
              '��������':pymysql.escape_string('[\"2\",\"7\",\"308\",\"377\"]'),
              '�Ű�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"378\"]'),
              'ί������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"379\"]'),
              '�Ჴ��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"380\"]'),
              '������˹̹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"381\"]'),
              'ӡ��������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"382\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"383\"]'),
              '��������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"384\"]'),
              'ͻ��˹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"385\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"386\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"387\"]'),
              'ϣ��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"388\"]'),
              '������˹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"389\"]'),
              'Ħ���': pymysql.escape_string('[\"2\",\"7\",\"308\",\"390\"]'),
              '˹������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"391\"]'),
              '�������Ͷ�͸�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"392\"]'),
              '����������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"393\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"394\"]'),
              '�����ݽ�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"395\"]'),
              '��³����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"396\"]'),
              'ī����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"397\"]'),
              'ɳ�ذ�����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"398\"]'),
              '����������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"399\"]'),
              '������˹̹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"400\"]'),
              '���������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"401\"]'),
              '������˹̹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"402\"]'),
              '�ݿ�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"403\"]'),
              '�ޱ���':pymysql.escape_string('[\"2\",\"7\",\"308\",\"404\"]'),
              '������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"405\"]'),
              '�ڸɴ�': pymysql.escape_string('[\"2\",\"7\",\"308\",\"406\"]'),
              '��������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"407\"]'),
              '��϶��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"408\"]'),
              '����': pymysql.escape_string('[\"2\",\"7\",\"308\",\"409\"]'),
              '��Ͳ�Τ':pymysql.escape_string('[\"2\",\"7\",\"308\",\"410\"]'),
              '����կ': pymysql.escape_string('[\"2\",\"7\",\"308\",\"411\"]'),
              '������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"412\"]'),
              '����':pymysql.escape_string('[\"2\",\"7\",\"308\",\"413\"]'),
              '�չ�������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"414\"]'),
              '������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"415\"]'),
              '����͢': pymysql.escape_string('[\"2\",\"7\",\"308\",\"416\"]'),
              '����ر�������': pymysql.escape_string('[\"2\",\"7\",\"308\",\"417\"]'),
              '�����ر�������':pymysql.escape_string('[\"2\",\"7\",\"308\",\"418\"]'),
              '̨��': pymysql.escape_string('[\"2\",\"7\",\"308\",\"419\"]')}   #cuntrylist={'���˰����Լ': pymysql.escape_string('[\"49\"]'), '����ر�������': pymysql.escape_string('[\"50\"]'), '�����ر�������': pymysql.escape_string('[\"51\"]'), '̨��': pymysql.escape_string('[\"52\"]'), '�ձ�': pymysql.escape_string('[\"53\"]'), '����': pymysql.escape_string('[\"54\"]'), '����': pymysql.escape_string('[\"55\"]'), 'Ӣ��': pymysql.escape_string('[\"56\"]'), '����ʱ': pymysql.escape_string('[\"57\"]'), '�¹�': pymysql.escape_string('[\"58\"]'), '��������': pymysql.escape_string('[\"59\"]'), 'Ų��': pymysql.escape_string('[\"60\"]'), '����': pymysql.escape_string('[\"61\"]'), '�¼���': pymysql.escape_string('[\"62\"]'), '���ô�': pymysql.escape_string('[\"63\"]'), '����': pymysql.escape_string('[\"64\"]'), '���': pymysql.escape_string('[\"65\"]'), '������': pymysql.escape_string('[\"66\"]'), '̩��': pymysql.escape_string('[\"67\"]'), '�����': pymysql.escape_string('[\"68\"]'), '����': pymysql.escape_string('[\"69\"]'), '�ݿ�˹�工��': pymysql.escape_string('[\"70\"]'), '����': pymysql.escape_string('[\"71\"]'), '�Ĵ�����': pymysql.escape_string('[\"72\"]'), '��˹����': pymysql.escape_string('[\"73\"]'), '��������': pymysql.escape_string('[\"74\"]'), '�ͻ�˹̹': pymysql.escape_string('[\"75\"]'), '������': pymysql.escape_string('[\"76\"]'), '��ʿ': pymysql.escape_string('[\"77\"]'), '����·˹': pymysql.escape_string('[\"78\"]'), '������': pymysql.escape_string('[\"79\"]'), '��������': pymysql.escape_string('[\"80\"]'), '�µ���': pymysql.escape_string('[\"81\"]'), '����': pymysql.escape_string('[\"82\"]'), '�ɹ�': pymysql.escape_string('[\"83\"]'), '������': pymysql.escape_string('[\"84\"]'), '�����': pymysql.escape_string('[\"85\"]'), '������': pymysql.escape_string('[\"86\"]'), '¬ɭ��': pymysql.escape_string('[\"87\"]'), '����': pymysql.escape_string('[\"88\"]'), '����˹': pymysql.escape_string('[\"89\"]'), '����': pymysql.escape_string('[\"90\"]'), 'ӡ��': pymysql.escape_string('[\"91\"]'), 'ë����˹': pymysql.escape_string('[\"92\"]'), '���޵���': pymysql.escape_string('[\"93\"]'), '�׶���˹': pymysql.escape_string('[\"94\"]'), '˹��������': pymysql.escape_string('[\"95\"]'), '��ɫ��': pymysql.escape_string('[\"96\"]'), 'Խ��': pymysql.escape_string('[\"97\"]'), '������': pymysql.escape_string('[\"98\"]'), '�ڿ���': pymysql.escape_string('[\"99\"]'), '��������': pymysql.escape_string('[\"100\"]'), '�����': pymysql.escape_string('[\"101\"]'), '����': pymysql.escape_string('[\"102\"]'), '������': pymysql.escape_string('[\"103\"]'), '����ά��': pymysql.escape_string('[\"104\"]'), '���ȱ��˹̹': pymysql.escape_string('[\"105\"]'), '�ϼ�����': pymysql.escape_string('[\"106\"]'), '��˹��������': pymysql.escape_string('[\"107\"]'), '�յ�': pymysql.escape_string('[\"108\"]'), '�����': pymysql.escape_string('[\"109\"]'), '����': pymysql.escape_string('[\"111\"]'), '������': pymysql.escape_string('[\"112\"]'), '��ɳ����': pymysql.escape_string('[\"113\"]'), '����': pymysql.escape_string('[\"114\"]'), '�����': pymysql.escape_string('[\"115\"]'), '���ɱ�THE': pymysql.escape_string('[\"116\"]'), '������': pymysql.escape_string('[\"117\"]'), '�Ϸ�': pymysql.escape_string('[\"118\"]'), '�ͰͶ�˹': pymysql.escape_string('[\"119\"]'), 'Ħ������': pymysql.escape_string('[\"120\"]'), '��������': pymysql.escape_string('[\"121\"]'), '�Ű�': pymysql.escape_string('[\"122\"]'), 'ί������': pymysql.escape_string('[\"123\"]'), '�Ჴ��': pymysql.escape_string('[\"124\"]'), '������˹̹': pymysql.escape_string('[\"125\"]'), 'ӡ��������': pymysql.escape_string('[\"126\"]'), '����': pymysql.escape_string('[\"127\"]'), '��������': pymysql.escape_string('[\"128\"]'), 'ͻ��˹': pymysql.escape_string('[\"129\"]'), '����': pymysql.escape_string('[\"130\"]'), '����': pymysql.escape_string('[\"131\"]'), 'ϣ��': pymysql.escape_string('[\"132\"]'), '������˹': pymysql.escape_string('[\"133\"]'), 'Ħ���': pymysql.escape_string('[\"134\"]'), '˹������': pymysql.escape_string('[\"135\"]'), '�������Ͷ�͸�': pymysql.escape_string('[\"136\"]'), '����������': pymysql.escape_string('[\"137\"]'), '����': pymysql.escape_string('[\"138\"]'), '�����ݽ�': pymysql.escape_string('[\"139\"]'), '��³����': pymysql.escape_string('[\"140\"]'), 'ī����': pymysql.escape_string('[\"141\"]'), 'ɳ�ذ�����': pymysql.escape_string('[\"142\"]'), '����������': pymysql.escape_string('[\"143\"]'), '������˹̹': pymysql.escape_string('[\"144\"]'), '���������': pymysql.escape_string('[\"145\"]'), '������˹̹': pymysql.escape_string('[\"146\"]'), '�ݿ�': pymysql.escape_string('[\"147\"]'), '�ޱ���': pymysql.escape_string('[\"148\"]'), '������': pymysql.escape_string('[\"149\"]'), '�ڸɴ�': pymysql.escape_string('[\"150\"]'), '��������': pymysql.escape_string('[\"151\"]'), '��϶��': pymysql.escape_string('[\"152\"]'), '����': pymysql.escape_string('[\"153\"]'), '��Ͳ�Τ': pymysql.escape_string('[\"154\"]'), '����կ': pymysql.escape_string('[\"155\"]'), '������': pymysql.escape_string('[\"156\"]'), '����': pymysql.escape_string('[\"157\"]'), '�չ�������': pymysql.escape_string('[\"158\"]'), '������': pymysql.escape_string('[\"159\"]'), '����͢': pymysql.escape_string('[\"160\"')}
    def __init__(self):
        self.session=requests.session()
    def geturls(self):
        res=self.session.get("http://www.chinatax.gov.cn/n810341/n810770/index.html",headers=self.headers)
        res.encoding="utf-8"
        time.sleep(6)
        #<p class="ntop4" align="center"><a target="_blank" href="/n810341/n810770/c1794734/content.html">̨��<br />
        urls=re.findall('<a target="_blank" href="/n810341/n810770/.*?content.html".*?<',res.text)
        #print(res.text)
        return urls

    def getpage(self,urls):
        for url in urls:
            time.sleep(3)
            try:
                time.sleep(10)
                item_url=re.findall('href="(.*?)".*?>(.*?)<',url)[0]
                if item_url[1]:
                    cuntry=item_url[1]
                    item_url="http://www.chinatax.gov.cn"+item_url[0]

                    res=self.session.get(item_url,headers=self.headers)
                    res.encoding="utf-8"
                    item=self.getdetail(res)

                    item["type_list"] = self.cuntrylist[cuntry]
                    item["type_name"]='�����,ȫ������,���ʷ�Χ,'+cuntry
                    Db = Dbmysql()
                    res = Db.dbs(item)
                    if res == 0:
                        db = dbmysql()
                        db.dbs(item)
            except Exception as e:
                logging.info(e)

    def getdetail(self,res):

        #print(res.text)
        try:
            content=re.findall('<li class="sv_texth3" id="tax_content">(.*?)</li>',res.text,re.S)[0]
            #print(content)
            content=content.replace('../../../',"http://www.chinatax.gov.cn/").replace("\n","").replace("\r\n","")
            title=re.search('<li class="sv_texth1" >(.*?)</li>',res.text).group(1)
            date=re.search('<div class="zuo1">(.*?)��',res.text).group(1)
            date=date.replace("��","-").replace("��","-")
            uid = str(int(random.random() * 1000000000000))
            item = {}
            item["library"] = pymysql.escape_string('[\"5\"]')
            item["url"] = res.url
            item["title"] = title
            item["content"] = content.replace('"',"'").replace("&ldquo;","").replace("&rdquo;","").replace("&lsquo;","").replace("&rsquo;","").replace("&ensp;","").replace("&hellip;","").replace("&mdash;","").replace("\r\n","")
            item["describes"] = title
            item["type"] = pymysql.escape_string('[\"44\"]')
            item["column_list_id"] = pymysql.escape_string('[\"100\"]')
            item["need_login"] = 0
            item["date"] = date
            item["uid"] = uid
            item["create_time"] = self.nowtime
            item["update_at"] = self.nowtime
            item["source"]="����˰���ܾ�"
            return item
        except Exception as e:
            logging.info(e)

class dbmysql():

    def __init__(self):
        self.db=pymysql.connect(host ="localhost",user="root",passwd="jKN09L_",db="hssj",charset = "utf8")
        self.cursor=self.db.cursor()
    def dbs(self,item):

        sql='insert into news(url,title,type_list,type_name,content,describes,type,column_list_id,need_login,date,uid,library,create_time,source) values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}")'.format(item["url"],item["title"],item["type_list"],item["type_name"],item["content"],item["describes"],item["type"],item["column_list_id"],item["need_login"],item["date"],item["uid"],item["library"],item["create_time"],item["source"])
       # print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("����ɹ�")
        except Exception as e:
            print(e)
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
            return 0
        except Exception as e:
            print(e)
            self.db.rollback()
            return 1

if __name__=="__main__":

    gj=GuoJi()
    urls=gj.geturls()
    gj.getpage(urls)


    # class dbmysql():
    #
    #     def __init__(self):
    #         self.db = pymysql.connect(host="localhost", user="root", passwd="123456", db="test", charset="utf8")
    #         self.cursor = self.db.cursor()
    #
    #     def dbs(self):
    #         item={}
    #         sql='select * from column_four_list where column_list_id=100 and STATUS=1'
    #         try:
    #             self.cursor.execute(sql)
    #             row=self.cursor.fetchall()
    #             for i in row:
    #                 item[i[2]]=str(i[0])
    #             print(item)
    #             self.db.commit()
    #            # print("����ɹ�")
    #         except Exception as e:
    #             print(e)
    #             self.db.rollback()
    #         self.db.close()
    #
    # db=dbmysql()
    # db.dbs()
