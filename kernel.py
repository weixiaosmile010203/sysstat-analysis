import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))
# 获取时间戳列表
timestamps = []
kernels = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        kernels.append(statistic['kernel'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))

dentunusd = [] # 表示当前未使用的内核密钥密钥槽位的数量。内核密钥是 Linux 内核中用于安全密钥管理的机制，而这个指标表示未使用的密钥槽位数量。
file_nr = [] # 表示当前系统中打开的文件数量。这包括所有类型的文件，包括普通文件、目录和套接字。
inode_nr = [] # 表示当前系统中打开的 inode 数量。inode 是 Linux 文件系统中的数据结构，用于存储文件的元数据。
pty_nr = [] # 表示当前系统中分配的伪终端数量。伪终端是一种虚拟的终端设备，通常用于创建终端会话，该指标表示已分配的伪终端数量。

for kernel in kernels:
    dentunusd.append(kernel['dentunusd'])
    file_nr.append(kernel['file-nr'])
    inode_nr.append(kernel['inode-nr'])
    pty_nr.append(kernel['pty-nr'])


# 图1: 文件句柄和inode数量
line1 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("文件句柄数量", file_nr)
    .add_yaxis("inode数量", inode_nr)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="文件句柄和inode数量"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)]
    )
)

# 图2: 未使用的内核密钥密钥槽位数量
line2 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("未使用的内核密钥密钥槽位数量", dentunusd)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="未使用的内核密钥密钥槽位数量"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)]
    )
)

# 图3: 伪终端数量
line3 = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("伪终端数量", pty_nr)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="伪终端数量"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)]
    )
)

# 将图表添加到页面中
page = Page()
page.add(line1)
page.add(line2)
page.add(line3)
page.render("kernel_analysis.html")
