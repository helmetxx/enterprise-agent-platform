/**
 * 企业智能助手平台 - Git 仓库初始化指南
 * 
 * 本文档提供在 Cursor 编辑器中为企业智能助手平台建立 Git 仓库的完整步骤。
 */

/**
 * 1. 初始化本地 Git 仓库
 * 
 * 首先，在项目根目录中初始化一个 Git 仓库：
 */

// 在 Cursor 中打开终端（通常可以通过 Ctrl+` 或菜单栏中的 "Terminal" 选项）
// 确保您在项目根目录下，然后执行以下命令：
// git init

/**
 * 2. 配置 Git 用户信息
 * 
 * Git 需要知道您的身份信息才能创建提交。
 */

// 全局配置（推荐，适用于所有仓库）
// git config --global user.email "your.email@example.com"
// git config --global user.name "Your Name"

// 或者，仅为当前仓库配置
// git config user.email "your.email@example.com"
// git config user.name "Your Name"

// 验证配置是否正确
// git config user.name
// git config user.email

/**
 * 3. 创建 .gitignore 文件
 * 
 * 在将代码提交到仓库之前，创建一个 .gitignore 文件来排除不需要版本控制的文件：
 */

// 创建 .gitignore 文件
// touch .gitignore

// 然后在 Cursor 中编辑 .gitignore 文件，添加以下内容：
/*
# 环境变量文件
.env
.env.local

# 依赖目录
node_modules/
__pycache__/
*.py[cod]
*$py.class
.Python
env/
venv/
ENV/

# 构建输出
dist/
build/
*.so

# 日志文件
*.log
logs/

# 数据库文件
*.sqlite
*.db

# 系统文件
.DS_Store
Thumbs.db

# IDE 配置
.idea/
.vscode/
*.swp
*.swo

# 上传的文件
uploads/
generated_pdfs/
*/

/**
 * 4. 添加文件到暂存区
 */

// 将项目文件添加到 Git 暂存区：
// git add .

/**
 * 5. 提交初始代码
 */

// 提交您的初始代码：
// git commit -m "Initial commit: Enterprise Agent Platform"

/**
 * 6. 在 GitHub 上创建仓库
 * 
 * 1. 登录您的 GitHub 账户
 * 2. 点击右上角的 "+" 图标，选择 "New repository"
 * 3. 填写仓库名称，例如 "enterprise-agent-platform"
 * 4. 添加描述（可选）
 * 5. 选择仓库可见性（公开或私有）
 * 6. 不要初始化仓库（因为您已经有了本地仓库）
 * 7. 点击 "Create repository"
 */

/**
 * 7. 将本地仓库连接到 GitHub
 * 
 * GitHub 会显示连接本地仓库的命令。复制并在 Cursor 终端中执行这些命令：
 */

// git remote add origin https://github.com/您的用户名/enterprise-agent-platform.git
// git branch -M main
// git push -u origin main

/**
 * 8. 推送代码到 GitHub
 */

// git push -u origin main

/**
 * 9. 设置分支保护（可选）
 * 
 * 在 GitHub 仓库设置中，您可以设置分支保护规则，例如要求代码审查或状态检查通过才能合并到主分支。
 */

/**
 * 10. 设置 GitHub Actions 进行 CI/CD（可选）
 * 
 * 您可以在项目中添加 GitHub Actions 工作流配置，实现自动化测试和部署：
 */

// 在项目根目录创建 .github/workflows 目录：
// mkdir -p .github/workflows

// 创建一个基本的 CI 工作流文件 .github/workflows/ci.yml：
/*
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd backend
        pytest

  test-frontend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: |
        cd frontend
        npm install
    - name: Type check
      run: |
        cd frontend
        npm run type-check
*/

/**
 * 11. 使用 Git 进行日常开发
 * 
 * 在 Cursor 中进行日常开发时，您可以使用以下 Git 命令：
 * 
 * - 查看更改状态：git status
 * - 添加更改：git add <文件名> 或 git add .
 * - 提交更改：git commit -m "提交信息"
 * - 拉取远程更改：git pull
 * - 推送本地更改：git push
 * - 创建新分支：git checkout -b feature/新功能名称
 * - 切换分支：git checkout 分支名称
 */

/**
 * 12. 设置自动部署（可选）
 * 
 * 您可以设置 GitHub Actions 工作流，在代码推送到主分支时自动部署到服务器：
 */

// 创建 .github/workflows/deploy.yml 文件：
/*
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /path/to/enterprise-agent-platform
          git pull
          docker-compose down
          docker-compose up -d
*/

// 在 GitHub 仓库设置中添加必要的 secrets（HOST、USERNAME、SSH_KEY）

/**
 * 常见问题解决
 * 
 * 1. 如果提交时遇到身份错误：
 *    确保已配置 Git 用户名和邮箱（见步骤 2）
 * 
 * 2. 如果推送到 GitHub 时遇到权限错误：
 *    - 检查是否有正确的 GitHub 访问权限
 *    - 考虑使用 SSH 密钥而不是 HTTPS
 *    - 或者使用 GitHub CLI 进行身份验证
 * 
 * 3. 如果 .gitignore 不生效：
 *    - 确保文件格式正确
 *    - 如果文件已经被跟踪，使用 git rm --cached <文件> 移除跟踪
 */

/**
 * 总结
 * 
 * 通过以上步骤，您就可以在 Cursor 中建立 Git 仓库，
 * 并为您的企业智能助手平台设置完整的开发和部署流程。
 * 
 * 良好的版本控制实践将帮助您更有效地管理代码，
 * 并与团队成员协作开发。
 */ 