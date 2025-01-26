from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import base64
import time


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """
    try:
        # 获取请求体参数
        params = request.get_json()

        # 检查action参数
        if 'action' not in params:
            return make_err_response('缺少action参数')

        # 如果数据库未初始化，返回模拟数据
        if 'db' not in globals() or db is None:
            return make_succ_response(0)

        # 按照不同的action的值，进行不同的操作
        action = params['action']

        # 执行自增操作
        if action == 'inc':
            counter = query_counterbyid(1)
            if counter is None:
                counter = Counters()
                counter.id = 1
                counter.count = 1
                counter.created_at = datetime.now()
                counter.updated_at = datetime.now()
                insert_counter(counter)
            else:
                counter.id = 1
                counter.count += 1
                counter.updated_at = datetime.now()
                update_counterbyid(counter)
            return make_succ_response(counter.count)

        # 执行清0操作
        elif action == 'clear':
            delete_counterbyid(1)
            return make_succ_empty_response()

        # action参数错误
        else:
            return make_err_response('action参数错误')

    except Exception as e:
        return make_err_response(str(e))


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route('/health')
def health_check():
    """
    健康检查接口
    """
    return make_succ_response('ok')


@app.route('/api/upload_base64', methods=['POST'])
def upload_base64():
    """
    处理base64图片上传的接口
    :return: 返回处理结果
    """
    try:
        # 获取请求体参数
        params = request.get_json()
        
        if 'image' not in params:
            return make_err_response('缺少image参数')
            
        # 获取base64图片数据
        image_base64 = params['image']
        
        # 获取当前时间，格式化为指定格式
        current_time = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
        
        return make_succ_response({
            'message': f'收到图片 - {current_time}'
        })
        
    except Exception as e:
        return make_err_response(str(e))


@app.route('/api/analyze_menu', methods=['POST'])
def analyze_menu():
    """
    分析菜单图片并返回结构化数据
    :return: 返回分析结果
    """
    try:
        # 获取请求体参数
        params = request.get_json()
        
        if 'image' not in params:
            return make_err_response('缺少image参数')
            
        # 获取base64图片数据
        image_base64 = params['image']
        
        # 获取当前时间，用于记录处理时间
        start_time = time.time()
        
        # TODO: 这里后续添加您的菜单分析逻辑
        # 示例返回数据结构
        menu_analysis = {
            "categories": {
                "1": [  # Cold Dish
                    ["凉拌黄瓜", "新鲜爽口的黄瓜", "12", "8", "清爽可口"],
                ],
                "2": [  # Hot Dish
                    ["宫保鸡丁", "传统川菜", "38", "9", "经典美味"],
                ],
                "4": [],  # Staple Food
                "5": [],  # Dessert
                "6": [],  # Tea/Drink
                "0": []   # Unknown
            },
            "processing_time": f"{time.time() - start_time:.2f}",
            "timestamp": datetime.now().strftime('%d/%b/%Y %H:%M:%S')
        }
        
        return make_succ_response(menu_analysis)
        
    except Exception as e:
        return make_err_response(str(e))
