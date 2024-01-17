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

softnet_total = {}
softnet_dropd = {}
softnet_squeezed = {}
softnet_rx_rps = {}
softnet_flw_lim = {}


for nets in networks:
    for net in nets['softnet']:
        print(net)
        softnet_total[net['cpu']] = softnet_total.get(net['cpu'], []) + [net['total']]
        softnet_dropd[net['cpu']] = softnet_dropd.get(net['cpu'], []) + [net['dropd']]
        softnet_squeezed[net['cpu']] = softnet_squeezed.get(net['cpu'], []) + [net['squeezd']]
        softnet_rx_rps[net['cpu']] = softnet_rx_rps.get(net['cpu'], []) + [net['rx_rps']]
        softnet_flw_lim[net['cpu']] = softnet_flw_lim.get(net['cpu'], []) + [net['flw_lim']]
print(softnet_total)

page=Page()
for i in softnet_total:
    softnet = (
        Line()
        .add_xaxis(timestamp_list)
        .add_yaxis("total", softnet_total[i], is_smooth=True)
        .add_yaxis("dropd", softnet_dropd[i], is_smooth=True)
        .add_yaxis("squeezed", softnet_squeezed[i], is_smooth=True)
        .add_yaxis("rx_rps", softnet_rx_rps[i], is_smooth=True)
        .add_yaxis("flw_lim", softnet_flw_lim[i], is_smooth=True)
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="cpu {} softnet".format(i)),
                         datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
                         )
    )
    page.add(softnet)
page.render("network_softnet.html")