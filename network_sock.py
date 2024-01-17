import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os
from pyecharts.options import InitOpts

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))
# 获取时间戳列表
timestamps = []
networks = []

for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        networks.append(statistic['network'])

timestamp_list = []
for timestamp in timestamps:
    timestamp_list.append(timestamp.get('date') + ' ' + timestamp.get('time'))


net_sock = []
net_tcp = []
net_udp = []
net_raw = []
net_frag = []
net_tw = []

for nets in networks:
    net_sock.append(nets['net-sock']['totsck'])
    net_tcp.append(nets['net-sock']['tcpsck'])
    net_udp.append(nets['net-sock']['udpsck'])
    net_raw.append(nets['net-sock']['rawsck'])
    net_frag.append(nets['net-sock']['ip-frag'])
    net_tw.append(nets['net-sock']['tcp-tw'])


net_sock = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("totsck", net_sock, is_smooth=True)
    .add_yaxis("tcpsck", net_tcp, is_smooth=True)
    .add_yaxis("udpsck", net_udp, is_smooth=True)
    .add_yaxis("rawsck", net_raw, is_smooth=True)
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="total socket"),
                     datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
                     )
)

net_sock_ip = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("ip-frag", net_frag, is_smooth=True)
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="ip-frag"),
                     datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],)

)

net_sock_tw = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("tcp-tw", net_tw, is_smooth=True)
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="tcp-tw"),
                     datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],)


)


page=Page()
page.add(net_sock)
page.add(net_sock_ip)
page.add(net_sock_tw)
page.render("network_sock.html")