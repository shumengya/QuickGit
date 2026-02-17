# QuickGit - 萌芽一键Git管理工具

一个纯 Python 3.6+、零外部依赖的彩色 CLI 工具，用模块化方式把常用 Git 操作"一键化"，支持 Windows / Linux / macOS。

**⚠️ 重要说明：** 本工具目前仅支持通过 **SSH 方式**连接 GitHub 和 Gitea 远程仓库，不支持 HTTPS 方式。使用前请确保已配置 SSH 密钥。

## 1) 项目简介与核心卖点
- 模块化架构，功能职责清晰，易扩展。
- 无三方依赖，直接随 Python 运行。
- 跨平台路径与编码适配，默认分支 `main`。
- 彩色输出 + ASCII 分隔线，兼顾可读性与兼容性。
- **SSH 优先策略**：仅支持 SSH 连接，更安全、更便捷。

## 2) 功能清单
- [x] 灵活目录选择（启动时可管理任意仓库）
- [x] 初始化仓库（创建分支、生成 `.gitignore`）
- [x] 提交更改（提交到本地仓库）
- [x] 推送更改（推送到远程仓库，支持多远程选择，**仅支持 SSH**）
- [x] 从远程拉取（**仅支持 SSH**）
- [x] 远程仓库管理（GitHub / Gitea / 自建 Git 服务器，**仅支持 SSH 方式**）
- [x] **可配置 Gitea 服务器**（自定义主机地址和端口）
- [x] **自建 Git 仓库支持**（GitLab、自建 Gitea、Gogs 等）
- [x] 状态查看（工作区状态 + 最近提交）
- [ ] 分支管理
- [ ] 标签管理
- [ ] 冲突解决辅助
- [ ] 批量处理多个仓库
- [ ] HTTPS 支持（未来版本）

## 3) 项目结构
```
QuickGit/
├── quickgit/              # 核心模块
│   ├── __init__.py
│   ├── config.py          # 常量与 .gitignore 模板
│   ├── utils.py           # 颜色、输出、命令执行、输入校验、平台工具
│   ├── git_operations.py  # init / add / commit / push / pull / status
│   ├── remote_manager.py  # 远程管理（GitHub/Gitea）
│   └── ui.py              # 交互与菜单
├── quickgit.py            # 主入口（模块化版本）
├── run.bat                # Windows 启动脚本（UTF-8）
├── run.sh                 # Linux/macOS 启动脚本（需 chmod +x）
├── mengya_git_manager.py  # 旧版单文件脚本（兼容保留）
└── README.md
```

## 4) 快速开始

### 前置要求
1. **必需**：已安装 Git 和 Python 3.6+
2. **必需**：已配置 SSH 密钥并添加到 GitHub/Gitea 账户
3. **推荐**：使用支持 ANSI 颜色的终端（Windows Terminal、PowerShell、iTerm2 等）

### SSH 密钥配置指南
如果你还没有配置 SSH 密钥，请按以下步骤操作：

```bash
# 1. 生成 SSH 密钥（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 查看公钥内容
cat ~/.ssh/id_ed25519.pub    # Linux/macOS
type %USERPROFILE%\.ssh\id_ed25519.pub    # Windows

# 3. 将公钥添加到远程仓库
# - GitHub: Settings -> SSH and GPG keys -> New SSH key
# - Gitea: 设置 -> SSH/GPG 密钥 -> 添加密钥

# 4. 测试连接
ssh -T git@github.com                           # 测试 GitHub
ssh -T git@git.shumengya.top -p 8022           # 测试 Gitea
```

### 启动程序

**Windows**
```bash
run.bat
# 或
python quickgit.py
```

**Linux / macOS**
```bash
chmod +x run.sh
./run.sh
# 或
python3 quickgit.py
```

## 5) 交互流程
- 启动即要求选择工作目录：支持绝对/相对路径，直接回车使用脚本所在目录，自动校验目录存在。
- 主菜单（含永久提示）：
```
[1] 初始化Git仓库
[2] 提交更改到本地
[3] 推送到远程仓库
[4] 从远程仓库拉取
[5] 查看仓库状态
[6] 管理远程仓库
[7] 退出程序
[*] 提交代码前建议先拉取最新代码，减少代码冲突
[*] 使用SSH进行Git提交更方便快捷和安全
```

## 6) 常用操作示例

### 场景0: 选择工作目录
- 启动时输入要管理的仓库路径
- 支持绝对路径、相对路径、`~` 路径
- 直接回车使用当前目录

### 场景1: 初始化新仓库
1. 选择 [1] 初始化Git仓库
2. 自动创建 `.gitignore`（含前端/后端通用规则）
3. 自动创建 `main` 分支并进行首次提交
4. 选择 [6] 管理远程仓库 → 添加 GitHub 或 Gitea 远程仓库（**仅 SSH**）

### 场景2: 日常提交工作流
1. 选择 [2] 提交更改到本地
   - 查看更改的文件
   - 输入提交信息（留空自动填入时间戳）
   - 代码提交到本地仓库
2. 选择 [3] 推送到远程仓库
   - 选择远程仓库（可多选）
   - 通过 SSH 推送到远程

