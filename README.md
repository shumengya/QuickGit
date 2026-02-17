# QuickGit - 萌芽一键Git管理工具

一个纯 Python 3.6+、零外部依赖的彩色 CLI 工具，用模块化方式把常用 Git 操作“一键化”，支持 Windows / Linux / macOS。

## 1) 项目简介与核心卖点
- 模块化架构，功能职责清晰，易扩展。
- 无三方依赖，直接随 Python 运行。
- 跨平台路径与编码适配，默认分支 `main`。
- 彩色输出 + ASCII 分隔线，兼顾可读性与兼容性。

## 2) 功能清单
- [x] 灵活目录选择（启动时可管理任意仓库）
- [x] 初始化仓库（创建分支、生成 `.gitignore`）
- [x] 提交更改（提交到本地仓库）
- [x] 推送更改（推送到远程仓库，支持多远程选择）
- [x] 从远程拉取
- [x] 远程仓库管理（GitHub / Gitea，SSH 优先）
- [x] 状态查看（工作区状态 + 最近提交）
- [ ] 分支管理
- [ ] 标签管理
- [ ] 冲突解决辅助
- [ ] 自定义配置文件
- [ ] 批量处理多个仓库

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
前置要求：已安装 Git，Python 3.6+；已配置 SSH 密钥（推荐用 SSH 访问远程仓库）。

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
- 初始化仓库：选择目录 → 选 1 → 自动创建 `.gitignore`（含前端/后端通用规则）并尝试首提。
- 提交更改：选 2 → 查看更改 → 输入提交信息（留空自动填入时间戳）→ 提交到本地仓库。
- 推送更改：选 3 → 选择远程（可多选）→ 推送到远程仓库。
- 拉取更新：选 4 → 选择远程 → 拉取当前分支。
- 远程管理：选 6 → 支持添加/删除远程；URL 模板  
  - GitHub: `git@github.com:shumengya/{repo}.git`  
  - Gitea : `ssh://git@git.shumengya.top:8022/{user}/{repo}.git`

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
- 推送失败：确认 SSH 密钥已添加且远程地址正确。
- 终端乱码：设置 UTF-8（Windows 可 `chcp 65001`；Linux/macOS 确保 `LANG/LC_ALL` 为 UTF-8）。
- 颜色不显示：使用支持 ANSI 的终端（Windows Terminal/PowerShell 等）。
- 找不到 `python3`：在 Linux/macOS 安装或创建软链接；Windows 使用 `python`。

## 11) 路线图
- [x] 模块化架构重构
- [ ] 分支管理
- [ ] 标签管理
- [ ] 冲突解决辅助
- [ ] 自定义配置文件
- [ ] 批量操作多个仓库

## 12) 许可证与作者
- 许可证：MIT
- 作者：shumengya

让 Git 操作更简单，让开发更高效！
