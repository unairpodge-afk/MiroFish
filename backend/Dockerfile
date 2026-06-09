# 使用轻量级 Python 3.11 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /home/user/app

# 安装必要的系统依赖（例如编译SQLite或其他可能需要的库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 设置 Hugging Face Spaces 要求的非 root 用户
# Hugging Face 默认使用 ID 为 1000 的 user 运行
RUN useradd -m -u 1000 user || true
RUN chown -R 1000:1000 /home/user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# 复制 requirements 文件并安装
COPY --chown=user requirements.txt /home/user/app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /home/user/app/requirements.txt

# 将所有代码复制到容器中
COPY --chown=user . /home/user/app

# Hugging Face Spaces 默认暴露 7860 端口
EXPOSE 7860

# 启动命令：使用 Gunicorn 运行，绑定到 7860 端口
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "8", "--timeout", "0", "run:app"]
