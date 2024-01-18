import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))
# 获取时间戳列表
timestamps = []
io = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        io.append(statistic['io'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))

io_tps = []
io_rtps = []
io_wtps = []
io_bread = []
io_bwrtn = []
io_dtps = []
io_bdscd = []

for i in io:
    io_tps.append(i['tps'])
    io_rtps.append(i['io-reads']['rtps'])
    io_wtps.append(i['io-writes']['wtps'])
    io_bread.append(i['io-reads']['bread'])
    io_bwrtn.append(i['io-writes']['bwrtn'])
    io_dtps.append(i['io-discard']['dtps'])
    io_bdscd.append(i['io-discard']['bdscd'])

# Create the charts
page = Page()

# Chart 1: Overall I/O Operations Frequency
chart1 = Line()
chart1.add_xaxis(timestamp_list)
chart1.add_yaxis("tps", io_tps)
chart1.set_global_opts(title_opts=opts.TitleOpts(title="总体 I/O 操作频率", subtitle="单位：次/秒"))
page.add(chart1)

# Chart 2: Read and Write Operations Count
chart2 = Line()
chart2.add_xaxis(timestamp_list)
chart2.add_yaxis("rtps", io_rtps)
chart2.add_yaxis("wtps", io_wtps)
chart2.set_global_opts(title_opts=opts.TitleOpts(title="读写操作次数" ,subtitle="单位：次/秒"))
page.add(chart2)

# Chart 3: Read and Write Data Volume
chart3 = Line()
chart3.add_xaxis(timestamp_list)
chart3.add_yaxis("readData", io_bread)
chart3.add_yaxis("writeData", io_bwrtn)
chart3.set_global_opts(title_opts=opts.TitleOpts(title="读写数据量" ,subtitle="单位：KB/秒"))
page.add(chart3)

# Chart 4: Discard Operations
chart4 = Line()
chart4.add_xaxis(timestamp_list)
chart4.add_yaxis("Discard Operations", io_dtps)
chart4.add_yaxis("Discard Data Volume", io_bdscd)
chart4.set_global_opts(title_opts=opts.TitleOpts(title="丢弃操作", subtitle="单位：次/秒"))
page.add(chart4)


page.render("io.html")
