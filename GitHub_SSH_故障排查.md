# GitHub SSH 连接问题诊断与解决方案

**⚠️ QuickGit 工具说明：** 本工具目前仅支持 SSH 方式连接远程仓库，不支持 HTTPS。本文档中提到的 HTTPS 方案仅适用于手动使用 `git` 命令行操作，不适用于 QuickGit 工具本身。

---

## 问题现象

```
Connection closed by 198.18.0.66 port 22
fatal: Could not read from remote repository.
```

这个错误表明 SSH 连接被关闭，可能的原因包括：
1. SSH 密钥未正确配置
2. SSH 密钥未添加到 GitHub
3. 网络问题或代理设置
4. SSH 配置文件问题

---

## 诊断步骤

### 第 1 步：检查 SSH 密钥是否存在

**Windows:**
```bash
dir %USERPROFILE%\.ssh
```

**Linux/macOS:**
```bash
ls -la ~/.ssh
```

**应该看到:**
- `id_rsa` 和 `id_rsa.pub` (RSA 密钥)
- 或 `id_ed25519` 和 `id_ed25519.pub` (Ed25519 密钥，推荐)

---

### 第 2 步：如果没有 SSH 密钥，生成新密钥

**推荐方式 (Ed25519):**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**传统方式 (RSA):**
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

**执行过程:**
```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/user/.ssh/id_ed25519): [直接回车]
Enter passphrase (empty for no passphrase): [可以直接回车或输入密码]
Enter same passphrase again: [重复密码]
```

---

### 第 3 步：查看公钥内容

**Windows:**
```bash
type %USERPROFILE%\.ssh\id_ed25519.pub
# 或
type %USERPROFILE%\.ssh\id_rsa.pub
```

**Linux/macOS:**
```bash
cat ~/.ssh/id_ed25519.pub
# 或
cat ~/.ssh/id_rsa.pub
```

**复制输出的完整内容**，类似：
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM... your_email@example.com
```

---

### 第 4 步：添加公钥到 GitHub

1. **登录 GitHub**: https://github.com
2. **打开设置**: 点击右上角头像 → Settings
3. **SSH 和 GPG 密钥**: 左侧菜单 → SSH and GPG keys
4. **添加新密钥**: 点击 "New SSH key" 按钮
5. **填写信息:**
   - Title: 给密钥起个名字（如：My Windows PC）
   - Key: 粘贴第3步复制的公钥内容
6. **保存**: 点击 "Add SSH key"

---

### 第 5 步：测试 SSH 连接

```bash
ssh -T git@github.com
```

**成功的输出:**
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

**如果仍然失败，继续下一步...**

---

## 常见问题与解决方案

### 问题 1: Connection closed by 198.18.0.66

这个 IP 地址 `198.18.0.66` 不是 GitHub 的官方 IP，可能是：
- 代理服务器
- VPN
- 公司网络的网关

**解决方案：检查代理设置**

#### 方案 A: 配置 Git 使用代理

如果您在使用代理，需要配置：

```bash
# HTTP 代理
git config --global http.proxy http://proxy_server:port
git config --global https.proxy https://proxy_server:port

# SOCKS5 代理
git config --global http.proxy socks5://proxy_server:port
```

#### 方案 B: 取消代理设置

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

#### 方案 C: 为 SSH 配置代理

创建或编辑 `~/.ssh/config` 文件：

**Windows:** `C:\Users\YourName\.ssh\config`
**Linux/macOS:** `~/.ssh/config`

```
Host github.com
    HostName github.com
    User git
    # 如果使用 HTTP 代理
    ProxyCommand connect -H proxy_server:port %h %p
    # 如果使用 SOCKS5 代理
    # ProxyCommand connect -S proxy_server:port %h %p
```

---

### 问题 2: Permission denied (publickey)

**原因:** SSH 密钥未被识别

**解决方案:**

1. **启动 SSH Agent:**
   ```bash
   # Windows (Git Bash)
   eval "$(ssh-agent -s)"
   
   # Linux/macOS
   eval "$(ssh-agent -s)"
   ```

2. **添加私钥到 SSH Agent:**
   ```bash
   ssh-add ~/.ssh/id_ed25519
   # 或
   ssh-add ~/.ssh/id_rsa
   ```

3. **再次测试连接:**
   ```bash
   ssh -T git@github.com
   ```

---

### 问题 3: 防火墙阻止 SSH 端口 22

**解决方案 A: 使用 HTTPS 代替 SSH**

修改远程仓库 URL：
```bash
# 查看当前 URL
git remote -v

