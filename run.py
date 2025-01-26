# 创建应用实例
import sys
from wxcloudrun import app

# 启动Flask Web服务
if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # 使用 werkzeug 直接启动
        from werkzeug.serving import run_simple
        run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=False)
    except Exception as e:
        print(f"启动失败: {str(e)}")
