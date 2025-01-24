import os

# 是否开启debug模式
DEBUG = True

# 数据库配置
MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME", 'root')
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", 'root')
MYSQL_ADDRESS = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')
