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


net_dev_rxkB = {}
net_dev_txkB = {}
net_dev_rxpck = {}
net_dev_txpck = {}
net_dev_rxcmp = {}
net_dev_txcmp = {}
net_dev_rxmcst = {}
net_dev_percent = {}
net_edev_rxerr = {}
net_edev_txerr = {}
net_edev_rxdrop = {}
net_edev_txdrop = {}
net_edev_rxfifo = {}
net_edev_txfifo = {}
net_edev_rxfram = {}
net_edev_coll = {}
net_edev_txcarr = {}

for nets in networks:
    for net in nets['net-dev']:
        if net['iface'] == 'lo':
            continue
        net_dev_rxkB[net['iface']] = net_dev_rxkB.get(net['iface'], []) + [net['rxkB']]
        net_dev_txkB[net['iface']] = net_dev_txkB.get(net['iface'], []) + [net['txkB']]
        net_dev_rxpck[net['iface']] = net_dev_rxpck.get(net['iface'], []) + [net['rxpck']]
        net_dev_txpck[net['iface']] = net_dev_txpck.get(net['iface'], []) + [net['txpck']]
        net_dev_rxcmp[net['iface']] = net_dev_rxcmp.get(net['iface'], []) + [net['rxcmp']]
        net_dev_txcmp[net['iface']] = net_dev_txcmp.get(net['iface'], []) + [net['txcmp']]
        net_dev_rxmcst[net['iface']] = net_dev_rxmcst.get(net['iface'], []) + [net['rxmcst']]
        net_dev_percent[net['iface']] = net_dev_percent.get(net['iface'], []) + [net['ifutil-percent']]
    for net in nets['net-edev']:
        if net['iface'] == 'lo':
            continue
        net_edev_rxerr[net['iface']] = net_edev_rxerr.get(net['iface'], []) + [net['rxerr']]
        net_edev_txerr[net['iface']] = net_edev_txerr.get(net['iface'], []) + [net['txerr']]
        net_edev_rxdrop[net['iface']] = net_edev_rxdrop.get(net['iface'], []) + [net['rxdrop']]
        net_edev_txdrop[net['iface']] = net_edev_txdrop.get(net['iface'], []) + [net['txdrop']]
        net_edev_rxfifo[net['iface']] = net_edev_rxfifo.get(net['iface'], []) + [net['rxfifo']]
        net_edev_txfifo[net['iface']] = net_edev_txfifo.get(net['iface'], []) + [net['txfifo']]
        net_edev_rxfram[net['iface']] = net_edev_rxfram.get(net['iface'], []) + [net['rxfram']]
        net_edev_coll[net['iface']] = net_edev_coll.get(net['iface'], []) + [net['coll']]
        net_edev_txcarr[net['iface']] = net_edev_txcarr.get(net['iface'], []) + [net['txcarr']]

