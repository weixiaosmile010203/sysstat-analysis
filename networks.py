import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json, os

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

for nets in networks:
    for net in nets['net-dev']:
        net_dev_rxkB[net['iface']] =  net_dev_rxkB.get(net['iface'], []) + [net['rxkB']]
        net_dev_txkB[net['iface']] =  net_dev_txkB.get(net['iface'], []) + [net['txkB']]
        net_dev_rxpck[net['iface']] =  net_dev_rxpck.get(net['iface'], []) + [net['rxpck']]
        net_dev_txpck[net['iface']] =  net_dev_txpck.get(net['iface'], []) + [net['txpck']]
        net_dev_rxcmp[net['iface']] =  net_dev_rxcmp.get(net['iface'], []) + [net['rxcmp']]
        net_dev_txcmp[net['iface']] =  net_dev_txcmp.get(net['iface'], []) + [net['txcmp']]
        net_dev_rxmcst[net['iface']] =  net_dev_rxmcst.get(net['iface'], []) + [net['rxmcst']]
        net_dev_percent[net['iface']] =  net_dev_percent.get(net['iface'], []) + [net['ifutil-percent']]


page = Page(layout=Page.SimplePageLayout)
# 获取网卡的名称，进行遍历  
for iface in nets['net-dev']:
    dev_name = iface['iface']
    line = Line()
    line.add_xaxis(timestamp_list)
    line.add_yaxis(f"{dev_name}_percent",
                   net_dev_percent[dev_name], 
                   label_opts=opts.LabelOpts(is_show=False),
                   areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    # 设置图表的标题和全局选项
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="{} ifutil-percent".format(dev_name)
                      , title_textstyle_opts=opts.TextStyleOpts(font_size=25)
                      ),
        # 设置数据缩放
        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100, type_="slider",)],
        # 设置工具箱
    )
    # 将图表添加到页面
    page.add(line)
# 渲染页面，生成 HTML 文件，可以在浏览器中打开查看所有图表
page.render("network_dev.html")