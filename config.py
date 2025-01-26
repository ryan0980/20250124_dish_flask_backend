import os

# 是否开启debug模式
DEBUG = True

# 禁用重载器
USE_RELOADER = False

# 本地测试用的配置
if DEBUG:
    username = 'root'
    password = 'root'
    db_address = '127.0.0.1:3306'
    
# 数据库配置
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{db_address}/python_demo'

# 如果数据库连接失败，使用SQLite
try:
    import pymysql
    pymysql.connect(host='127.0.0.1', port=3306, user=username, password=password)
except:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# 不追踪对象的修改
SQLALCHEMY_TRACK_MODIFICATIONS = False
