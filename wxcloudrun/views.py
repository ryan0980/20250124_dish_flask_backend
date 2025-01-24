from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.response import make_succ_response, make_err_response

@app.route('/')
def index():
    """
    首页
    """
    return render_template('index.html')

@app.route('/api/date', methods=['GET'])
def get_date():
    """
    获取当前日期
    :return: 当前日期，格式 YYYY-MM-DD
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    return make_succ_response({
        'date': current_date
    })
