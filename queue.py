import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))
# 获取时间戳列表
timestamps = []
queues = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        queues.append(statistic['queue'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))

# Create empty lists for each key in the "queue" dictionary
runq_sz_list = [] # 表示当前运行队列的大小，即正在等待在 CPU 上执行的进程的数量。
plist_sz_list = [] # 表示当前可运行进程的列表大小，即在内核中准备运行但尚未分配 
ldavg_1_list = [] # 表示系统的 1 分钟平均负载。平均负载是指在一段时间内运行队列中的平均进程数量。这里显示的是过去 1 分钟的平均值。
ldavg_5_list = [] # 表示系统的 5 分钟平均负载。与 ldavg-1 类似，这里显示的是过去 5 分钟的平均值。
ldavg_15_list = [] # 表示系统的 15 分钟平均负载。同样，这里显示的是过去 15 分钟的平均值。
blocked_list = [] # 表示当前被阻塞（无法运行）的进程数量。

for queue in queues:
    runq_sz_list.append(queue['runq-sz'])
    plist_sz_list.append(queue['plist-sz'])
    ldavg_1_list.append(queue['ldavg-1'])
    ldavg_5_list.append(queue['ldavg-5'])
    ldavg_15_list.append(queue['ldavg-15'])
    blocked_list.append(queue['blocked'])


# Create the first chart for runq-sz and plist-sz
chart1 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("runq-sz", runq_sz_list)
    .add_yaxis("plist-sz", plist_sz_list)
    .set_global_opts(title_opts=opts.TitleOpts(title="运行队列和可运行进程数量"),
                     datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)])
)

# Create the second chart for ldavg-1, ldavg-5, and ldavg-15
chart2 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("ldavg-1", ldavg_1_list)
    .add_yaxis("ldavg-5", ldavg_5_list)
    .add_yaxis("ldavg-15", ldavg_15_list)
    .set_global_opts(title_opts=opts.TitleOpts(title="平均负载"),
                     datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)])
)

# Create the third chart for blocked
chart3 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("blocked", blocked_list)
    .set_global_opts(title_opts=opts.TitleOpts(title="阻塞的进程数量"),
                     datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)])
)

# Create a page to display all charts
page = Page()
page.add(chart1)
page.add(chart2)
page.add(chart3)
page.render("queue_analysis.html")
