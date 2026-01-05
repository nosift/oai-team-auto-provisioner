#!/bin/bash
# Docker 启动脚本

set -e

echo "🚀 启动 ChatGPT Team 兑换码系统..."

# 检查配置文件
if [ ! -f "config.toml" ]; then
    echo "❌ 错误: 未找到 config.toml"
    echo "请复制 config.toml.example 并配置"
    exit 1
fi

if [ ! -f "team.json" ]; then
    echo "❌ 错误: 未找到 team.json"
    echo "请创建 team.json 并配置Team凭证"
    exit 1
fi

# 创建数据目录
mkdir -p data

# 复制环境变量文件
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ 已创建 .env 文件"
    fi
fi

# 启动服务
echo "🐳 启动Docker容器..."
docker-compose up -d

echo ""
echo "✅ 服务已启动!"
echo ""
echo "📝 访问地址:"
echo "   用户兑换页面: http://localhost:5000/"
echo "   管理后台: http://localhost:5000/admin"
echo ""
echo "📊 查看日志:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 停止服务:"
echo "   docker-compose down"
