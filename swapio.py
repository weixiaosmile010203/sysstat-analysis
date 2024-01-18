import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))
# 获取时间戳列表
timestamps = []
swapio = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        swapio.append(statistic['swap-pages'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))

pswpin = []
pswpout = []

for i in swapio:
    pswpin.append(i['pswpin'])
    pswpout.append(i['pswpout'])


page = Page()
chart1 = Line()
chart1.add_xaxis(timestamp_list)
chart1.add_yaxis("pswpin", pswpin)
chart1.add_yaxis("pswpout", pswpout)
chart1.set_global_opts(title_opts=opts.TitleOpts(title="swap-pages", subtitle="单位：页面/秒"),
                       datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="inside",)])

page.add(chart1)
page.render("swap.html")