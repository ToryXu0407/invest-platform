# 云服务器部署指南

**版本**: v1.0  
**日期**: 2026-02-28  
**目标**: 部署到用户自有云服务器

---

## 📋 系统要求

### 最低配置
- **CPU**: 2 核
- **内存**: 4GB
- **硬盘**: 20GB
- **系统**: Ubuntu 20.04+ / CentOS 7+

### 推荐配置
- **CPU**: 4 核
- **内存**: 8GB
- **硬盘**: 40GB SSD
- **带宽**: 5Mbps+

---

## 🚀 部署方案

### 方案一：Docker Compose（推荐）

**优点**:
- ✅ 一键部署
- ✅ 环境隔离
- ✅ 易于维护
- ✅ 便于扩展

**架构**:
```
┌─────────────────────────────────────┐
│         Nginx (反向代理)             │
│            Port 80/443              │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼──────┐
│   Next.js      │  │  FastAPI    │
│   :3000        │  │  :8000      │
└────────────────┘  └──────┬──────┘
                           │
                  ┌────────▼────────┐
                  │   PostgreSQL    │
                  │   :5432         │
                  └─────────────────┘
                           │
                  ┌────────▼────────┐
                  │     Redis       │
                  │   :6379         │
                  └─────────────────┘
```

### 方案二：手动部署

**适合**: 需要完全控制环境的场景

---

## 📦 Docker Compose 部署

### 1. 准备服务器

```bash
# SSH 登录服务器
ssh root@your-server-ip

# 更新系统
apt update && apt upgrade -y  # Ubuntu/Debian
# 或
yum update -y  # CentOS

# 安装 Docker
curl -fsSL https://get.docker.com | bash

# 安装 Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 2. 上传代码

**方式一：Git 克隆**
```bash
cd /opt
git clone https://github.com/ToryXu0407/invest-platform.git
cd invest-platform
```

**方式二：SCP 上传**
```bash
# 本地执行
scp -r /path/to/invest-platform root@your-server-ip:/opt/
```

### 3. 配置环境变量

```bash
cd /opt/invest-platform

# 复制环境配置示例
cp backend/.env.example backend/.env

# 编辑配置文件
vim backend/.env
```

**关键配置**:
```bash
# 环境
ENVIRONMENT=production

# 安全（务必修改！）
SECRET_KEY=your-production-secret-key-min-32-characters

# 数据库
DATABASE_URL=postgresql+asyncpg://postgres:your-password@postgres:5432/invest_platform

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1

# Tushare
TUSHARE_TOKEN=your-tushare-token

# CORS（添加你的域名）
ALLOWED_ORIGINS=["https://your-domain.com"]
```

### 4. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看服务状态
docker-compose ps
```

### 5. 配置 Nginx（可选）

如果使用 Docker，可以跳过这一步，使用应用内置的端口访问。

如果需要 Nginx 反向代理：

```nginx
# /etc/nginx/sites-available/invest-platform
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 后端 API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 启用配置
ln -s /etc/nginx/sites-available/invest-platform /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### 6. 配置 HTTPS（推荐）

```bash
# 安装 Certbot
apt install certbot python3-certbot-nginx -y

# 获取证书
certbot --nginx -d your-domain.com

# 自动续期
certbot renew --dry-run
```

---

## 🔧 手动部署

### 1. 安装依赖

```bash
# Python
apt install python3.11 python3.11-venv python3-pip -y

# Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install nodejs -y

# PostgreSQL
apt install postgresql postgresql-contrib -y

# Redis
apt install redis-server -y

# Nginx
apt install nginx -y
```

### 2. 配置数据库

```bash
# 启动 PostgreSQL
systemctl start postgresql
systemctl enable postgresql

# 创建数据库
sudo -u postgres psql
CREATE DATABASE invest_platform;
CREATE USER invest_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE invest_platform TO invest_user;
\q
```

### 3. 部署后端

```bash
cd /opt/invest-platform/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
vim .env  # 编辑配置

# 数据库迁移
alembic upgrade head

