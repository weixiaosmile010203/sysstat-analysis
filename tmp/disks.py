import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa17.json')))
# 获取时间戳列表
timestamps = []
disks = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        disks.append(statistic['disk'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))


disk_tps = {} # 表示每秒钟的传输次数 (transactions per second)。即每秒磁盘处理的 I/O 操作次数。
disk_rd_sec = {} # 表示每秒钟的读取扇区数 (reads per second)。一个扇区通常是512字节。
disk_wr_sec = {} # 表示每秒钟的写入扇区数 (writes per second)。一个扇区通常是512字节。
disk_dc_sec = {} # 表示每秒钟从磁盘读取的扇区的数量。
disk_rkB = {} # 表示每秒钟的读取数据量 (reads in kilobytes per second)。
disk_wkB = {} # 表示每秒钟的写入数据量 (writes in kilobytes per second)。
disk_dkB = {} # 表示每秒钟从磁盘读取的数据量 (data in kilobytes per second)。
disk_avgrq_sz = {}  #表示平均每个请求的扇区数 (average request size)。
disk_avgqu_sz = {} # 表示平均 I/O 请求队列的长度 (average queue size)。通常，如果此值大于1，表示系统中有请求正在排队等待处理。
disk_areq_sz = {} # 表示平均每个 I/O 请求的扇区数 (average request size)。
disk_aqu_sz = {} # 表示 I/O 请求队列的长度 (current queue size)。
disk_await = {} # 表示平均 I/O 操作的等待时间 (average time for I/O requests to be served)。单位是毫秒。
disk_util = {} # 表示磁盘的利用率百分比。表示磁盘的工作百分比，即磁盘非空闲时间所占的百分比。

for disk in disks:
    for i in disk:
        disk_tps[i['disk-device']] = disk_tps.get(i['disk-device'], []) + [i['tps']]
        disk_rd_sec[i['disk-device']] = disk_rd_sec.get(i['disk-device'], []) + [i['rd_sec']]
        disk_wr_sec[i['disk-device']] = disk_wr_sec.get(i['disk-device'], []) + [i['wr_sec']]
        disk_dc_sec[i['disk-device']] = disk_dc_sec.get(i['disk-device'], []) + [i.get('dc_sec', 0)] # 兼容低版本sysstat输出的不同列
        disk_rkB[i['disk-device']] = disk_rkB.get(i['disk-device'], []) + [i['rkB']]
        disk_wkB[i['disk-device']] = disk_wkB.get(i['disk-device'], []) + [i['wkB']]
        disk_dkB[i['disk-device']] = disk_dkB.get(i['disk-device'], []) + [i.get('dkB', 0)] # 兼容低版本sysstat输出的不同列
        disk_avgrq_sz[i['disk-device']] = disk_avgrq_sz.get(i['disk-device'], []) + [i['avgrq-sz']]
        disk_avgqu_sz[i['disk-device']] = disk_avgqu_sz.get(i['disk-device'], []) + [i['avgqu-sz']]
        disk_areq_sz[i['disk-device']] = disk_areq_sz.get(i['disk-device'], []) + [i['areq-sz']]
        disk_aqu_sz[i['disk-device']] = disk_aqu_sz.get(i['disk-device'], []) + [i['aqu-sz']]
        disk_await[i['disk-device']] = disk_await.get(i['disk-device'], []) + [i['await']]
        disk_util[i['disk-device']] = disk_util.get(i['disk-device'], []) + [i['util-percent']]

# 初始化页面
page = Page()
for i in disk_tps:
    # 图1: I/O 操作频率
    line1 = (
        Line()
        .add_xaxis(timestamp_list)
        .add_yaxis("tps", disk_tps[i], is_smooth=True)
        .add_yaxis("rd_sec", disk_rd_sec[i], is_smooth=True)
        .add_yaxis("wr_sec", disk_wr_sec[i], is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="I/O 操作频率({})".format(i))
                         ,datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)]
                         )
    )
    page.add(line1)

    # 图2: 数据传输量
    line2 = (
        Line()
        .add_xaxis(timestamp_list)
        .add_yaxis("rkB", disk_rkB[i], is_smooth=True)
        .add_yaxis("wkB", disk_wkB[i], is_smooth=True)
        .add_yaxis("dkB", disk_dkB[i], is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="数据传输量({})".format(i))
                         ,datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)]
                         )
    )
    page.add(line2)

    # 图3: I/O 请求队列
    line3 = (
        Line()
        .add_xaxis(timestamp_list)
        .add_yaxis("avgqu-sz", disk_avgqu_sz[i], is_smooth=True)
        .add_yaxis("aqu-sz", disk_aqu_sz[i], is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="I/O 请求队列({})".format(i))
                         ,datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)]
                         )
    )
    page.add(line3)

    # 图4: 平均等待时间和利用率
    line4 = (
        Line()
        .add_xaxis(timestamp_list)
        .add_yaxis("await", disk_await[i], is_smooth=True)
        .add_yaxis("util-percent", disk_util[i], is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="平均等待时间和利用率({})".format(i))
                         ,datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)]
                         )
    )
    page.add(line4)
page.render("disk.html")

