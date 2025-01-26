from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import base64
import time
from together import Together


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


# 添加测试接口
@app.route('/api/test_together', methods=['GET'])
def test_together():
    """
    测试Together API连接的接口
    :return: 返回API调用结果
    """
    try:
        start_time = time.time()
        
        client = Together(
            api_key="43a055c9202a487b90992dbc228455059cc9b36ad010dce5372f7b30a04ee0c6"
        )
        
        # 扩展测试提示语，测试更多功能
        system_prompt = """
        你是一个中餐菜单分析助手。
        请按以下格式分析菜品：
        1. 菜品类型
        2. 价格合理性
        3. 推荐指数
        """
        
        test_prompt = "请分析这道菜：宫保鸡丁 38元"
        
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": test_prompt}
            ],
            max_tokens=1024,
            temperature=0.7  # 添加温度参数控制输出的创造性
        )
        
        # 扩展返回信息
        return make_succ_response({
            "message": response.choices[0].message.content,
            "processing_time": f"{time.time() - start_time:.2f}",
            "timestamp": datetime.now().strftime('%d/%b/%Y %H:%M:%S'),
            "model": "Meta-Llama-3.1-8B-Instruct-Turbo",
            "status": "连接成功",
            "tokens": len(response.choices[0].message.content.split())  # 估算token数
        })
        
    except Exception as e:
        error_message = str(e)
        return make_err_response({
            "error": f"API调用失败: {error_message}",
            "timestamp": datetime.now().strftime('%d/%b/%Y %H:%M:%S')
        })
