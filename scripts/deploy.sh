#!/bin/bash
# 快速部署脚本

set -e

echo "🚀 开始部署价值投资分析平台..."

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 创建 .env 文件
if [ ! -f .env ]; then
    echo "📝 创建环境配置文件..."
    cp .env.example .env
    
    # 生成随机密钥
    SECRET_KEY=$(openssl rand -hex 32)
    POSTGRES_PASSWORD=$(openssl rand -hex 16)
    
    # 更新 .env 文件
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$POSTGRES_PASSWORD/" .env
    
    echo "✅ 环境配置已生成，请编辑 .env 文件配置 TUSHARE_TOKEN 和 DOMAIN"
fi

# 拉取最新代码
echo "📦 拉取最新代码..."
git pull origin main

# 构建并启动
echo "🔨 构建服务..."
docker-compose -f docker-compose.prod.yml build

echo "🚀 启动服务..."
docker-compose -f docker-compose.prod.yml up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose -f docker-compose.prod.yml ps

# 查看日志
echo "📋 查看日志（按 Ctrl+C 退出）..."
docker-compose -f docker-compose.prod.yml logs -f
