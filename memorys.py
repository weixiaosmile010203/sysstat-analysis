import pyecharts.options as opts
from pyecharts.charts import Line, Page
from pyecharts.commons.utils import JsCode
import json
import os

def format_memory(mem_size):
    if mem_size < 1e3:  # 小于1GB，以MB为单位显示
        return f"{mem_size:.2f} MB"
    else:  # 大于等于1GB，以GB为单位显示
        return f"{mem_size / 1e3:.2f} GB"
    

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
memcache = []
membuffer = []
memswpfree = []
memswpused = []
memswpused_percent = []
# memswpcad = []
# memswpcad_percent = []


for memory in memorys:
    memfree.append(memory['memfree'])
    memused.append(memory['memused'])
    memavail.append(memory['avail'])
    memused_percent.append(memory['memused-percent'])
    memcache.append(memory['cached'])
    membuffer.append(memory['buffers'])
    memswpfree.append(memory['swpfree'])
    memswpused.append(memory['swpused'])
    memswpused_percent.append(memory['swpused-percent'])
    # memswpcad.append(memory['swpcad'])
    # memswpcad_percent.append(memory['swpcad-percent'])

# 创建内存使用率折线图表
mem_user_percent = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("memused_percent", memused_percent, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.2),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="内存使用率", pos_top="1%"),
        legend_opts=opts.LegendOpts(pos_top="1%"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
        yaxis_opts=opts.AxisOpts(max_=100),
        # brush_opts 配置用于设置 datazoom 的相关参数
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, pos_bottom="1%")],
    )
)

mem_use = (
    Line()
    .add_xaxis(timestamp_list) 
    .add_yaxis("mem_used", memused, is_smooth=True)
    .add_yaxis("mem_avail", memavail, is_smooth=True)
    .add_yaxis("mem_free", memfree, is_smooth=True)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="已使用内存", pos_top="1%"),
        legend_opts=opts.LegendOpts(pos_top="1%"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, pos_bottom="1%")],
    )
)

mem_cache = (
    Line()
    .add_xaxis(timestamp_list) 
    .add_yaxis("mem_used", memused, is_smooth=True)
    .add_yaxis("mem_buffer", membuffer, is_smooth=True)
    .add_yaxis("mem_cached", memcache, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="缓存", pos_top="1%"),
        legend_opts=opts.LegendOpts(pos_top="1%"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, pos_bottom="1%")],
    )
)

mem_swap_percent = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("swap使用率", memswpused_percent, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.2),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="swap使用率", pos_top="1%"),
        legend_opts=opts.LegendOpts(pos_top="1%"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
        yaxis_opts=opts.AxisOpts(max_=100),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, pos_bottom="1%")],
    )
)

mem_swap_used = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("swap使用", memswpused_percent, is_smooth=True, stack="swap_total")
    .add_yaxis("swap剩余", memswpfree, is_smooth=True, stack="swap_total")
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.2),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="swap使用率", pos_top="1%"),
        legend_opts=opts.LegendOpts(pos_top="1%"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, pos_bottom="1%")],
    )
)


page = Page()
page.page_title = "内存详情"
page.add(mem_user_percent)
page.add(mem_use)
page.add(mem_cache)
page.add(mem_swap_percent)
page.add(mem_swap_used)
page.render("memory.html")