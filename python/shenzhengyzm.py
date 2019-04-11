import requests
import sys
import json
import io
from urllib import parse
class ShenZhenYzm():

    session=requests.session()
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    cardtypes={
        "身份证":"201",
        "军官证":"202",
        "武警警官证":"203",
        "士兵证":"204",
        "外国护照":"208",
        "港澳居民来往内地通行证":"210",
        "台湾居民来往大陆通行证":"213",
        "香港身份证":"219",
        "台湾身份证":"220",
        "澳门身份证":"221",
        "中国护照":"227",
        "外国人永久居留证":"233"
    }
    def getyzm(self,cardtype,username):

        res=self.session.get("https://dzswj.szds.gov.cn/dzswj/zrrUserLogin.do?method=initYthLogin",headers=self.headers,verify=False)
        data={
            'zjlx':self.cardtypes[cardtype],
            'gjDm':'156',
            'zjhm':username
        }
        res=self.session.post('https://dzswj.szds.gov.cn/dzswj/zrrUserLogin.json?method=getZrrDtm',data=data,verify=False,headers=self.headers).json()
        resp=json.dumps(res)
        print(resp)

if __name__=="__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # cardtype="身份证"
    # username="23102419721012400215"

    cardtype = sys.argv[1]
    username = sys.argv[2]
    cardtype = parse.unquote(cardtype)
    szy=ShenZhenYzm()
    szy.getyzm(cardtype,username)
