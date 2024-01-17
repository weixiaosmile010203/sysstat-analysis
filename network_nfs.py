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


nfs_call = []
nfs_retrans = []
nfs_read = []
nfs_write = []
nfs_access = []
nfs_getatt = []
nfsd_scall = []
nfsd_badcall = []
nfsd_packet = []
nfsd_udp = []
nfsd_tcp = []
nfsd_hit = []
nfsd_miss = []
nfsd_sread = []
nfs_swrite = []
nfsd_saccess = []
nfsd_sgetatt = []

for nets in networks:
    nfs_call.append(nets['net-nfs']['call'])
    nfs_retrans.append(nets['net-nfs']['retrans'])
    nfs_read.append(nets['net-nfs']['read'])
    nfs_write.append(nets['net-nfs']['write'])
    nfs_access.append(nets['net-nfs']['access'])
    nfs_getatt.append(nets['net-nfs']['getatt'])
    nfsd_scall.append(nets['net-nfsd']['scall'])
    nfsd_badcall.append(nets['net-nfsd']['badcall'])
    nfsd_packet.append(nets['net-nfsd']['packet'])
    nfsd_udp.append(nets['net-nfsd']['udp'])
    nfsd_tcp.append(nets['net-nfsd']['tcp'])
    nfsd_hit.append(nets['net-nfsd']['hit'])
    nfsd_miss.append(nets['net-nfsd']['miss'])
    nfsd_sread.append(nets['net-nfsd']['sread'])
    nfs_swrite.append(nets['net-nfsd']['swrite'])
    nfsd_saccess.append(nets['net-nfsd']['saccess'])
    nfsd_sgetatt.append(nets['net-nfsd']['sgetatt'])


call = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("call", nfs_call, is_smooth=True)
    .add_yaxis("retrans", nfs_retrans, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="call"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )
)

readwrite = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("read", nfs_read, is_smooth=True)
    .add_yaxis("write", nfs_write, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="readwrite"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )
)

access = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("access", nfs_access, is_smooth=True)
    .add_yaxis("getatt", nfs_getatt, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="access"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )
)

nfsd_scall = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("scall", nfsd_scall, is_smooth=True)
    .add_yaxis("badcall", nfsd_badcall, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="nfsd_scall"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )

)

nfsd_packet = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("packet", nfsd_packet, is_smooth=True)
    .add_yaxis("udp", nfsd_udp, is_smooth=True)
    .add_yaxis("tcp", nfsd_tcp, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="nfsd_packet"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )
)

nfsd_cache = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("hit", nfsd_hit, is_smooth=True)
    .add_yaxis("miss", nfsd_miss, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="nfsd_cache"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )
)

nfsd_readwrite = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("sread", nfsd_sread, is_smooth=True)
    .add_yaxis("swrite", nfs_swrite, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="nfsd_sreadwrite"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )
)

nfsd_saccess = (
    Line()
    .add_xaxis(timestamp_list)
    .add_yaxis("saccess", nfsd_saccess, is_smooth=True)
    .add_yaxis("sgetatt", nfsd_sgetatt, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="nfsd_saccess"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )
)

page=Page(layout=Page.SimplePageLayout)
page.add(call)
page.add(readwrite)
page.add(access)
page.add(nfsd_scall)
page.add(nfsd_packet)
page.add(nfsd_cache)
page.add(nfsd_readwrite)
page.add(nfsd_saccess)
page.render("nfs.html")