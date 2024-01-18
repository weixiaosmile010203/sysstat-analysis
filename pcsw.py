import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))
# 获取时间戳列表
timestamps = []
pcsw = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        pcsw.append(statistic['process-and-context-switch'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))

process = []
content = []

for pc in pcsw:
    process.append(pc['proc'])
    content.append(pc['cswch'])


page = Page()
chart1 = Line()
chart1.add_xaxis(timestamp_list)
chart1.add_yaxis("process", process)
chart1.set_global_opts(title_opts=opts.TitleOpts(title="每秒进程切换数", subtitle="单位：个"))

chart2 = Line()
chart2.add_xaxis(timestamp_list)
chart2.add_yaxis("content", content)
chart2.set_global_opts(title_opts=opts.TitleOpts(title="每秒上下文切换次数", subtitle="单位：个"))
page.add(chart1)
page.add(chart2)
page.render("pcsw.html")