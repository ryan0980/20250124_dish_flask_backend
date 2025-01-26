from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import config
import logging

# 因MySQLDB不支持Python3，使用pymysql扩展库代替MySQLDB库
pymysql.install_as_MySQLdb()

# 初始化 Flask app
app = Flask(__name__, instance_relative_config=True)

# 设置日志
logging.basicConfig(level=logging.INFO)

try:
    # 从 config.py 中读取配置
    app.config.from_object('config')
    
    # 初始化数据库
    db = SQLAlchemy(app)
    
    # 初始化所有的控制器
    from wxcloudrun import views, model
    
    # 初始化数据库表
    with app.app_context():
        db.create_all()
        
except Exception as e:
    logging.error(f"初始化失败: {str(e)}")
    # 继续运行，但不使用数据库功能
    db = None