# 修改为 HTTPS
git remote set-url origin https://github.com/shumengya/QuickGit.git
```

**缺点:** 每次推送需要输入用户名和密码（或 Token）

**解决方案 B: 使用 SSH over HTTPS (端口 443)**

编辑 `~/.ssh/config`:
```
Host github.com
    HostName ssh.github.com
    Port 443
    User git
```

测试：
```bash
ssh -T -p 443 git@ssh.github.com
```

---

### 问题 4: SSH 密钥格式错误

**原因:** Windows 换行符问题或复制时引入了额外字符

**解决方案:**

1. **重新生成密钥**（推荐）
2. **或确保公钥完整且格式正确**

---

## QuickGit 用户的完整解决流程

### 步骤 1: 生成 SSH 密钥

```bash
# Windows (Git Bash 或 PowerShell)
ssh-keygen -t ed25519 -C "shumengya@example.com"

# 一路回车即可
```

### 步骤 2: 复制公钥

```bash
# Windows
type %USERPROFILE%\.ssh\id_ed25519.pub

# Linux/macOS
cat ~/.ssh/id_ed25519.pub
```

### 步骤 3: 添加到 GitHub

1. 访问 https://github.com/settings/keys
2. 点击 "New SSH key"
3. 粘贴公钥，保存

### 步骤 4: 测试连接

```bash
ssh -T git@github.com
```

**期望输出:**
```
Hi shumengya! You've successfully authenticated...
```

### 步骤 5: 在 QuickGit 中重新配置远程仓库

如果之前的远程仓库配置有问题：

```bash
# 删除旧的 github 远程仓库
git remote remove github

# 重新添加
git remote add github git@github.com:shumengya/QuickGit.git

# 验证
git remote -v
```

### 步骤 6: 使用 QuickGit 推送

1. 启动 QuickGit
2. 选择 `[2] 提交更改到本地` - 提交到本地仓库
3. 选择 `[3] 推送到远程仓库` - 推送到 `github`（通过 SSH）

---

## 调试命令

如果问题仍然存在，使用以下命令获取详细信息：

```bash
# 详细模式测试 SSH 连接
ssh -vT git@github.com

# 查看 Git 配置
git config --list

# 查看远程仓库配置
git remote -v

# 手动推送（查看详细错误）
git push -v github main
```

---

## 快速修复：改用 HTTPS（仅适用于 git 命令行）

**⚠️ 重要：** 以下 HTTPS 方案仅适用于手动使用 `git` 命令行操作，**QuickGit 工具本身不支持 HTTPS**。

如果 SSH 问题难以解决，可以临时使用命令行的 HTTPS 方式：

```bash
# 修改远程仓库 URL
git remote set-url github https://github.com/shumengya/QuickGit.git

# 推送（需要输入用户名和密码/Token）
git push github main
```

**注意:** HTTPS 方式需要：
- GitHub 用户名
- Personal Access Token（不能使用密码）

**生成 Token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. 勾选 `repo` 权限
4. 复制 Token（只显示一次）

**再次强调：** QuickGit 工具不支持 HTTPS 远程仓库，必须使用 SSH。如果需要使用 HTTPS，请直接使用 `git` 命令行工具。

---

## 总结

**推荐解决方案顺序（用于 QuickGit）:**

1. ✅ 生成 SSH 密钥
2. ✅ 添加公钥到 GitHub
3. ✅ 测试 SSH 连接
4. ✅ 配置 SSH Agent（如果需要）
5. ⚠️ 检查代理设置（如果在公司网络）
6. ⚠️ 使用 SSH over HTTPS（端口 443）作为备选

**注意：** QuickGit 工具不支持 HTTPS 方式，必须解决 SSH 连接问题才能正常使用。如果实在无法配置 SSH，建议直接使用 `git` 命令行工具配合 HTTPS。
