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


@app.route('/')
def home():
    data = import_data()
    timestamp_list = data._get_timestamp_list()
    p_data = data._get_pcsw_data()['proc']
    c_data = data._get_pcsw_data()['cswch']
    return render_template('index.html', timestamp_list=timestamp_list, p_data=p_data, c_data=c_data)

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
