"""
配置模块 - 存储项目配置信息
"""


class Config:
    """配置类"""
    
    # Gitea服务器配置
    GITEA_HOST = "git.shumengya.top"
    GITEA_PORT = "8022"
    
    # GitHub配置
    GITHUB_USER = "shumengya"
    
    # Git配置
    DEFAULT_BRANCH = "main"
    
    # .gitignore模板
    GITIGNORE_TEMPLATE = """# Node/React
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
build/
dist/
coverage/
.env.local
.env.development.local
.env.test.local
.env.production.local

# Go
*.exe
*.exe~
*.test
*.out
*.dll
*.so
*.dylib
vendor/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# 数据文件
data/data.json
*.db
*.sqlite

# 日志文件
*.log
logs/

# 操作系统
.DS_Store
Thumbs.db
desktop.ini

# IDE
.idea/
.vscode/
*.swp
*.swo
*~
.project
.classpath
.settings/

# 其他
*.bak
*.tmp
*.temp
"""
