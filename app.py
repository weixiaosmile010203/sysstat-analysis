from flask import Flask
from flask import url_for
from flask import request, render_template
from pyecharts import options as opts
from pyecharts.charts import Line, Page
from test import SysStatAnalyzer
import json, os

app = Flask(__name__)



def import_data():
    data = SysStatAnalyzer(os.path.join(os.path.dirname(__file__), 'sa01.json'))
    return data




@app.route('/cpu_page')
def cpu_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    cpu_data = data._get_cpu_data()
    print(cpu_data)
    return render_template('cpu.html', timestamp_list=timestamp_list, cpu_data=cpu_data)

@app.route('/mem_page')
def mem_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    mem_data = data._get_memory_data()
    return render_template('memory.html', timestamp_list=timestamp_list, mem_data=mem_data)

@app.route('/network_page')
def network_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    network_data = data._get_network_dev_data()
    return render_template('network.html', timestamp_list=timestamp_list, network_data=network_data)

@app.route('/nfs_page')
def nfs_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    nfs_data = data._get_network_nfs_data()
    return render_template('network-nfs.html', timestamp_list=timestamp_list, nfs_data=nfs_data)

@app.route('/nfsd_page')
def nfsd_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    nfsd_data = data._get_network_nfsd_data()
    return render_template('network-nfsd.html', timestamp_list=timestamp_list, nfsd_data=nfsd_data)

@app.route('/socket_page')
def socket_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    socket_data = data._get_network_sock_data()
    return render_template('network-sock.html', timestamp_list=timestamp_list, socket_data=socket_data)

@app.route('/softnet_page')
def softnet_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    softnet_data = data._get_network_softnet_data()
    return render_template('network-softnet.html', timestamp_list=timestamp_list, softnet_data=softnet_data)

@app.route('/disk_page')
def disk_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    disk_data = data._get_disk_data()
    return render_template('disks.html', timestamp_list=timestamp_list, disk_data=disk_data)

@app.route('/pcsw_page')
def home():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    pcsw_data = data._get_pcsw_data()
    return render_template('pcsw.html', timestamp_list=timestamp_list, pcsw_data=pcsw_data)

@app.route('/swap_page')
def swap_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    swap_data = data._get_swap_data()
    return render_template('swap_page.html', timestamp_list=timestamp_list, swap_data=swap_data)

@app.route('/paging_page')
def paging_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    paging_data = data._get_page_data()
    return render_template('paging.html', timestamp_list=timestamp_list, paging_data=paging_data)

@app.route('/io_page')
def io_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    io_data = data._get_io_data()
    return render_template('io.html', timestamp_list=timestamp_list, io_data=io_data)

@app.route('/huge_page')
def huge_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    huge_data = data._get_hugepage_data()
    return render_template('hugepage.html', timestamp_list=timestamp_list, huge_data=huge_data)

@app.route('/kernel_page')
def kernel_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    kernel_data = data._get_kernel_table_data()
    return render_template('kernel.html', timestamp_list=timestamp_list, kernel_data=kernel_data)

@app.route('/queue_page')
def queue_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    queue_data = data._get_queue_data()
    return render_template('queue.html', timestamp_list=timestamp_list, queue_data=queue_data)

@app.route('/serial_page')
def serial_page():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    serial_data = data._get_serial_data()
    return render_template('serial.html', timestamp_list=timestamp_list, serial_data=serial_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        file.save(file.filename)
        return 'File uploaded successfully'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
