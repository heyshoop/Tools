# -*-coding:utf8-*-
import datetime
import time
import requests
import json
from pymongo import MongoClient

#数据库设置
conn = MongoClient('127.0.0.1',27017)
db = conn.bilibili
biliuser = db.bili_user

#生成随机数
def datetime_to_timestamp_in_milliseconds(d):
    current_milli_time = lambda: int(round(time.time() * 1000))
    return current_milli_time()
#设置头部
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/873981/',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}
#要爬取的连接
urls = []

for i in range(1, 2):
    url = 'http://space.bilibili.com/ajax/member/GetInfo?mid=' + str(i)
    urls.append(url)
payload = {
        '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
        'mid': url.replace('http://space.bilibili.com/ajax/member/GetInfo?mid=', '')
    }

print(payload)
jscontent = requests.post('http://space.bilibili.com/ajax/member/GetInfo', headers=head,  data=payload).content
print(jscontent)

jsDict = json.loads(jscontent.decode())

print(jsDict)
if jsDict['status'] == True:
    UserInfo = dict() #人员信息
    UserInfo['DisplayRank'] = jsDict['data']['DisplayRank'] #显示等级
    UserInfo['theme_preview'] = jsDict['data']['theme_preview'] #主体预览
    UserInfo['playNum'] = int(jsDict['data']['playNum'])  #播放量
    UserInfo['coins'] = int(jsDict['data']['coins']) #硬币数
    UserInfo['regtime'] = int(jsDict['data']['regtime']) #注册时间
    UserInfo['pendant'] = jsDict['data']['pendant'] #json
    UserInfo['approve'] = jsDict['data']['approve']
    UserInfo['theme'] = jsDict['data']['theme'] #主题
    UserInfo['sign'] = jsDict['data']['sign'] #签名
    UserInfo['name'] = jsDict['data']['name'] #姓名
    UserInfo['nameplate'] = jsDict['data']['nameplate']#名牌json
    UserInfo['article'] = int(jsDict['data']['article']) #文章
    UserInfo['rank'] = jsDict['data']['rank'] #等级
    UserInfo['attention'] = jsDict['data']['attention'] #注意
    UserInfo['fans'] = int(jsDict['data']['fans']) #粉丝数
    UserInfo['face'] = jsDict['data']['face'] #头像
    UserInfo['official_verify'] = jsDict['data']['official_verify'] #官方验证 json
    UserInfo['attentions'] = jsDict['data']['attentions'] #注意事项
    UserInfo['spacesta'] = int(jsDict['data']['spacesta'])
    UserInfo['birthday'] = jsDict['data']['birthday'] #生日
    UserInfo['sex'] = jsDict['data']['sex'] #性别
    UserInfo['description'] = jsDict['data']['description'] #描述
    UserInfo['friend'] = int(jsDict['data']['friend']) #朋友
    UserInfo['level_info'] = jsDict['data']['level_info'] #等级信息json
    UserInfo['place'] = jsDict['data']['place'] #地址
    UserInfo['mid'] = jsDict['data']['mid'] #ID
    UserInfo['im9_sign'] = jsDict['data']['im9_sign']
    UserInfo['toutu'] = jsDict['data']['toutu'] #头像

    try:
        biliuser.insert(UserInfo)
    except:
        print("存储用户"+jsDict['data']['name']+"时发生错误")
