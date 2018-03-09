# 哔哩哔哩爬虫 mongoDB版
# -*- coding: utf-8 -*-
__author__ = 'netuser'
from spider import SpiderHTML
from multiprocessing import Pool
import sys, urllib, http, os, re, time, codecs, json
from pymongo import MongoClient

# 从本地记录里获取曾经爬取过的视频号
f = open('avlist.txt', 'r')
avSet = set([])
for line in f:
    avSet = set(line.split(','))
#数据库设置
conn = MongoClient('127.0.0.1',27017)
db = conn.bilibili
biliavinfo = db.bili_avinfo


pattern = re.compile(r'\d+')  # 获取av号的正则表达式
orders = {"hot": "播放量", "review": "评论数", "promote": "硬币数", "stow": "收藏数"}
biliUrl = 'http://www.bilibili.com'


class BilibiliSpider(SpiderHTML):
    def __init__(self, module, timeStart, timeEnd, limit):
        self.url = biliUrl + '/video/' + module + '.html'
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.limit = limit

    def start(self):
        content = self.getUrl(self.url)
        print(content)
        sorts = content.find('ul', class_='n_num')
        subSorts = sorts.find_all('a')

        # 处理该类别下的子模块
        for sub in subSorts:
            subName = sub.string
            if (subName == '全部'):
                continue
            # 子模块只需要tid即可
            tid = sub.parent['tid']
            if tid is None or tid == '':
                print('模块{type} tid解析错误'.format(type=subName))
                continue
            self.parsePage(subName, tid)

    # 处理一个子模块的页面
    def parsePage(self, typeName, tid):
        for (order, name) in orders.items():
            sumData = dict()
            print("对子模块‘{typeName}’进行‘{name}’排序的分析".format(name=name, typeName=typeName))
            sort = 0;
            # 是否获取到足够的排名
            isBreak = False
            for page in range(1, 5):
                urlTmp = biliUrl + "/list/{order}-{tid}-{page}-{start}~{end}.html".format(order=order, tid=tid,
                                                                                          page=page,
                                                                                          start=self.timeStart,
                                                                                          end=self.timeEnd)
                content = self.getUrl(urlTmp)

                videoContent = content.find('ul', class_='vd-list l1')
                try:
                    videoList = videoContent.find_all('div', class_='l-item')
                except:
                    print("错误连接地址：")
                    print(urlTmp)
                for video in videoList:
                    AVInfo = dict()  # 作品信息
                    AVInfo['av'] = pattern.search(video.find('a', class_='title')['href']).group()  # av号
                    AVInfo['title'] = video.find('a', class_='title').string  # 标题
                    sort = sort + 1
                    if AVInfo['av'] in avSet:
                        print("已经爬取过该视频av{av},{title}".format(**AVInfo))
                        continue

                    AVInfo['author_name'] = video.find('a', class_='v-author').string  # 作者
                    AVInfo['module'] = typeName  # 模块名
                    AVInfo['tid'] = tid  # 模块id
                    coinInfo = self.parseAV(AVInfo['av'])  # 解析详细视频页面获取硬币和收藏数
                    if coinInfo == 0:
                        sort = sort - 1
                        print("作品名：{title},【视频信息获取失败】".format(**AVInfo))
                        continue

                    AVInfo['play'] = int(video.find('span', class_='v-info-i gk').span.string.replace("--","0"))  # 播放数
                    AVInfo['danmu'] = int(video.find('span', class_='v-info-i dm').span.string.replace("--","0"))  # 弹幕数
                    AVInfo['collect'] = int(video.find('span', class_='v-info-i sc').span.string.replace("--","0"))  # 收藏数
                    AVInfo['url'] = biliUrl + video.find('a', class_='title')['href']  # 视频链接
                    AVInfo['desc'] = video.find('div', class_='v-desc').string  # 视频描述
                    AVInfo['author'] = video.find('a', class_='v-author')['href'].split('/')[-1]  # 用户id
                    # 将此视频加入已经爬取过的列表
                    avSet.add(AVInfo['av'])
                    AVInfo['mtime'] = int(time.time())
                    AVInfo['ctime'] = int(time.time())
                    # 合并信息
                    AVInfo = dict(coinInfo, **AVInfo)

                    print("排名第{sort}：\t{author_name},\t播放量:{play},\t收藏数:{collect},\t硬币数:{coin},\t作品名：{title}".format(
                        sort=sort, **AVInfo))
                    biliavinfo.insert(AVInfo)
                    if sort >= self.limit:
                        isBreak = True
                        break
                if isBreak == True:
                    break
        # 全部获取完毕，保存av号
        with codecs.open('avlist.txt', encoding='utf-8', mode='w') as f:
            f.write(','.join(str(s) for s in avSet))

    # 解析单独的一个视频
    def parseAV(self, avNum):
        url = "http://api.bilibili.com/archive_stat/stat?callback=&aid={av}&type=jsonp&_={time}".format(av=avNum,
                                                                                                        time=int(
                                                                                                            time.time() * 1000))
        info = dict()

        try:
            content = self.getUrl(url).find('p').string
            data = str(content)
            data = json.loads(data)
            info['coin'] = data['data']['coin']
            info['share'] = data['data']['share']
        except:
            return 0;
        return info


# module  分类:动画 音乐 舞蹈 游戏 科技 生活 鬼畜 时尚 娱乐
module = 'dance'
all_model = {'douga','music','dance','game','technology','life','kichiku','fashion','ent'}
# 热度统计开始时间
start = '2016-09-01'
# 热度统计结束时间
end = '2016-09-27'
# 单个模块排名获取个数100以内
limit = 40
for zmodule in all_model:
    spider = BilibiliSpider(zmodule, start, end, limit)
    print("分析周期：`{start}` ~ `{end}`".format(start=start, end=end))
    spider.start()