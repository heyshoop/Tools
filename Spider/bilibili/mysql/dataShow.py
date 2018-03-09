#数据可视化
# -*- coding: utf-8 -*-
from plistlib import Data

import pymysql
import pandas as pd
import plotly
import plotly.graph_objs
from bokeh.charts import Scatter
from bokeh.plotting import Figure
from matplotlib.axis import XAxis, YAxis
from openpyxl.chart.layout import Layout

from plotly.graph_objs import *


pymysql.install_as_MySQLdb()

#配置数据库连接
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='datamining', port=3306, use_unicode=True, charset="utf8")
cur = conn.cursor()

#查询数据
cur.execute("SELECT B.author_name,B.play,B.danmu,B.`share`,B.coin,B.title FROM BILIBILI B ORDER BY B.coin DESC")
rows = cur.fetchall()
#格式化数据
df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'author_name', 1: 'play', 2: 'danmu', 3: 'share', 4:'coin',5:'title'}, inplace=True);
df = df.sort_values(['play'], ascending=[0]);
#定义纵横坐标
trace1 = Scatter(
    x=df['play'],
    y=df['coin'],
    text=df['author_name']+":"+df['title'],
    mode='markers'
)
#定义纵横坐标显示
layout = Layout(
    title='哔哩哔哩近9月数据统计 ',
    xaxis=XAxis( type='log', title='播放量' ),
    yaxis=YAxis( title='投币数' ),
)
#生成页面
data = Data([trace1])
fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='BiliBli.html')