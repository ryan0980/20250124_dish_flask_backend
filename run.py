# 创建应用实例
import sys

from wxcloudrun import app

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
