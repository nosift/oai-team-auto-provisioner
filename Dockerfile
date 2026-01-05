# 多阶段构建 Dockerfile for ChatGPT Team Redemption System
# 优化版本 - 适用于 Zeabur/爪云 等轻量级平台

FROM python:3.12-slim as base

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖 (一次性安装,减少层数)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

# 生产阶段
FROM python:3.12-slim

WORKDIR /app

# 复制Python依赖
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    LOG_LEVEL=INFO \
    GUNICORN_WORKERS=2 \
    GUNICORN_TIMEOUT=120

# 创建非root用户和数据目录
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

# 复制应用代码
COPY --chown=appuser:appuser . .

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 5000

# 健康检查 (优化为不依赖requests库)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health', timeout=5)" || exit 1

# 启动命令 (使用环境变量控制workers数量,适应不同平台)
CMD gunicorn --workers ${GUNICORN_WORKERS} --bind 0.0.0.0:5000 --timeout ${GUNICORN_TIMEOUT} --access-logfile - --error-logfile - web_server:app