### 场景3: 拉取远程更新
1. 选择 [4] 从远程仓库拉取
2. 选择远程仓库（单选）
3. 通过 SSH 拉取当前分支的更新

### 场景4: 管理远程仓库

选择 [6] 管理远程仓库，提供以下功能：

#### 4.1 添加 GitHub 远程仓库
SSH 格式：`git@github.com:shumengya/{repo}.git`

#### 4.2 添加 Gitea 远程仓库
SSH 格式：`ssh://git@git.shumengya.top:8022/{user}/{repo}.git`

默认使用配置的 Gitea 服务器地址和端口，可通过"配置 Gitea 服务器"修改。

#### 4.3 添加自建 Git 仓库
支持添加自定义 Git 服务器（GitLab、自建 Gitea、Gogs 等）：
1. 输入远程仓库名称（如：`gitlab`、`mygit`）
2. 输入完整的 SSH URL
3. 支持的 URL 格式示例：
   - `git@gitlab.com:user/repo.git`
   - `ssh://git@your-server.com:port/user/repo.git`

#### 4.4 配置 Gitea 服务器
自定义 Gitea 服务器的主机地址和 SSH 端口：
- 默认主机：`git.shumengya.top`
- 默认端口：`8022`
- 配置保存在：`~/.quickgit_config.json`

#### 4.5 其他功能
- **查看所有远程仓库** - 显示已配置的远程仓库列表
- **删除远程仓库** - 移除不需要的远程仓库

**⚠️ 注意：** 本工具不支持 HTTPS URL 格式（如 `https://github.com/user/repo.git`），仅支持 SSH 格式。

### 场景5: 配置文件

QuickGit 的配置文件保存在：`~/.quickgit_config.json`

**配置内容：**
```json
{
  "gitea_host": "git.shumengya.top",
  "gitea_port": "8022",
  "github_user": "shumengya",
  "default_branch": "main"
}
```

**修改方式：**
- 通过菜单：[6] 管理远程仓库 → [5] 配置 Gitea 服务器
- 或手动编辑配置文件（需重启工具生效）

## 7) 跨平台与终端要求
- `run.bat` 自动设置 UTF-8；Windows 使用 `python` 命令。
- `run.sh` 设置 `LANG/LC_ALL`，首次需 `chmod +x run.sh`；Linux/macOS 使用 `python3`。
- 终端需支持 ANSI 颜色；仅使用 ASCII 符号，避免编码错位。

## 8) 控制台输出规范
- 分隔线宽度固定 60：`======` / `------` / `·····`。
- 禁止使用 emoji 和 Unicode 盒线字符。
- 颜色键值：成功绿、错误红、信息青、警告黄、标题青/品红。
- 状态/提示图标：`[√] [×] [i] [!] [>] [*]`。

## 9) 手动测试清单
- 启动脚本：`run.bat`、`run.sh`、直接运行 `python/ python3 quickgit.py`。
- 颜色与中文显示正常，分隔线对齐 60 列。
- 初始化仓库、提交+推送、拉取、远程管理均可用。
- 默认分支 `main`；`.gitignore` 自动写入成功。

## 10) 常见问题 / 故障排查

### SSH 相关问题
- **推送/拉取失败 "Permission denied (publickey)"**：
  - 确认 SSH 密钥已生成：`ls ~/.ssh/id_*.pub` (Linux/macOS) 或 `dir %USERPROFILE%\.ssh\id_*.pub` (Windows)
  - 确认公钥已添加到 GitHub/Gitea 账户
  - 测试 SSH 连接：`ssh -T git@github.com` 或 `ssh -T git@git.shumengya.top -p 8022`
  
- **"Could not resolve hostname"**：
  - 检查网络连接
  - 确认远程仓库地址格式正确（SSH 格式，非 HTTPS）
  
- **端口被防火墙拦截**：
  - GitHub 使用标准 SSH 端口 22
  - Gitea 使用自定义端口 8022，确保防火墙允许此端口

### 远程仓库相关
- **不支持 HTTPS URL**：本工具仅支持 SSH 方式，如果你的远程仓库使用 HTTPS URL（如 `https://github.com/user/repo.git`），请手动改为 SSH 格式或使用 `git remote` 命令修改。

### 终端显示问题
- **终端乱码**：设置 UTF-8（Windows 可 `chcp 65001`；Linux/macOS 确保 `LANG/LC_ALL` 为 UTF-8）。
- **颜色不显示**：使用支持 ANSI 的终端（Windows Terminal/PowerShell 等）。
- **找不到 `python3`**：在 Linux/macOS 安装或创建软链接；Windows 使用 `python`。

## 11) 路线图
- [x] 模块化架构重构
- [x] SSH 方式支持（GitHub + Gitea）
- [x] 可配置 Gitea 服务器
- [x] 自建 Git 仓库支持（GitLab、自建 Gitea 等）
- [x] 配置文件持久化
- [ ] HTTPS 方式支持
- [ ] 分支管理
- [ ] 标签管理
- [ ] 冲突解决辅助
- [ ] 批量操作多个仓库
- [ ] 更多 Git 托管平台支持（Bitbucket 等）

## 12) 许可证与作者
- 许可证：MIT
- 作者：shumengya

让 Git 操作更简单，让开发更高效！