page = Page(layout=Page.SimplePageLayout)
# 获取网卡的名称，进行遍历  
for iface in nets['net-dev']:
    if iface['iface'] == 'lo':
        continue
    dev_name = iface['iface']
    print(net_dev_percent)
    print(dev_name)
    print(net_dev_percent[dev_name])
    line = Line(init_opts=InitOpts(width="1800px", height="400px"))
    line.add_xaxis(timestamp_list)
    line.add_yaxis(f"{dev_name}_percent",
                   net_dev_percent[dev_name], 
                   label_opts=opts.LabelOpts(is_show=False),
                   areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    # 设置图表的标题和全局选项
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="{} ifutil-percent".format(dev_name)
                      , title_textstyle_opts=opts.TextStyleOpts(font_size=25,)
                      ),
        yaxis_opts=opts.AxisOpts(max_=100),
        # 设置数据缩放
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
        # 设置工具箱
    )
    line_pck = Line(init_opts=InitOpts(width="1800px", height="400px"))
    line_pck.add_xaxis(timestamp_list)
    line_pck.add_yaxis(f"{dev_name} 发送数据包",
                net_dev_txpck[dev_name], 
                label_opts=opts.LabelOpts(is_show=False), is_smooth=True)
    line_pck.add_yaxis(f"{dev_name} 接收数据包",
                net_dev_rxpck[dev_name], 
                label_opts=opts.LabelOpts(is_show=False), is_smooth=True)
    line_pck.add_yaxis(f"{dev_name} 发送错误的数量",
                net_edev_txerr[dev_name], 
                label_opts=opts.LabelOpts(is_show=False))
    line_pck.add_yaxis(f"{dev_name} 接收错误的数量",
                net_edev_rxerr[dev_name], 
                label_opts=opts.LabelOpts(is_show=False))
    line_pck.add_yaxis(f"{dev_name}  发送时的冲突数量",
                net_edev_coll[dev_name], 
                label_opts=opts.LabelOpts(is_show=False))
    line_pck.add_yaxis(f"{dev_name} 发送时的丢包数量",
                net_edev_txdrop[dev_name], 
                label_opts=opts.LabelOpts(is_show=False))
    line_pck.add_yaxis(f"{dev_name} 接收时的丢包数量",
                net_edev_rxdrop[dev_name], 
                label_opts=opts.LabelOpts(is_show=False))
    line_pck.add_yaxis(f"{dev_name} 发送时的载波错误数量",
                net_edev_txcarr[dev_name], 
                label_opts=opts.LabelOpts(is_show=False))
    line_pck.add_yaxis(f"{dev_name} 接收时的帧错误数量",
                net_edev_rxfram[dev_name], 
                label_opts=opts.LabelOpts(is_show=False))
    line_pck.add_yaxis(f"{dev_name} 接收时的 FIFO 缓冲区错误数量",
                net_edev_rxfifo[dev_name], 
                label_opts=opts.LabelOpts(is_show=False))
    line_pck.add_yaxis(f"{dev_name} 发送时的 FIFO 缓冲区错误数量",
                net_edev_txfifo[dev_name],
                label_opts=opts.LabelOpts(is_show=False))

    # 设置图表的标题和全局选项
    line_pck.set_global_opts(
        title_opts=opts.TitleOpts(title="{} 数据包".format(dev_name)
                      , title_textstyle_opts=opts.TextStyleOpts(font_size=25,)
                      ),
        # 设置数据缩放
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
        # 设置工具箱
    )
    line_kb = Line(init_opts=InitOpts(width="800px", height="400px"))
    line_kb.add_xaxis(timestamp_list)
    line_kb.add_yaxis(f"{dev_name} 发送千字节",
                   net_dev_txkB[dev_name], 
                   label_opts=opts.LabelOpts(is_show=False),
                   areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line_kb.add_yaxis(f"{dev_name} 接收千字节",
                    net_dev_rxkB[dev_name], 
                    label_opts=opts.LabelOpts(is_show=False),
                    areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    # 设置图表的标题和全局选项
    line_kb.set_global_opts(
        title_opts=opts.TitleOpts(title="{} 数据量".format(dev_name)
                      , title_textstyle_opts=opts.TextStyleOpts(font_size=25,)
                      ),
        # 设置数据缩放
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
        # 设置工具箱
    )
    line_cmp = Line(init_opts=InitOpts(width="800px", height="400px"))
    line_cmp.add_xaxis(timestamp_list)
    line_cmp.add_yaxis(f"{dev_name} 发送的压缩数据包数量",
                   net_dev_txcmp[dev_name], 
                   label_opts=opts.LabelOpts(is_show=False),
                   areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    line_cmp.add_yaxis(f"{dev_name} 接收的压缩数据包数量",
                    net_dev_rxcmp[dev_name], 
                    label_opts=opts.LabelOpts(is_show=False),
                    areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    # 设置图表的标题和全局选项
    line_cmp.set_global_opts(
        title_opts=opts.TitleOpts(title="{} 压缩数据包数量".format(dev_name)
                      , title_textstyle_opts=opts.TextStyleOpts(font_size=25,)
                      ),
        # 设置数据缩放
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )
    line_mcst = Line(init_opts=InitOpts(width="800px", height="400px"))
    line_mcst.add_xaxis(timestamp_list)
    line_mcst.add_yaxis(f"{dev_name} 接收的多播包数量",
                net_dev_rxmcst[dev_name], 
                label_opts=opts.LabelOpts(is_show=False))
    line_cmp.set_global_opts(
        title_opts=opts.TitleOpts(title="{} 接收的多播数据包数量".format(dev_name)
                      , title_textstyle_opts=opts.TextStyleOpts(font_size=25,)
                      ),
        # 设置数据缩放
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
    )
    # 将图表添加到页面
    page.add(line)
    page.add(line_pck)
    page.add(line_kb)
    page.add(line_cmp)
    page.add(line_mcst)
# 渲染页面，生成 HTML 文件，可以在浏览器中打开查看所有图表
page.render("network_dev.html")