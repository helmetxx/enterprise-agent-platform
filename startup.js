/**
 * Creative Platform 启动指南 (Windows 11 环境)
 * 
 * 前置条件:
 * 1. 已安装 Docker Desktop for Windows
 * 2. Docker Desktop 已启动且运行正常 (可在系统托盘查看状态)
 * 3. 确保以下端口未被占用:
 *    - 3000 (前端)
 *    - 8000 (后端)
 *    - 3307 (MySQL，避免与本地 MySQL 3306 冲突)
 *    - 6380 (Redis，避免与本地 Redis 6379 冲突)
 * 
 * 目录结构:
 * .
 * ├── docker-compose.yml
 * ├── frontend/
 * │   ├── Dockerfile
 * │   ├── nginx.conf
 * │   └── ...
 * ├── backend/
 * │   ├── Dockerfile
 * │   └── ...
 * └── migrations/
 *     └── init.sql
 * 
 * 启动步骤:
 * 
 * 1. 打开 PowerShell 或 CMD，进入项目根目录
 * 
 * 2. 首次启动（构建并运行）:
 * ```powershell
 * docker-compose up --build
 * ```
 * 
 * 3. 后续启动（无需重新构建）:
 * ```powershell
 * docker-compose up
 * ```
 * 
 * 4. 在后台运行:
 * ```powershell
 * docker-compose up -d
 * ```
 * 
 * 5. 查看日志:
 * ```powershell
 * # 查看所有日志
 * docker-compose logs -f
 * 
 * # 查看特定服务日志
 * docker-compose logs frontend
 * docker-compose logs backend
 * docker-compose logs mysql
 * docker-compose logs redis
 * ```
 * 
 * 6. 停止服务:
 * ```powershell
 * docker-compose down
 * ```
 * 
 * 7. 完全重置（包括数据库）:
 * ```powershell
 * docker-compose down -v
 * docker-compose up --build
 * ```
 * 
 * 访问地址:
 * - 前端界面: http://localhost:3000
 * - 后端API: http://localhost:8000/api/v1
 * - API文档: http://localhost:8000/docs
 * 
 * 常见问题:
 * 1. 如果 Docker Desktop 未启动，请先启动它
 * 2. 如果端口被占用，可以在 docker-compose.yml 中修改端口映射
 * 3. 如果遇到 WSL 相关错误，请确保 WSL 2 已正确安装
 * 4. 如果前端无法访问后端，检查 nginx 配置
 * 5. 如果后端无法连接数据库，检查环境变量配置
 * 
 * 调试命令:
 * ```powershell
 * # 查看所有容器状态
 * docker-compose ps
 * 
 * # 查看 Docker Desktop 仪表盘
 * # 可以在系统托盘图标右键打开 Dashboard
 * 
 * # 进入容器内部
 * docker-compose exec frontend sh
 * docker-compose exec backend bash
 * docker-compose exec mysql mysql -uroot -p123456 agent_platform
 * docker-compose exec redis redis-cli
 * 
 * # 查看容器日志
 * docker logs -f <container_id>
 * 
 * # 检查端口占用
 * netstat -ano | findstr "3000"
 * netstat -ano | findstr "8000"
 * netstat -ano | findstr "3307"
 * netstat -ano | findstr "6380"
 * ```
 * 
 * WSL 相关命令:
 * ```powershell
 * # 查看 WSL 状态
 * wsl --status
 * 
 * # 重启 WSL
 * wsl --shutdown
 * ```
 * 
 * 数据库连接信息:
 * - Host: localhost
 * - Port: 3307 (映射到容器内的 3306)
 * - Database: agent_platform
 * - Username: root
 * - Password: 123456
 * 
 * Redis 连接信息:
 * - Host: localhost
 * - Port: 6380 (映射到容器内的 6379)
 * - No password set
 * 
 * 注意事项:
 * 1. 确保 Docker Desktop 设置中的 "Use WSL 2 based engine" 已启用
 * 2. 如果修改了代码，需要重新构建镜像 (使用 --build 参数)
 * 3. Windows 文件路径使用反斜杠，但 Docker 相关配置使用正斜杠
 * 4. 首次启动数据库初始化可能需要一些时间
 * 5. MySQL 端口映射到 3307 是为了避免与本地 MySQL 冲突
 * 6. Redis 端口映射到 6380 是为了避免与本地 Redis 冲突
 */
