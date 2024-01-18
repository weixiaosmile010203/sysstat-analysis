import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))
# 获取时间戳列表
timestamps = []
paging = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        paging.append(statistic['paging'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))
    
pgpgin = []
pgpgout = []
fault = []
majflt = []
pgfree = []
pgscank = []
pgscand = []
pgsteal = []
vmeff_percent = []

for pg in paging:
    pgpgin.append(pg['pgpgin'])
    pgpgout.append(pg['pgpgout'])
    fault.append(pg['fault'])
    majflt.append(pg['majflt'])
    pgfree.append(pg['pgfree'])
    pgscank.append(pg['pgscank'])
    pgscand.append(pg['pgscand'])
    pgsteal.append(pg['pgsteal'])
    vmeff_percent.append(pg['vmeff-percent'])

page = Page()

# 图1: 缺页中断和主缺页中断
line1 = Line()
line1.add_xaxis(timestamp_list)
line1.add_yaxis("fault", fault)
line1.add_yaxis("majflt", majflt)
line1.set_global_opts(title_opts=opts.TitleOpts(title="缺页中断和主缺页中断", subtitle="单位：次"),
                      datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)])
page.add(line1)

# 图2: 读写和交换活动
line2 = Line()
line2.add_xaxis(timestamp_list)
line2.add_yaxis("pgpgin", pgpgin)
line2.add_yaxis("pgpgout", pgpgout)
line2.add_yaxis("pgsteal", pgsteal)
line2.set_global_opts(title_opts=opts.TitleOpts(title="读写和交换活动", subtitle="单位：页面/秒"),
                      datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)])
page.add(line2)

# 图3: 空闲页面和扫描页面
line3 = Line()
line3.add_xaxis(timestamp_list)
line3.add_yaxis("pgfree", pgfree)
line3.add_yaxis("pgscank", pgscank)
line3.add_yaxis("pgscand", pgscand)
line3.set_global_opts(title_opts=opts.TitleOpts(title="空闲页面和扫描页面", subtitle="单位：页面/秒"),
                      datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)])
page.add(line3)

# 图4: 页面偷取
line4 = Line()
line4.add_xaxis(timestamp_list)
line4.add_yaxis("pgsteal", pgsteal)
line4.set_global_opts(title_opts=opts.TitleOpts(title="页面偷取",subtitle="单位：页面/秒"),
                      datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)])
page.add(line4)

# 图5: 虚拟内存效率
line5 = Line()
line5.add_xaxis(timestamp_list)
line5.add_yaxis("vmeff-percent", vmeff_percent)
line5.set_global_opts(title_opts=opts.TitleOpts(title="虚拟内存效率", subtitle="单位：百分比"),
                      datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
                      yaxis_opts=opts.AxisOpts(max_=100),)
page.add(line5)

page.render("paging.html")