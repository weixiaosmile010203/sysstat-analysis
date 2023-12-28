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


import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker


c = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("free", memfree, is_smooth=True)
    .add_yaxis("used", memused, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="内存使用"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100)],
    )
    .render("line_areastyle_boundary_gap.html")
)
