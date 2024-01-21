from flask import Flask
from flask import request, render_template
from pyecharts import options as opts
from pyecharts.charts import Line, Page
from test import SysStatAnalyzer
import json, os

app = Flask(__name__)


def line_base():
    line_data = SysStatAnalyzer(os.path.join(os.path.dirname(__file__), 'sa01.json'))
    pcsw_char = (
        Line()
        .add_xaxis(line_data._get_timestamp_list())
        .add_yaxis("进程创建数", line_data._get_pcsw_data()['proc'])
        .add_yaxis("上下文切换数", line_data._get_pcsw_data()['cswch'])
        .set_global_opts(title_opts=opts.TitleOpts(title="进程和上下文切换次数", subtitle="单位：次"),
                         datazoom_opts=opts.DataZoomOpts(),)
    )
    return pcsw_char


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/pcsw_char')
def get_pcsw_char():
    c = line_base()
    return c.dump_options_with_quotes()

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
