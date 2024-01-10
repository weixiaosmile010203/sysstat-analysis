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
memused_percent = []
for memory in memorys:
    memfree.append(memory['memfree'])
    memused.append(memory['memused'])
    memavail.append(memory['avail'])
    memused_percent.append(memory['memused-percent'])
print(len(timestamp_list))
print(len(memfree))


import pyecharts.options as opts
from pyecharts.charts import Line, Grid
from pyecharts.faker import Faker


# 创建内存使用率折线图表
c = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("memused_percent", memused_percent, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="内存使用率", pos_top="5%"),
        legend_opts=opts.LegendOpts(pos_top="5%"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
        # brush_opts 配置用于设置 datazoom 的相关参数
        brush_opts=opts.BrushOpts(
            x_axis_index=0,
            brush_link="memory_brush",  # 设置 brush_link，确保两个图形联动
            brush_type="lineX",  # "lineX" 表示横向的 datazoom
        ),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, pos_bottom="1%")],
    )
)

# 创建内存使用折线图表
c2 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("free", memfree, is_smooth=True)
    .add_yaxis("used", memused, is_smooth=True)
    .add_yaxis("avail", memavail, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="内存使用", pos_top="50%"),
        legend_opts=opts.LegendOpts(pos_top="50%"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
        # brush_opts 配置用于设置 datazoom 的相关参数
        brush_opts=opts.BrushOpts(
            x_axis_index=0,
            brush_link="memory_brush",  # 设置 brush_link，确保两个图形联动
            brush_type="lineX",  # "lineX" 表示横向的 datazoom
        ),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, pos_bottom="20%")],
    )
)

# 创建两个 Grid 实例，设置纵向排列
grid = Grid(init_opts=opts.InitOpts(width="1000px", height="800px"))
grid.add(c, grid_opts=opts.GridOpts(pos_top="10%", pos_bottom="60%"))
grid.add(c2, grid_opts=opts.GridOpts(pos_top="70%", pos_bottom="10%"))

# 使用 render 方法保存为 HTML 文件
grid.render("memory.html")