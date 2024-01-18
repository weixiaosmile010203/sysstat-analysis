import pyecharts.options as opts
from pyecharts.charts import Line, Page
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
            

# for cpu in cpus:
#     print(cpu.get('cpu'))
#     print(cpu)
    
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
    # print(cpu['cpu'], cpu['usr'])
# 初始化页面
page = Page()

# 遍历每个 CPU 的数据，创建对应的图表
cores = []
for cpu in cpus:
    if cpu['cpu'] not in cores:
        cores.append(cpu['cpu'])
for i in cores:   
    # 创建 Line 图表
    print(i)
    line = Line()
    line.add_xaxis(timestamp_list)
    line.add_yaxis(f"{i}_usr", cpu_usr_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.add_yaxis(f"{i}_nice", cpu_nice_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.add_yaxis(f"{i}_sys", cpu_sys_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.add_yaxis(f"{i}_iowait", cpu_iowait_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.add_yaxis(f"{i}_steal", cpu_steal_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.add_yaxis(f"{i}_irq", cpu_irq_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.add_yaxis(f"{i}_soft", cpu_soft_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.add_yaxis(f"{i}_guest", cpu_guest_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.add_yaxis(f"{i}_gnice", cpu_gnice_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line.add_yaxis(f"{i}_idle", cpu_idle_list[i], label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    
    # 设置图表的标题和全局选项
    line.set_global_opts(
        title_opts=opts.TitleOpts(title=f"CPU %s Usage Over Time" % i
                      , title_textstyle_opts=opts.TextStyleOpts(font_size=25)
                      ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"
                                      , background_color="rgba(245, 245, 245, 0.8)"
                                      , border_width=1
                                      , border_color="#ccc"
                                      , textstyle_opts=opts.TextStyleOpts(color="#000")
                                      ),
        # 设置 Y 轴为值轴
        yaxis_opts=opts.AxisOpts(type_="value", axistick_opts=opts.AxisTickOpts(is_show=True)),
        # 设置 X 轴为时间轴
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False, axistick_opts=opts.AxisTickOpts(is_show=True)),
        # 设置图例
        legend_opts=opts.LegendOpts(pos_right="-10", pos_top="middle", orient="vertical",),
        # 设置数据缩放
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
        # 设置工具箱
        toolbox_opts=opts.ToolboxOpts(is_show=False,
                                      feature={
                "dataZoom": {"title": {"zoom": "区域缩放", "zoomin": "局部缩放", "zoomout": "全局缩放"}},
                "magicType": {"title": {"line": "切换为折线图", "bar": "切换为柱状图"}},
                "restore": {"title": "还原"},
                "saveAsImage": {"title": "保存为图片"},
            }),
    )
    
    # 将图表添加到页面
    page.add(line)

# 渲染页面，生成 HTML 文件，可以在浏览器中打开查看所有图表
page.render("cpu_usage_all.html")
