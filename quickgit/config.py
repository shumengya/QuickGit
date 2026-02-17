"""
配置模块 - 存储项目配置信息
"""

import os
import json


class Config:
    """配置类"""
    
    # 配置文件路径
    CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".quickgit_config.json")
    
    # 默认配置
    _defaults = {
        "gitea_host": "git.shumengya.top",
        "gitea_port": "8022",
        "github_user": "shumengya",
        "default_branch": "main"
    }
    
    # 运行时配置（从文件加载或使用默认值）
    _config = None
    
    @classmethod
    def _load_config(cls):
        """加载配置文件"""
        if cls._config is not None:
            return
        
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    cls._config = json.load(f)
            except Exception:
                cls._config = cls._defaults.copy()
        else:
            cls._config = cls._defaults.copy()
    
    @classmethod
    def _save_config(cls):
        """保存配置到文件"""
        cls._load_config()
        try:
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(cls._config, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    @classmethod
    def get(cls, key: str, default=None):
        """获取配置项"""
        cls._load_config()
        return cls._config.get(key, default)
    
    @classmethod
    def set(cls, key: str, value):
        """设置配置项"""
        cls._load_config()
        cls._config[key] = value
        cls._save_config()
    
    # 属性访问器（保持向后兼容）
    @property
    def GITEA_HOST(self) -> str:
        return self.get("gitea_host", self._defaults["gitea_host"])
    
    @property
    def GITEA_PORT(self) -> str:
        return self.get("gitea_port", self._defaults["gitea_port"])
    
    @property
    def GITHUB_USER(self) -> str:
        return self.get("github_user", self._defaults["github_user"])
    
    @property
    def DEFAULT_BRANCH(self) -> str:
        return self.get("default_branch", self._defaults["default_branch"])
    
    # 类方法访问器（用于类级别访问）
    @classmethod
    def get_gitea_host(cls) -> str:
        return cls.get("gitea_host", cls._defaults["gitea_host"])
    
    @classmethod
    def get_gitea_port(cls) -> str:
        return cls.get("gitea_port", cls._defaults["gitea_port"])
    
    @classmethod
    def get_github_user(cls) -> str:
        return cls.get("github_user", cls._defaults["github_user"])
    
    @classmethod
    def get_default_branch(cls) -> str:
        return cls.get("default_branch", cls._defaults["default_branch"])
    
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
