import pyecharts.options as opts
from pyecharts.charts import Line, Page
import json
import os

class SysStatAnalyzer:
    def __init__(self, json_file_path):
        self.data = json.load(open(json_file_path))
        self.page = Page()

    def _get_timestamp_list(self):
        timestamps = []
        for host in self.data['sysstat']['hosts']:
            for statistic in host['statistics']:
                timestamps.append(statistic['timestamp'])
        return [timestamp.get('date') + ' ' + timestamp.get('time') for timestamp in timestamps]

    def _raw_data(self, key):
        data = []
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            data.append(statistic[key])
        return data

    def _get_cpu_data(self):
        cpu_data = {}
        cpu_stats = ['usr', 'nice', 'sys', 'iowait', 'steal', 'irq', 'soft', 'guest', 'gnice', 'idle']
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            for cpu in statistic['cpu-load']:
                for stat in cpu_stats:
                    cpu_data.setdefault(cpu['cpu'], {}).setdefault(stat, []).append(cpu[stat])
        return cpu_data

    def _get_memory_data(self):
        mem_data = {}
        mem_stats = ["memfree", "avail", "memused", "memused-percent", "buffers", "cached", "commit", "commit-percent", "active", "inactive", "dirty", "anonpg", "slab", "kstack", "pgtbl", "vmused", "swpfree", "swpused", "swpused-percent", "swpcad", "swpcad-percent"]
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            memory = statistic['memory']
            for stat in mem_stats:
                mem_data.setdefault(stat, []).append(memory[stat])
        return mem_data
    
    def _get_network_dev_data(self):
        network_data = {}
        network_stats = ["rxpck", "txpck", "rxkB", "txkB", "rxcmp", "txcmp", "rxmcst"]
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            for net in statistic['network']['net-dev']:
                iface = net['iface']
                network_data.setdefault(iface, {})
                for stat in network_stats:
                    network_data[iface].setdefault(stat, []).append(net[stat])
        network_stats = ['rxerr','txerr','coll','rxdrop','txdrop','txcarr','rxfram','rxfifo','txfifo']
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            for net in statistic['network']['net-edev']:
                iface = net['iface']
                network_data.setdefault(iface, {})
                for stat in network_stats:
                    network_data[iface].setdefault(stat, []).append(net[stat])
        return network_data
    
    def _get_network_nfs_data(self):
        network_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            nfs = statistic['network']['net-nfs']
            for i in nfs:
                network_data.setdefault(i, []).append(nfs[i])
        return network_data

    def _get_network_nfsd_data(self):
        network_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            nfsd = statistic['network']['net-nfsd']
            for i in nfsd:
                network_data.setdefault(i, []).append(nfsd[i])
        return network_data
    
    def _get_network_sock_data(self):
        network_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            sock = statistic['network']['net-sock']
            for i in sock:
                network_data.setdefault(i, []).append(sock[i])
        return network_data
    
    def _get_network_softnet_data(self):
        network_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            softnet = statistic['network']['softnet']
            for cpus in softnet:
                for i in cpus:
                    if i == 'cpu':
                        continue
                    network_data.setdefault(cpus['cpu'], {}).setdefault(i, []).append(cpus[i])
        return network_data
    
    def _get_disk_data(self):
        disk_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            disks = statistic['disk']
            for disk in disks:
                for i in disk:
                    if i == 'disk-device':
                        continue
                    disk_data.setdefault(disk['disk-device'], {}).setdefault(i, []).append(disk[i])
        return disk_data

    def _get_pcsw_data(self):
        pcsw_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            pcsw = statistic['process-and-context-switch']
            for i in pcsw:
                pcsw_data.setdefault(i, []).append(pcsw[i])
        return pcsw_data
    
    def _get_swap_data(self):
        swap_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            swap = statistic['swap-pages']
            for i in swap:
                swap_data.setdefault(i, []).append(swap[i])
        return swap_data
    
    def _get_page_data(self):
        page_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            page = statistic['paging']
            for i in page:
                page_data.setdefault(i, []).append(page[i])
        return page_data
    
    def _get_io_data(self):
        io_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            io = statistic['io']
            for i in io:
                io_data.setdefault(i, []).append(io[i])
        return io_data
    
    def _get_hugepage_data(self):
        hugepage_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            hugepage = statistic['hugepages']
            for i in hugepage:
                hugepage_data.setdefault(i, []).append(hugepage[i])
        return hugepage_data
    
    def _get_kernel_table_data(self):
        kernel_table_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            kernel_table = statistic['kernel']
            for i in kernel_table:
                kernel_table_data.setdefault(i, []).append(kernel_table[i])
        return kernel_table_data

    def _get_queue_data(self):
        queue_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            queue = statistic['queue']
            for i in queue:
                queue_data.setdefault(i, []).append(queue[i])
        return queue_data
    
    def _get_serial_data(self):
        serial_data = {}
        for statistic in self.data['sysstat']['hosts'][0]['statistics']:
            serials = statistic['serial']
            for serial in serials:
                for line in serial:
                    if line == 'line':
                        continue
                    serial_data.setdefault(serial['line'], {}).setdefault(line, []).append(serial[line])
        return serial_data
    
    def _create_cpu_chart(self, cpu_data, timestamp_list):
        cores = list(cpu_data.keys())
        for core in cores:
            line = Line()
            line.add_xaxis(timestamp_list)
            line.add_yaxis(f"{core}_usr", cpu_data[core], label_opts=opts.LabelOpts(is_show=False),
                           areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
            # 其他设置...
            self.page.add(line)

    def analyze_cpu(self):
        timestamp_list = self._get_timestamp_list()
        cpu_data = self._get_cpu_data()
        self._create_cpu_chart(cpu_data, timestamp_list)

    def render_page(self, output_file="output.html"):
        self.page.render(output_file)

# 使用示例
analyzer = SysStatAnalyzer(os.path.join(os.path.dirname(__file__), 'sa01.json'))
analyzer._get_cpu_data()
analyzer._get_memory_data()
analyzer._get_network_dev_data()
analyzer._get_network_nfs_data()
analyzer._get_network_nfsd_data()
analyzer._get_network_sock_data()
analyzer._get_network_softnet_data()
analyzer._get_disk_data()
analyzer._get_pcsw_data()
analyzer._get_swap_data()
analyzer._get_page_data()
analyzer._get_io_data()
analyzer._get_hugepage_data()
analyzer._get_kernel_table_data()
analyzer._get_queue_data()
analyzer._get_serial_data()
