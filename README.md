# 微信云托管 Flask 后端

这是一个基于 Flask 框架的微信小程序后端项目。

## 项目结构

# wxcloudrun-flask

[![GitHub license](https://img.shields.io/github/license/WeixinCloud/wxcloudrun-express)](https://github.com/WeixinCloud/wxcloudrun-express)
![GitHub package.json dependency version (prod)](https://img.shields.io/badge/python-3.7.3-green)

微信云托管 python Flask 框架模版，实现简单的计数器读写接口，使用云托管 MySQL 读写、记录计数值。

![](https://qcloudimg.tencent-cloud.cn/raw/be22992d297d1b9a1a5365e606276781.png)

## 快速开始

前往 [微信云托管快速开始页面](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/basic/guide.html)，选择相应语言的模板，根据引导完成部署。

## 本地调试

下载代码在本地调试，请参考[微信云托管本地调试指南](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/guide/debug/)

## 实时开发

代码变动时，不需要重新构建和启动容器，即可查看变动后的效果。请参考[微信云托管实时开发指南](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/guide/debug/dev.html)

## Dockerfile 最佳实践

请参考[如何提高项目构建效率](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/scene/build/speed.html)

## 目录结构说明

```
.
├── Dockerfile dockerfile       dockerfile
├── README.md                  README.md文件
├── container.config.json      模板部署「服务设置」初始化配置
├── requirements.txt           依赖包文件
├── config.py                  项目的总配置文件
├── run.py                     flask项目管理文件
└── wxcloudrun                 app目录
    ├── __init__.py            python项目必带
    ├── dao.py                 数据库访问模块
    ├── model.py               数据库对应的模型
    ├── response.py            响应结构构造
    ├── templates              模版目录
    └── views.py               业务逻辑处理模块
```

## 使用注意

需要在「服务设置」中配置以下环境变量:

- MYSQL_ADDRESS
- MYSQL_PASSWORD
- MYSQL_USERNAME

## License

[MIT](./LICENSE)