# 启动服务（生产环境）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Systemd 服务配置**:
```ini
# /etc/systemd/system/invest-api.service
[Unit]
Description=Invest Platform API
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/invest-platform/backend
Environment="PATH=/opt/invest-platform/backend/venv/bin"
ExecStart=/opt/invest-platform/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
systemctl daemon-reload
systemctl enable invest-api
systemctl start invest-api
systemctl status invest-api
```

### 4. 部署前端

```bash
cd /opt/invest-platform/apps/web

# 安装依赖
npm install

# 构建
npm run build

# 启动（生产环境）
npm run start
```

**PM2 管理**:
```bash
# 安装 PM2
npm install -g pm2

# 启动应用
pm2 start npm --name "invest-web" -- run start

# 开机自启
pm2 startup
pm2 save
```

### 5. 配置 Nginx

```nginx
# /etc/nginx/sites-available/invest-platform
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /opt/invest-platform/apps/web/out;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 📊 性能优化

### 1. 数据库优化

```sql
-- 添加索引
CREATE INDEX idx_stock_code ON stocks(code);
CREATE INDEX idx_stock_date ON stock_daily_data(date);
CREATE INDEX idx_user_email ON users(email);

-- 定期清理
VACUUM ANALYZE;
```

### 2. Redis 缓存

```python
# 缓存热点数据
@cache.cached(timeout=300)
async def get_stock_indicators(code: str):
    # ...
```

### 3. Gzip 压缩

```nginx
# Nginx 配置
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;
```

### 4. 静态资源 CDN

将前端静态资源上传到 CDN，加速访问。

---

## 🔒 安全配置

### 1. 防火墙

```bash
# UFW 配置（Ubuntu）
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### 2. SSH 安全

```bash
# 禁用密码登录
vim /etc/ssh/sshd_config
PasswordAuthentication no
PermitRootLogin prohibit-password

# 重启 SSH
systemctl restart sshd
```

### 3. 数据库安全

```bash
# 只允许本地访问
vim /etc/postgresql/15/main/postgresql.conf
listen_addresses = 'localhost'
```

### 4. 定期备份

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U invest_user invest_platform > /backups/db_$DATE.sql
docker cp postgres:/var/lib/postgresql/data /backups/data_$DATE
# 保留最近 7 天备份
find /backups -mtime +7 -delete
```

**Cron 定时任务**:
```bash
# 每天凌晨 2 点备份
0 2 * * * /opt/invest-platform/scripts/backup.sh
```

---

## 📈 监控告警

### 1. 应用监控

```bash
# 安装 Sentry SDK
pip install sentry-sdk[fastapi]
```

**配置**:
```python
# backend/.env
SENTRY_DSN=https://your-sentry-dsn
```

### 2. 系统监控

```bash
# 安装 Prometheus Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
tar xvfz node_exporter-*.tar.gz
sudo mv node_exporter-*/node_exporter /usr/local/bin/

# 创建 systemd 服务
# ...（参考官方文档）
```

### 3. 日志管理

```bash
# 查看日志
docker-compose logs -f api
docker-compose logs -f web

# 日志轮转
# /etc/logrotate.d/invest-platform
/var/log/invest-platform/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
}
```

---

## ✅ 部署检查清单

- [ ] 服务器系统更新
- [ ] Docker 安装
- [ ] 代码上传
- [ ] 环境变量配置
- [ ] 数据库初始化
- [ ] 服务启动
- [ ] HTTPS 配置
- [ ] 防火墙配置
- [ ] 备份脚本
- [ ] 监控配置
- [ ] 访问测试

---

## 🆘 故障排查

### 常见问题

**1. 服务无法启动**
```bash
# 查看日志
docker-compose logs api
docker-compose logs web

# 检查端口占用
netstat -tlnp | grep :8000
netstat -tlnp | grep :3000
```

**2. 数据库连接失败**
```bash
# 检查 PostgreSQL 状态
docker-compose ps postgres

# 查看数据库日志
docker-compose logs postgres

# 测试连接
docker-compose exec postgres psql -U postgres -d invest_platform
```

**3. 内存不足**
```bash
# 查看内存使用
free -h
docker stats

# 增加 Swap
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

---

## 📞 技术支持

**文档**: https://github.com/ToryXu0407/invest-platform  
**Issues**: https://github.com/ToryXu0407/invest-platform/issues

---

**最后更新**: 2026-02-28
