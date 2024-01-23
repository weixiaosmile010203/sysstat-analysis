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
    line_data = SysStatAnalyzer(os.path.join(os.path.dirname(__file__), 'sa01.json'))
    timestamp_list = line_data._get_timestamp_list()
    p_data = line_data._get_pcsw_data()['proc']
    c_data = line_data._get_pcsw_data()['cswch']
    return render_template('cpu.html', timestamp_list=timestamp_list, p_data=p_data, c_data=c_data)

@app.route('/mem_page')
def mem_page():
    line_data = SysStatAnalyzer(os.path.join(os.path.dirname(__file__), 'sa01.json'))
    timestamp_list = line_data._get_timestamp_list()
    p_data = line_data._get_pcsw_data()['proc']
    c_data = line_data._get_pcsw_data()['cswch']
    return render_template('memory.html', timestamp_list=timestamp_list, p_data=p_data, c_data=c_data)


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
