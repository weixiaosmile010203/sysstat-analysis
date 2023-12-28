import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json
import os

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))
# 获取时间戳列表
timestamps = []
memorys = []

# 遍历数据结构
for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        memorys.append(statistic['memory'])
timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))

memfree = []
memused = []
memavail = []
for memory in memorys:
    memfree.append(memory['memfree'])
    memused.append(memory['memused'])

print(len(timestamp_list))
print(len(memfree))


line = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("内存", memfree,  is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="内存剩余情况"))

)
line.render('memory.html')