@echo off
chcp 65001 >nul
echo ========================================
echo GitHub SSH 连接快速修复脚本
echo ========================================
echo.

echo [1] 方案一：修改 hosts 文件（需要管理员权限）
echo [2] 方案二：配置 SSH 使用 HTTPS 端口 443
echo [3] 方案三：改用 HTTPS 方式（临时方案）
echo [4] 测试当前 SSH 连接
echo [5] 查看详细诊断信息
echo [0] 退出
echo.

set /p choice="请选择 [0-5]: "

if "%choice%"=="1" goto solution1
if "%choice%"=="2" goto solution2
if "%choice%"=="3" goto solution3
if "%choice%"=="4" goto test
if "%choice%"=="5" goto diagnose
if "%choice%"=="0" goto end

:solution1
echo.
echo ========================================
echo 方案一：修改 hosts 文件
echo ========================================
echo.
echo 请按照以下步骤操作：
echo.
echo 1. 以管理员身份打开记事本
echo 2. 打开文件：C:\Windows\System32\drivers\etc\hosts
echo 3. 找到被注释的 GitHub 行（以 # 开头）
echo 4. 删除行首的 # 和空格，保存文件
echo.
echo 或者在文件末尾添加：
echo 140.82.112.3    github.com
echo.
echo 修改后执行：ipconfig /flushdns
echo.
notepad C:\Windows\System32\drivers\etc\hosts
goto end

:solution2
echo.
echo ========================================
echo 方案二：配置 SSH 使用端口 443
echo ========================================
echo.
echo 正在修改 SSH 配置文件...
echo.

(
echo.
echo # GitHub SSH over HTTPS
echo Host github.com
echo     HostName ssh.github.com
echo     Port 443
echo     User git
echo     IdentityFile ~/.ssh/id_ed25519
) >> %USERPROFILE%\.ssh\config

echo [OK] SSH 配置已更新！
echo.
echo 测试连接：
ssh -T git@github.com
goto end

:solution3
echo.
echo ========================================
echo 方案三：改用 HTTPS 方式
echo ========================================
echo.
echo 请在您的 Git 仓库目录执行：
echo.
echo git remote set-url github https://github.com/shumengya/QuickGit.git
echo git push github main
echo.
echo 注意：需要使用 GitHub Personal Access Token 作为密码
goto end

:test
echo.
echo ========================================
echo 测试 SSH 连接
echo ========================================
echo.
ssh -T git@github.com
echo.
goto end

:diagnose
echo.
echo ========================================
echo 详细诊断信息
echo ========================================
echo.
echo [1] DNS 解析结果：
nslookup github.com
echo.
echo [2] SSH 密钥状态：
dir %USERPROFILE%\.ssh\id_*
echo.
echo [3] Git 远程仓库配置：
git remote -v
echo.
echo [4] 详细 SSH 测试：
ssh -vT git@github.com
goto end

:end
echo.
pause
