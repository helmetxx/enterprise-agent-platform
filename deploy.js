/**
 * 企业智能助手平台 - Ubuntu 部署指南
 * 
 * 本文档提供在 Ubuntu 系统上部署企业智能助手平台的完整步骤，
 * 包括 frontend、backend、MySQL 和 Redis 四个组件的配置和启动。
 */

/**
 * 1. 系统准备
 * 
 * 首先，确保您的 Ubuntu 系统是最新的：
 */

// 更新系统包
// sudo apt update
// sudo apt upgrade -y

// 安装必要的工具
// sudo apt install -y curl git build-essential

/**
 * 2. 安装 Docker 和 Docker Compose
 * 
 * Docker 和 Docker Compose 是最简单的部署方式，可以确保各组件之间的隔离和一致性：
 */

// 安装 Docker
// sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
// curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
// sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
// sudo apt update
// sudo apt install -y docker-ce

// 启动 Docker 并设置开机自启
// sudo systemctl start docker
// sudo systemctl enable docker

// 将当前用户添加到 docker 组，避免每次使用 docker 命令都需要 sudo
// sudo usermod -aG docker $USER

// 安装 Docker Compose
// sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
// sudo chmod +x /usr/local/bin/docker-compose

// 注销并重新登录，使 docker 组权限生效

/**
 * 3. 克隆项目代码
 */

// git clone <您的项目仓库URL> enterprise-agent-platform
// cd enterprise-agent-platform

/**
 * 4. 配置环境变量
 */

// 创建 .env 文件
// cp .env.example .env

// 编辑环境变量
// nano .env

// 确保设置了正确的数据库连接信息和 JWT 密钥

/**
 * 5. 使用 Docker Compose 部署
 * 
 * 您的项目已经包含了 docker-compose.yml 文件，我们可以直接使用它来部署所有服务：
 */

// 构建并启动所有服务
// docker-compose up -d

// 这个命令会启动以下服务：
// - Frontend (Vue.js 应用)
// - Backend (FastAPI 应用)
// - MySQL 数据库
// - Redis 缓存

/**
 * 6. 初始化数据库
 * 
 * 首次部署时，需要初始化数据库：
 */

// 进入后端容器
// docker-compose exec backend bash

// 运行数据库迁移
// cd /app
// python -m alembic upgrade head

// 如果需要，可以创建初始管理员用户
// python -m app.initial_data

// 退出容器
// exit

/**
 * 7. 检查服务状态
 */

// 查看所有容器的运行状态
// docker-compose ps

// 确保所有服务都处于 "Up" 状态

/**
 * 8. 访问应用
 * 
 * 现在，您可以通过以下 URL 访问应用：
 * - 前端应用：http://your-server-ip:3000
 * - 后端 API：http://your-server-ip:8000
 */

/**
 * 9. 配置 Nginx 反向代理（可选但推荐）
 * 
 * 为了更好的安全性和性能，建议使用 Nginx 作为反向代理：
 */

// 安装 Nginx
// sudo apt install -y nginx

// 创建 Nginx 配置文件
// sudo nano /etc/nginx/sites-available/enterprise-agent-platform

// 添加以下配置：
/*
server {
    listen 80;
    server_name your-domain.com;  # 替换为您的域名或服务器 IP

    # 前端应用
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket 支持
    location /ws {
        proxy_pass http://localhost:8000/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
*/

// 启用配置并重启 Nginx
// sudo ln -s /etc/nginx/sites-available/enterprise-agent-platform /etc/nginx/sites-enabled/
// sudo nginx -t  # 测试配置是否有效
// sudo systemctl restart nginx

/**
 * 10. 配置 SSL/TLS（可选但强烈推荐）
 * 
 * 使用 Let's Encrypt 获取免费的 SSL 证书：
 */

// 安装 Certbot
// sudo apt install -y certbot python3-certbot-nginx

// 获取并配置证书
// sudo certbot --nginx -d your-domain.com

// 按照提示完成配置

/**
 * 11. 设置自动更新和备份
 */

// 自动更新容器
// 创建一个脚本来定期更新容器：
// nano ~/update-containers.sh

// 添加以下内容：
/*
#!/bin/bash
cd /path/to/enterprise-agent-platform
git pull
docker-compose down
docker-compose up -d
*/

// 设置执行权限：
// chmod +x ~/update-containers.sh

// 添加到 crontab 定期执行：
// crontab -e

// 添加以下行（每周日凌晨 2 点更新）：
// 0 2 * * 0 ~/update-containers.sh >> ~/container-updates.log 2>&1

// 数据库备份
// 创建一个数据库备份脚本：
// nano ~/backup-db.sh

// 添加以下内容：
/*
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR=~/database_backups

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份 MySQL 数据库
docker-compose exec -T mysql mysqldump -u root -p123456 agent_platform > $BACKUP_DIR/agent_platform_$TIMESTAMP.sql

# 保留最近 30 天的备份
find $BACKUP_DIR -name "*.sql" -type f -mtime +30 -delete
*/

// 设置执行权限：
// chmod +x ~/backup-db.sh

// 添加到 crontab 定期执行：
// crontab -e

// 添加以下行（每天凌晨 1 点备份）：
// 0 1 * * * ~/backup-db.sh >> ~/database-backups.log 2>&1

/**
 * 12. 监控和日志管理
 */

// 设置日志轮转
// 创建 Docker 日志轮转配置：
// sudo nano /etc/docker/daemon.json

// 添加以下内容：
/*
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
*/

// 重启 Docker 服务：
// sudo systemctl restart docker

// 查看日志
// 查看所有容器的日志
// docker-compose logs

// 查看特定服务的日志
// docker-compose logs backend
// docker-compose logs frontend
// docker-compose logs mysql
// docker-compose logs redis

// 实时查看日志
// docker-compose logs -f backend

/**
 * 13. 故障排除
 * 
 * 如果遇到问题，可以尝试以下步骤：
 * 
 * 1. 检查容器状态：
 *    docker-compose ps
 * 
 * 2. 检查容器日志：
 *    docker-compose logs <service-name>
 * 
 * 3. 重启特定服务：
 *    docker-compose restart <service-name>
 * 
 * 4. 重建并重启所有服务：
 *    docker-compose down
 *    docker-compose up -d
 * 
 * 5. 检查网络连接：
 *    docker network inspect enterprise-agent-platform_app-network
 */

/**
 * 总结
 * 
 * 通过以上步骤，您已经成功地在 Ubuntu 系统上部署了企业智能助手平台的所有组件。
 * 系统现在应该可以正常运行，并且配置了自动更新、备份和监控。
 * 
 * 如果您需要扩展系统或提高性能，可以考虑使用更高级的部署策略，
 * 如 Kubernetes 集群或云服务提供商的托管服务。
 */ 