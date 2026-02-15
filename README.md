# QuickGit - 萌芽一键Git管理工具

一个简单易用的模块化Git命令行管理工具，让Git操作更加便捷高效。

## 功能特性

- **一键初始化Git仓库** - 自动完成Git初始化、分支创建、.gitignore配置
- **一键提交推送** - 快速提交代码并推送到远程仓库
- **多仓库支持** - 同时支持GitHub和Gitea仓库管理
- **远程仓库管理** - 便捷地添加、删除、查看远程仓库
- **状态查看** - 快速查看仓库状态和提交历史
- **彩色界面** - 友好的彩色控制台输出
- **模块化设计** - 易于维护和扩展
- **跨平台支持** - 完美兼容 Windows、Linux、macOS

## 项目结构

```
QuickGit/
├── quickgit/              # 核心模块
│   ├── __init__.py       # 包初始化
│   ├── config.py         # 配置模块
│   ├── utils.py          # 工具类（命令执行、输出格式化、输入验证、平台工具）
│   ├── git_operations.py # Git操作模块
│   ├── remote_manager.py # 远程仓库管理模块
│   └── ui.py            # UI交互模块
├── quickgit.py          # 主程序入口
├── run.bat              # Windows启动脚本
├── run.sh               # Linux/macOS启动脚本
├── mengya_git_manager.py # 旧版单文件脚本（兼容保留）
└── README.md            # 项目文档
```

## 快速开始

### 运行脚本

**Windows:**
```bash
# 使用启动脚本（自动设置UTF-8编码）
run.bat

# 或直接运行
python quickgit.py
```

**Linux/macOS:**
```bash
# 首次使用需要添加执行权限
chmod +x run.sh

# 使用启动脚本（推荐）
./run.sh

# 或直接运行
python3 quickgit.py
```

**通用方式:**
```bash
# 新版模块化脚本（推荐）
python quickgit.py

# 或使用旧版单文件脚本
python mengya_git_manager.py
```

### 主要功能菜单

```
1. 初始化Git仓库
2. 提交并推送更改
3. 从远程仓库拉取
4. 查看仓库状态
5. 管理远程仓库
6. 退出
```

## 使用场景

### 场景1：初始化新项目

1. 在项目目录运行脚本
2. 选择 `1. 初始化Git仓库`
3. 按提示配置GitHub或Gitea远程仓库
4. 完成首次提交

### 场景2：提交代码更改

1. 修改代码后运行脚本
2. 选择 `2. 提交并推送更改`
3. 输入提交信息（或使用默认信息）
4. 选择推送到哪个远程仓库

### 场景3：拉取远程更新

1. 运行脚本
2. 选择 `3. 从远程仓库拉取`
3. 选择要拉取的远程仓库

## 远程仓库配置

### GitHub配置

- 使用SSH方式连接
- 格式：`git@github.com:shumengya/{仓库名}.git`

### Gitea配置

- 服务器地址：`repo.shumengya.top:8022`
- 使用SSH方式连接
- 格式：`ssh://git@repo.shumengya.top:8022/{用户名}/{仓库名}.git`

## .gitignore 支持

脚本自动创建的 `.gitignore` 文件支持以下项目类型：

- **Node.js/React** - node_modules/, build/, dist/
- **Go** - *.exe, *.test, vendor/
- **Python** - __pycache__/, venv/, *.pyc
- **通用** - 日志文件、临时文件、IDE配置

## 系统要求

- **Python:** 3.6+ (Linux/macOS 使用 python3)
- **Git:** 已安装并配置
- **SSH密钥:** 已配置（用于远程仓库推送）
- **操作系统:** Windows、Linux、macOS 均支持

### 平台特定说明

**Windows:**
- 建议使用 `run.bat` 启动，自动配置UTF-8编码
- 控制台需支持ANSI颜色代码（Windows 10+自带支持）

**Linux/macOS:**
- 使用 `python3` 命令运行
- 确保终端支持UTF-8编码和颜色显示
- 首次使用 `run.sh` 需要添加执行权限：`chmod +x run.sh`

## 注意事项

1. 首次使用前请确保已配置Git用户信息：
   ```bash
   git config --global user.name "你的名字"
   git config --global user.email "你的邮箱"
   ```

2. 使用SSH方式连接需要提前配置SSH密钥

3. 推送到Gitea时请确保仓库已在服务器上创建

4. **重要提示:** 提交代码前建议先拉取最新代码，减少代码冲突
   - 先执行 `3. 从远程仓库拉取`
   - 再执行 `2. 提交并推送更改`

## 常见问题

**Q: 推送失败怎么办？**  
A: 请检查SSH密钥配置和远程仓库地址是否正确

**Q: 如何切换远程仓库？**  
A: 使用 `5. 管理远程仓库` 功能添加或删除远程仓库

**Q: 支持哪些Git操作？**  
A: 目前支持init、add、commit、push、pull等常用操作

## 模块说明

### config.py - 配置模块
存储所有配置信息，包括Gitea服务器地址、GitHub用户名、.gitignore模板等。

### utils.py - 工具类模块
- `Colors`: 控制台颜色定义
- `CommandExecutor`: 命令执行器
- `OutputFormatter`: 输出格式化器
- `InputValidator`: 输入验证器
- `PlatformUtils`: 跨平台工具（清屏、平台检测）

### git_operations.py - Git操作模块
提供Git基本操作功能：
- 初始化仓库
- 检查状态
- 添加/提交更改
- 推送/拉取代码

### remote_manager.py - 远程仓库管理模块
管理GitHub和Gitea远程仓库：
- 添加/删除远程仓库
- 查看远程仓库列表
- 选择推送/拉取目标

### ui.py - UI交互模块
处理用户界面和交互逻辑，整合所有功能模块。

## 开发计划

- [x] 模块化架构重构
- [ ] 支持分支管理
- [ ] 支持标签管理
- [ ] 支持冲突解决辅助
- [ ] 支持自定义配置文件
- [ ] 支持批量操作多个仓库

## 许可证

MIT License

## 作者

shumengya

---

**让Git操作更简单，让开发更高效！**
