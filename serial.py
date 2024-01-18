import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa17.json')))
# 获取时间戳列表
timestamps = []
serials = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        serials.append(statistic['serial'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))

line_rcvin = {} #  表示每秒从串口接收的字符数。
line_xmtin = {} #  表示每秒通过串口发送的字符数。
line_framerr = {} # 表示发生的帧错误的数量。帧错误通常表示串口接收到的数据帧不符合标准帧格式。
line_prtyerr = {} # 表示发生的奇偶校验错误的数量。奇偶校验错误表示在串口通信中，接收到的数据的奇偶校验不匹配。
line_brk = {} # 表示接收到的中断信号的数量。在串口通信中，中断信号可能表示通信的特殊情况。
line_ovrun = {} # 表示发生的溢出错误的数量。溢出错误通常表示串口接收缓冲区溢出。


for serial in serials:
    for line in serial:
        line_rcvin[line['line']] = line_rcvin.get(line['line'], []) + [line['rcvin']]
        line_xmtin[line['line']] = line_xmtin.get(line['line'], []) + [line['xmtin']]
        line_framerr[line['line']] = line_framerr.get(line['line'], []) + [line['framerr']]
        line_prtyerr[line['line']] = line_prtyerr.get(line['line'], []) + [line['prtyerr']]
        line_brk[line['line']] = line_brk.get(line['line'], []) + [line['brk']]
        line_ovrun[line['line']] = line_ovrun.get(line['line'], []) + [line['ovrun']]

page = Page()
for i in line_rcvin:
    # 图1: 串口接收和发送字符数
    line_chart1 = Line()
    line_chart1.add_xaxis(timestamp_list) 
    line_chart1.add_yaxis("接收字符数", line_rcvin[i])
    line_chart1.add_yaxis("发送字符数", line_xmtin[i])
    line_chart1.set_global_opts(title_opts=opts.TitleOpts(title="串口接收和发送字符数(line:{})".format(i), subtitle="单位：字符/秒"))
    page.add(line_chart1)

    # 图2: 串口错误数量
    line_chart2 = Line()
    line_chart2.add_xaxis(timestamp_list)
    line_chart2.add_yaxis("帧错误数", line_framerr[i])
    line_chart2.add_yaxis("奇偶校验错误数", line_prtyerr[i])
    line_chart2.add_yaxis("中断信号数", line_brk[i])
    line_chart2.add_yaxis("溢出错误数", line_ovrun[i])
    line_chart2.set_global_opts(title_opts=opts.TitleOpts(title="串口错误数量(line:{})".format(i), subtitle="单位：次"))
    page.add(line_chart2)
page.render('serial.html')