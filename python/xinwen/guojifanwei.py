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
    cuntrylist= {'多边税收条约': pymysql.escape_string('[\"2\",\"7\",\"308\",\"309\"]'),
              '日本': pymysql.escape_string('[\"2\",\"7\",\"308\",\"310\"]'),
              '美国': pymysql.escape_string('[\"2\",\"7\",\"308\",\"311\"]'),
              '法国': pymysql.escape_string('[\"2\",\"7\",\"308\",\"312\"]'),
              '英国': pymysql.escape_string('[\"2\",\"7\",\"308\",\"313\"]'),
              '比利时':pymysql.escape_string('[\"2\",\"7\",\"308\",\"314\"]'),
              '德国': pymysql.escape_string('[\"2\",\"7\",\"308\",\"315\"]'),
              '马来西亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"316\"]'),
              '挪威': pymysql.escape_string('[\"2\",\"7\",\"308\",\"317\"]'),
              '丹麦': pymysql.escape_string('[\"2\",\"7\",\"308\",\"318"])'),
              '新加坡': pymysql.escape_string('[\"2\",\"7\",\"308\",\"319\"]'),
              '加拿大': pymysql.escape_string('[\"2\",\"7\",\"308\",\"320\"]'),
              '芬兰': pymysql.escape_string('[\"2\",\"7\",\"308\",\"321\"]'),
              '瑞典':pymysql.escape_string('[\"2\",\"7\",\"308\",\"322\"]'),
              '新西兰':pymysql.escape_string('[\"2\",\"7\",\"308\",\"323\"]'),
              '泰国': pymysql.escape_string('[\"2\",\"7\",\"308\",\"324\"]'),
              '意大利':pymysql.escape_string('[\"2\",\"7\",\"308\",\"325\"]'),
              '荷兰': pymysql.escape_string('[\"2\",\"7\",\"308\",\"326\"]'),
              '捷克斯洛伐克（适用于斯洛伐克）':pymysql.escape_string('[\"2\",\"7\",\"308\",\"327\"]'),
              '波兰': pymysql.escape_string('[\"2\",\"7\",\"308\",\"328\"]'),
              '澳大利亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"329\"]'),
              '南斯拉夫（适用于波斯尼亚和黑塞哥维那）':pymysql.escape_string('[\"2\",\"7\",\"308\",\"330\"]'),
              '保加利亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"331\"]'),
              '巴基斯坦':pymysql.escape_string('[\"2\",\"7\",\"308\",\"332\"]'),
              '科威特':pymysql.escape_string('[\"2\",\"7\",\"308\",\"333\"]'),
              '瑞士': pymysql.escape_string('[\"2\",\"7\",\"308\",\"334\"]'),
              '塞浦路斯':pymysql.escape_string('[\"2\",\"7\",\"308\",\"335\"]'),
              '西班牙': pymysql.escape_string('[\"2\",\"7\",\"308\",\"336\"]'),
              '罗马尼亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"337\"]'),
              '奥地利': pymysql.escape_string('[\"2\",\"7\",\"308\",\"338\"]'),
              '巴西': pymysql.escape_string('[\"2\",\"7\",\"308\",\"339\"]'),
              '蒙古': pymysql.escape_string('[\"2\",\"7\",\"308\",\"340\"]'),
              '匈牙利':pymysql.escape_string('[\"2\",\"7\",\"308\",\"341\"]'),
              '马耳他': pymysql.escape_string('[\"2\",\"7\",\"308\",\"342\"]'),
              '阿联酋':pymysql.escape_string('[\"2\",\"7\",\"308\",\"343\"]'),
              '卢森堡':pymysql.escape_string('[\"2\",\"7\",\"308\",\"344\"]'),
              '韩国': pymysql.escape_string('[\"2\",\"7\",\"308\",\"345\"]'),
              '俄罗斯': pymysql.escape_string('[\"2\",\"7\",\"308\",\"346\"]'),
              '巴新': pymysql.escape_string('[\"2\",\"7\",\"308\",\"347\"]'),
              '印度':pymysql.escape_string('[\"2\",\"7\",\"308\",\"348\"]'),
              '毛里求斯': pymysql.escape_string('[\"2\",\"7\",\"308\",\"349\"]'),
              '克罗地亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"350\"]'),
              '白俄罗斯': pymysql.escape_string('[\"2\",\"7\",\"308\",\"351\"]'),
              '斯洛文尼亚':pymysql.escape_string('[\"2\",\"7\",\"308\",\"352\"]'),
              '以色列': pymysql.escape_string('[\"2\",\"7\",\"308\",\"353\"]'),
              '越南': pymysql.escape_string('[\"2\",\"7\",\"308\",\"354\"]'),
              '土耳其':pymysql.escape_string('[\"2\",\"7\",\"308\",\"355\"]'),
              '乌克兰': pymysql.escape_string('[\"2\",\"7\",\"308\",\"356\"]'),
              '亚美尼亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"357\"]'),
              '牙买加': pymysql.escape_string('[\"2\",\"7\",\"308\",\"358\"]'),
              '冰岛': pymysql.escape_string('[\"2\",\"7\",\"308\",\"359\"]'),
              '立陶宛': pymysql.escape_string('[\"2\",\"7\",\"308\",\"360\"]'),
              '拉脱维亚':pymysql.escape_string('[\"2\",\"7\",\"308\",\"361\"]'),
              '乌兹别克斯坦': pymysql.escape_string('[\"2\",\"7\",\"308\",\"362\"]'),
              '孟加拉国': pymysql.escape_string('[\"2\",\"7\",\"308\",\"363\"]'),
              '南斯拉夫联盟（适用于塞尔维亚和黑山）': pymysql.escape_string('[\"2\",\"7\",\"308\",\"364\"]'),
              '苏丹': pymysql.escape_string('[\"2\",\"7\",\"308\",\"365\"]'),
              '马其顿':pymysql.escape_string('[\"2\",\"7\",\"308\",\"366\"]'),
              '埃及': pymysql.escape_string('[\"2\",\"7\",\"308\",\"367\"]'),
              '葡萄牙': pymysql.escape_string('[\"2\",\"7\",\"308\",\"368\"]'),
              '爱沙尼亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"369\"]'),
              '老挝': pymysql.escape_string('[\"2\",\"7\",\"308\",\"370\"]'),
              '塞舌尔': pymysql.escape_string('[\"2\",\"7\",\"308\",\"371\"]'),
              '菲律宾THE': pymysql.escape_string('[\"2\",\"7\",\"308\",\"372\"]'),
              '爱尔兰': pymysql.escape_string('[\"2\",\"7\",\"308\",\"373\"]'),
              '南非':pymysql.escape_string('[\"2\",\"7\",\"308\",\"374\"]'),
              '巴巴多斯':pymysql.escape_string('[\"2\",\"7\",\"308\",\"375\"]'),
              '摩尔多瓦':pymysql.escape_string('[\"2\",\"7\",\"308\",\"376\"]'),
              '卡塔尔国':pymysql.escape_string('[\"2\",\"7\",\"308\",\"377\"]'),
              '古巴': pymysql.escape_string('[\"2\",\"7\",\"308\",\"378\"]'),
              '委内瑞拉': pymysql.escape_string('[\"2\",\"7\",\"308\",\"379\"]'),
              '尼泊尔': pymysql.escape_string('[\"2\",\"7\",\"308\",\"380\"]'),
              '哈萨克斯坦': pymysql.escape_string('[\"2\",\"7\",\"308\",\"381\"]'),
              '印度尼西亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"382\"]'),
              '阿曼': pymysql.escape_string('[\"2\",\"7\",\"308\",\"383\"]'),
              '尼日利亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"384\"]'),
              '突尼斯': pymysql.escape_string('[\"2\",\"7\",\"308\",\"385\"]'),
              '伊朗': pymysql.escape_string('[\"2\",\"7\",\"308\",\"386\"]'),
              '巴林': pymysql.escape_string('[\"2\",\"7\",\"308\",\"387\"]'),
              '希腊': pymysql.escape_string('[\"2\",\"7\",\"308\",\"388\"]'),
              '吉尔吉斯': pymysql.escape_string('[\"2\",\"7\",\"308\",\"389\"]'),
              '摩洛哥': pymysql.escape_string('[\"2\",\"7\",\"308\",\"390\"]'),
              '斯里兰卡': pymysql.escape_string('[\"2\",\"7\",\"308\",\"391\"]'),
              '特立尼达和多巴哥': pymysql.escape_string('[\"2\",\"7\",\"308\",\"392\"]'),
              '阿尔巴尼亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"393\"]'),
              '文莱': pymysql.escape_string('[\"2\",\"7\",\"308\",\"394\"]'),
              '阿塞拜疆': pymysql.escape_string('[\"2\",\"7\",\"308\",\"395\"]'),
              '格鲁吉亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"396\"]'),
              '墨西哥': pymysql.escape_string('[\"2\",\"7\",\"308\",\"397\"]'),
              '沙特阿拉伯': pymysql.escape_string('[\"2\",\"7\",\"308\",\"398\"]'),
              '阿尔及利亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"399\"]'),
              '塔吉克斯坦': pymysql.escape_string('[\"2\",\"7\",\"308\",\"400\"]'),
              '埃塞俄比亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"401\"]'),
              '土库曼斯坦': pymysql.escape_string('[\"2\",\"7\",\"308\",\"402\"]'),
              '捷克': pymysql.escape_string('[\"2\",\"7\",\"308\",\"403\"]'),
              '赞比亚':pymysql.escape_string('[\"2\",\"7\",\"308\",\"404\"]'),
              '叙利亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"405\"]'),
              '乌干达': pymysql.escape_string('[\"2\",\"7\",\"308\",\"406\"]'),
              '博茨瓦纳': pymysql.escape_string('[\"2\",\"7\",\"308\",\"407\"]'),
              '厄瓜多尔': pymysql.escape_string('[\"2\",\"7\",\"308\",\"408\"]'),
              '智利': pymysql.escape_string('[\"2\",\"7\",\"308\",\"409\"]'),
              '津巴布韦':pymysql.escape_string('[\"2\",\"7\",\"308\",\"410\"]'),
              '柬埔寨': pymysql.escape_string('[\"2\",\"7\",\"308\",\"411\"]'),
              '肯尼亚': pymysql.escape_string('[\"2\",\"7\",\"308\",\"412\"]'),
              '加蓬':pymysql.escape_string('[\"2\",\"7\",\"308\",\"413\"]'),
              '刚果（布）': pymysql.escape_string('[\"2\",\"7\",\"308\",\"414\"]'),
              '安哥拉': pymysql.escape_string('[\"2\",\"7\",\"308\",\"415\"]'),
              '阿根廷': pymysql.escape_string('[\"2\",\"7\",\"308\",\"416\"]'),
              '香港特别行政区': pymysql.escape_string('[\"2\",\"7\",\"308\",\"417\"]'),
              '澳门特别行政区':pymysql.escape_string('[\"2\",\"7\",\"308\",\"418\"]'),
              '台湾': pymysql.escape_string('[\"2\",\"7\",\"308\",\"419\"]')}   #cuntrylist={'多边税收条约': pymysql.escape_string('[\"49\"]'), '香港特别行政区': pymysql.escape_string('[\"50\"]'), '澳门特别行政区': pymysql.escape_string('[\"51\"]'), '台湾': pymysql.escape_string('[\"52\"]'), '日本': pymysql.escape_string('[\"53\"]'), '美国': pymysql.escape_string('[\"54\"]'), '法国': pymysql.escape_string('[\"55\"]'), '英国': pymysql.escape_string('[\"56\"]'), '比利时': pymysql.escape_string('[\"57\"]'), '德国': pymysql.escape_string('[\"58\"]'), '马来西亚': pymysql.escape_string('[\"59\"]'), '挪威': pymysql.escape_string('[\"60\"]'), '丹麦': pymysql.escape_string('[\"61\"]'), '新加坡': pymysql.escape_string('[\"62\"]'), '加拿大': pymysql.escape_string('[\"63\"]'), '芬兰': pymysql.escape_string('[\"64\"]'), '瑞典': pymysql.escape_string('[\"65\"]'), '新西兰': pymysql.escape_string('[\"66\"]'), '泰国': pymysql.escape_string('[\"67\"]'), '意大利': pymysql.escape_string('[\"68\"]'), '荷兰': pymysql.escape_string('[\"69\"]'), '捷克斯洛伐克': pymysql.escape_string('[\"70\"]'), '波兰': pymysql.escape_string('[\"71\"]'), '澳大利亚': pymysql.escape_string('[\"72\"]'), '南斯拉夫': pymysql.escape_string('[\"73\"]'), '保加利亚': pymysql.escape_string('[\"74\"]'), '巴基斯坦': pymysql.escape_string('[\"75\"]'), '科威特': pymysql.escape_string('[\"76\"]'), '瑞士': pymysql.escape_string('[\"77\"]'), '塞浦路斯': pymysql.escape_string('[\"78\"]'), '西班牙': pymysql.escape_string('[\"79\"]'), '罗马尼亚': pymysql.escape_string('[\"80\"]'), '奥地利': pymysql.escape_string('[\"81\"]'), '巴西': pymysql.escape_string('[\"82\"]'), '蒙古': pymysql.escape_string('[\"83\"]'), '匈牙利': pymysql.escape_string('[\"84\"]'), '马耳他': pymysql.escape_string('[\"85\"]'), '阿联酋': pymysql.escape_string('[\"86\"]'), '卢森堡': pymysql.escape_string('[\"87\"]'), '韩国': pymysql.escape_string('[\"88\"]'), '俄罗斯': pymysql.escape_string('[\"89\"]'), '巴新': pymysql.escape_string('[\"90\"]'), '印度': pymysql.escape_string('[\"91\"]'), '毛里求斯': pymysql.escape_string('[\"92\"]'), '克罗地亚': pymysql.escape_string('[\"93\"]'), '白俄罗斯': pymysql.escape_string('[\"94\"]'), '斯洛文尼亚': pymysql.escape_string('[\"95\"]'), '以色列': pymysql.escape_string('[\"96\"]'), '越南': pymysql.escape_string('[\"97\"]'), '土耳其': pymysql.escape_string('[\"98\"]'), '乌克兰': pymysql.escape_string('[\"99\"]'), '亚美尼亚': pymysql.escape_string('[\"100\"]'), '牙买加': pymysql.escape_string('[\"101\"]'), '冰岛': pymysql.escape_string('[\"102\"]'), '立陶宛': pymysql.escape_string('[\"103\"]'), '拉脱维亚': pymysql.escape_string('[\"104\"]'), '乌兹别克斯坦': pymysql.escape_string('[\"105\"]'), '孟加拉国': pymysql.escape_string('[\"106\"]'), '南斯拉夫联盟': pymysql.escape_string('[\"107\"]'), '苏丹': pymysql.escape_string('[\"108\"]'), '马其顿': pymysql.escape_string('[\"109\"]'), '埃及': pymysql.escape_string('[\"111\"]'), '葡萄牙': pymysql.escape_string('[\"112\"]'), '爱沙尼亚': pymysql.escape_string('[\"113\"]'), '老挝': pymysql.escape_string('[\"114\"]'), '塞舌尔': pymysql.escape_string('[\"115\"]'), '菲律宾THE': pymysql.escape_string('[\"116\"]'), '爱尔兰': pymysql.escape_string('[\"117\"]'), '南非': pymysql.escape_string('[\"118\"]'), '巴巴多斯': pymysql.escape_string('[\"119\"]'), '摩尔多瓦': pymysql.escape_string('[\"120\"]'), '卡塔尔国': pymysql.escape_string('[\"121\"]'), '古巴': pymysql.escape_string('[\"122\"]'), '委内瑞拉': pymysql.escape_string('[\"123\"]'), '尼泊尔': pymysql.escape_string('[\"124\"]'), '哈萨克斯坦': pymysql.escape_string('[\"125\"]'), '印度尼西亚': pymysql.escape_string('[\"126\"]'), '阿曼': pymysql.escape_string('[\"127\"]'), '尼日利亚': pymysql.escape_string('[\"128\"]'), '突尼斯': pymysql.escape_string('[\"129\"]'), '伊朗': pymysql.escape_string('[\"130\"]'), '巴林': pymysql.escape_string('[\"131\"]'), '希腊': pymysql.escape_string('[\"132\"]'), '吉尔吉斯': pymysql.escape_string('[\"133\"]'), '摩洛哥': pymysql.escape_string('[\"134\"]'), '斯里兰卡': pymysql.escape_string('[\"135\"]'), '特立尼达和多巴哥': pymysql.escape_string('[\"136\"]'), '阿尔巴尼亚': pymysql.escape_string('[\"137\"]'), '文莱': pymysql.escape_string('[\"138\"]'), '阿塞拜疆': pymysql.escape_string('[\"139\"]'), '格鲁吉亚': pymysql.escape_string('[\"140\"]'), '墨西哥': pymysql.escape_string('[\"141\"]'), '沙特阿拉伯': pymysql.escape_string('[\"142\"]'), '阿尔及利亚': pymysql.escape_string('[\"143\"]'), '塔吉克斯坦': pymysql.escape_string('[\"144\"]'), '埃塞俄比亚': pymysql.escape_string('[\"145\"]'), '土库曼斯坦': pymysql.escape_string('[\"146\"]'), '捷克': pymysql.escape_string('[\"147\"]'), '赞比亚': pymysql.escape_string('[\"148\"]'), '叙利亚': pymysql.escape_string('[\"149\"]'), '乌干达': pymysql.escape_string('[\"150\"]'), '博茨瓦纳': pymysql.escape_string('[\"151\"]'), '厄瓜多尔': pymysql.escape_string('[\"152\"]'), '智利': pymysql.escape_string('[\"153\"]'), '津巴布韦': pymysql.escape_string('[\"154\"]'), '柬埔寨': pymysql.escape_string('[\"155\"]'), '肯尼亚': pymysql.escape_string('[\"156\"]'), '加蓬': pymysql.escape_string('[\"157\"]'), '刚果（布）': pymysql.escape_string('[\"158\"]'), '安哥拉': pymysql.escape_string('[\"159\"]'), '阿根廷': pymysql.escape_string('[\"160\"')}
    def __init__(self):
        self.session=requests.session()
    def geturls(self):
        res=self.session.get("http://www.chinatax.gov.cn/n810341/n810770/index.html",headers=self.headers)
        res.encoding="utf-8"
        time.sleep(6)
        #<p class="ntop4" align="center"><a target="_blank" href="/n810341/n810770/c1794734/content.html">台湾<br />
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
                    item["type_name"]='法规库,全部法规,国际范围,'+cuntry
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
            date=re.search('<div class="zuo1">(.*?)日',res.text).group(1)
            date=date.replace("年","-").replace("月","-")
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
            item["source"]="国家税务总局"
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
            print("插入成功")
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
    #            # print("插入成功")
    #         except Exception as e:
    #             print(e)
    #             self.db.rollback()
    #         self.db.close()
    #
    # db=dbmysql()
    # db.dbs()
