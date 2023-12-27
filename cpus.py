import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker
import json
import os

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))
# 获取时间戳列表
timestamps = []
cpus = []

# 遍历数据结构
for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        # 获取 CPU 列表
        for cpu in statistic['cpu-load']:
            cpus.append(cpu)
            

for cpu in cpus:
    print(cpu.get('cpu'))
    print(cpu)
    
cpu_cores = data['sysstat']['hosts'][0]['number-of-cpus']

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))
cpu_usr_list = {}
cpu_nice_list = {}
cpu_sys_list = {}
cpu_iowait_list = {}
cpu_steal_list = {}
cpu_irq_list = {}
cpu_soft_list = {}
cpu_guest_list = {}
cpu_gnice_list = {}
cpu_idle_list = {}
for cpu in cpus:
    cpu_usr_list[cpu['cpu']] = cpu_usr_list.get(cpu['cpu'], []) + [cpu['usr']]
    cpu_nice_list[cpu['cpu']] = cpu_nice_list.get(cpu['cpu'], []) + [cpu['nice']]
    cpu_sys_list[cpu['cpu']] = cpu_sys_list.get(cpu['cpu'], []) + [cpu['sys']]
    cpu_iowait_list[cpu['cpu']] = cpu_iowait_list.get(cpu['cpu'], []) + [cpu['iowait']]
    cpu_steal_list[cpu['cpu']] = cpu_steal_list.get(cpu['cpu'], []) + [cpu['steal']]
    cpu_irq_list[cpu['cpu']] = cpu_irq_list.get(cpu['cpu'], []) + [cpu['irq']]
    cpu_soft_list[cpu['cpu']] = cpu_soft_list.get(cpu['cpu'], []) + [cpu['soft']]
    cpu_guest_list[cpu['cpu']] = cpu_guest_list.get(cpu['cpu'], []) + [cpu['guest']]
    cpu_gnice_list[cpu['cpu']] = cpu_gnice_list.get(cpu['cpu'], []) + [cpu['gnice']]
    cpu_idle_list[cpu['cpu']] = cpu_idle_list.get(cpu['cpu'], []) + [cpu['idle']]

# print(timestamp_list)
# c = (
#     Line()
#     .add_xaxis(timestamp_list)
#     .add_yaxis("usr", cpu_usr_list, is_smooth=True)
#     .add_yaxis("nice", cpu_nice_list, is_smooth=True)
#     .add_yaxis("sys", cpu_sys_list, is_smooth=True)
#     .add_yaxis("iowait", cpu_iowait_list, is_smooth=True)
#     .add_yaxis("steal", cpu_steal_list, is_smooth=True)
#     .add_yaxis("irq", cpu_irq_list, is_smooth=True)
#     .add_yaxis("soft", cpu_soft_list, is_smooth=True)
#     .add_yaxis("guest", cpu_guest_list, is_smooth=True)
#     .add_yaxis("gnice",  cpu_gnice_list, is_smooth=True)
#     .add_yaxis("idle", cpu_idle_list, is_smooth=True)
#     .set_series_opts(
#         areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
#         label_opts=opts.LabelOpts(is_show=True),
#     )
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="CPU Usage"),
#         xaxis_opts=opts.AxisOpts(
#             axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
#             is_scale=False,
#             boundary_gap=False,
#         ),
#     )
#     .render("line_areastyle_boundary_gap.html")
# )

import pyecharts.options as opts
from pyecharts.charts import Line

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://echarts.apache.org/examples/editor.html?c=area-stack

目前无法实现的功能:

暂无
"""





(
    Line()
    .add_xaxis(xaxis_data=timestamp_list)
    .add_yaxis(
        series_name="usr",
        stack="总量",
        y_axis=cpu_usr_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="nice",
        stack="总量",
        y_axis=cpu_nice_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="sys",
        stack="总量",
        y_axis=cpu_sys_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="iowait",
        stack="总量",
        y_axis=cpu_iowait_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="steal",
        stack="总量",
        y_axis=cpu_steal_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="irq",
        stack="总量",
        y_axis=cpu_irq_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="soft",
        stack="总量",
        y_axis=cpu_soft_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="guest",
        stack="总量",
        y_axis=cpu_guest_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="gnice",
        stack="总量",
        y_axis=cpu_gnice_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        series_name="idle",
        stack="总量",
        y_axis=cpu_idle_list,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="CPU使用率"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
            max_=100,
        ),
         datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
        ],
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),

    )
    .render("stacked_area_chart.html")
)
