import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa17.json')))
# 获取时间戳列表
timestamps = []
hugepages = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        hugepages.append(statistic['hugepages'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))

hugfree = [] # 表示当前系统中空闲的巨大页面的数量。巨大页面是一种较大的内存页面，通常比标准页面的大小大得多。它们用于减少页表的数量，提高内存访问效率。
hugused = [] # 表示当前系统中已经被使用的巨大页面的数量。这些页面已经被分配给进程或系统使用。
hugused_percent = [] # 表示已使用的巨大页面数量占总巨大页面数量的百分比。这可以帮助评估系统对巨大页面的利用程度。
hugrsvd = [] # 表示当前系统中被保留但尚未被分配的巨大页面的数量。这些页面已经被保留，但还没有实际分配给任何进程。
hugsurp = [] # 表示当前系统中多余的巨大页面的数量。这表示系统中存在的但未被使用的额外巨大页面。

for hp in hugepages:
    hugfree.append(hp['hugfree'])
    hugused.append(hp['hugused'])
    hugused_percent.append(hp['hugused-percent'])
    hugrsvd.append(hp.get('hugrsvd', 0))
    hugsurp.append(hp.get('hugsurp', 0))


page = Page()
# 图1: 巨大页面使用情况
line1 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("已使用大页", hugused)
    .add_yaxis("空闲大页", hugfree)
    .set_global_opts(title_opts=opts.TitleOpts(title="大页使用情况" , subtitle="单位：页"))
)
page.add(line1)

# 图2: 已使用巨大页面百分比
line2 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("已使用大页百分比", hugused_percent)
    .set_global_opts(title_opts=opts.TitleOpts(title="已使用大页百分比", subtitle="单位：%"))
)
page.add(line2)

# 图3: 保留和多余的巨大页面
line3 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("保留的大页", hugrsvd)
    .add_yaxis("多余的大页", hugsurp)
    .set_global_opts(title_opts=opts.TitleOpts(title="保留和多余的大页", subtitle="单位：页"))
)
page.add(line3)
page.render("hugepages.html")