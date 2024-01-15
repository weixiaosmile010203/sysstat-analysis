import json
import os

data = json.load(open(os.path.join(os.path.dirname(__file__), 'sa01.json')))

# hostname = data['sysstat']['hosts'][0]['nodename']
# sysname = data['sysstat']['hosts'][0]['sysname']
# release = data['sysstat']['hosts'][0]['release']
# machine = data['sysstat']['hosts'][0]['machine']
# cpu_cores = data['sysstat']['hosts'][0]['number-of-cpus']
# file_date = data['sysstat']['hosts'][0]['file-date']
# file_utc_time = data['sysstat']['hosts'][0]['file-utc-time']


# 获取时间戳列表
timestamps = []
cpus = []
processes = []
swaps = []
pages = []
ios = []
memorys = []
hugepages = []
kernels = []
queues = []
serials = []
disks = []
networks = []
# 遍历数据结构
for host in data['sysstat']['hosts']:
    for statistic in host['statistics']:
        timestamps.append(statistic['timestamp'])
        # 获取 CPU 列表
        for cpu in statistic['cpu-load']:
            cpus.append(cpu)
        # 获取进程上下文切换列表
        processes.append(statistic['process-and-context-switch'])
        # 获取swap列表
        swaps.append(statistic['swap-pages'])
        # 获取系统分页列表
        pages.append(statistic['paging'])
        # 获取io列表
        ios.append(statistic['io'])
        # 获取memory列表
        memorys.append(statistic['memory'])
        # 获取hugepages列表
        hugepages.append(statistic['hugepages'])
        # 获取kernel列表
        kernels.append(statistic['kernel'])
        # 获取queue列表
        queues.append(statistic['queue'])
        # 获取serial列表
        serials.append(statistic['serial'])
        # 获取disk列表
        disks.append(statistic['disk'])
        # 获取network列表
        networks.append(statistic['network'])
# for cpu in cpus:
#     print(cpu)

for net in networks:
    print(net['net-dev'])