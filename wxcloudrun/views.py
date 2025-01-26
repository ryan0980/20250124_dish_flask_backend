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
        print("\n=== API Request Debug Info ===")
        print(f"Image base64 prefix: {image_base64[:50]}...")
        
        # 记录开始时间
        start_time = time.time()
        
        # 初始化Together客户端
        client = Together(
            api_key="43a055c9202a487b90992dbc228455059cc9b36ad010dce5372f7b30a04ee0c6"
        )
        
        # 设置提示语
        system_prompt = """
        You are given an image of a menu. Your job is to extract all the menu items and present them in the following format:

        Name | Description | Price

        Formatting guidelines:
        1. Each menu item must be presented on a separate line.
        2. Do not include empty lines between items.
        3. Use the separator " | " (pipe with spaces) to separate name, description, and price.
        4. If a description or price is missing, replace it with the word "null".
        5. Ensure the description and price are on the same line as the dish name.
        6. Do not add any extra text, explanations, or formatting.
        """
        
        print("\n=== API Call Info ===")
        print(f"Model: meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo")
        print(f"Max tokens: 4096")
        
        # 调用API
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": system_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ],
                }
            ],
            max_tokens=4096
        )
        
        # 处理API返回的结果
        menu_text = response.choices[0].message.content.strip()
        
        print("\n=== API Response ===")
        print(f"Raw response: {response}")
        print(f"\nExtracted menu text:\n{menu_text}")
        print(f"\nProcessing time: {time.time() - start_time:.2f} seconds")
        
        # 构建返回数据
        menu_analysis = {
            "text": menu_text,  # 原始文本
            "processing_time": f"{time.time() - start_time:.2f}",
            "timestamp": datetime.now().strftime('%d/%b/%Y %H:%M:%S')
        }
        
        return make_succ_response(menu_analysis)
        
    except Exception as e:
        error_message = str(e)
        print(f"\n=== Error Details ===")
        print(f"Error type: {type(e)}")
        print(f"Error message: {error_message}")
        print(f"Stack trace:", exc_info=True)
        return make_err_response({
            "error": f"菜单分析失败: {error_message}",
            "timestamp": datetime.now().strftime('%d/%b/%Y %H:%M:%S')
        })


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
