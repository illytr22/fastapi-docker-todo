# 1. 基础镜像：使用官方的轻量级 Python 3.9 环境
FROM python:3.9-slim

# 2. 设定工作目录：容器内的操作都在 /code 目录下进行
WORKDIR /code

# 3. 复制依赖清单：先只复制 requirements.txt（利用 Docker 缓存机制）
COPY ./requirements.txt /code/requirements.txt

# 4. 安装依赖：使用清华镜像源加速下载
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 复制代码：把你本地的 app 文件夹，完整复制到容器的 /code/app 目录里
COPY ./app /code/app

# 6. 暴露端口：声明这个容器内部会使用 8000 端口
EXPOSE 8000

# 7. 启动命令：当容器跑起来时，执行 uvicorn 启动服务器
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]