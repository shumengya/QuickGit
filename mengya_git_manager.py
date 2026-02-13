#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
萌芽一键Git管理工具
支持快速初始化Git仓库、提交更改、推送到GitHub和Gitea
"""

import os
import sys
import subprocess
from typing import Optional, List


class Colors:
    """控制台颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class GitManager:
    """Git管理器"""
    
    def __init__(self):
        self.gitea_host = "repo.shumengya.top"
        self.gitea_port = "8022"
        self.github_user = "shumengya"
        self.current_dir = os.getcwd()
    
    def print_header(self, text: str):
        """打印标题"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*50}")
        print(f"  {text}")
        print(f"{'='*50}{Colors.ENDC}\n")
    
    def print_success(self, text: str):
        """打印成功信息"""
        print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")
    
    def print_error(self, text: str):
        """打印错误信息"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")
    
    def print_info(self, text: str):
        """打印提示信息"""
        print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")
    
    def print_warning(self, text: str):
        """打印警告信息"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")
    
    def run_command(self, command: str, show_output: bool = True) -> tuple[bool, str]:
        """
        执行命令
        返回: (是否成功, 输出内容)
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            output = result.stdout + result.stderr
            
            if show_output and output.strip():
                print(output)
            
            return result.returncode == 0, output
        except Exception as e:
            self.print_error(f"命令执行失败: {str(e)}")
            return False, str(e)
    
    def is_git_repo(self) -> bool:
        """检查当前目录是否是Git仓库"""
        return os.path.isdir('.git')
    
    def get_gitignore_template(self) -> str:
        """获取.gitignore模板"""
        return """# Node/React
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
    
    def init_git_repo(self):
        """初始化Git仓库"""
        self.print_header("初始化Git仓库")
        
        if self.is_git_repo():
            self.print_warning("当前目录已经是Git仓库")
            return True
        
        # 1. 初始化Git仓库
        self.print_info("正在初始化Git仓库...")
        success, _ = self.run_command("git init", show_output=False)
        if not success:
            self.print_error("Git初始化失败")
            return False
        self.print_success("Git仓库初始化成功")
        
        # 2. 创建main分支
        self.print_info("正在创建main分支...")
        success, _ = self.run_command("git checkout -b main", show_output=False)
        if success:
            self.print_success("main分支创建成功")
        else:
            self.print_warning("main分支创建失败，将使用默认分支")
        
        # 3. 创建.gitignore文件
        self.print_info("正在创建.gitignore文件...")
        try:
            with open('.gitignore', 'w', encoding='utf-8') as f:
                f.write(self.get_gitignore_template())
            self.print_success(".gitignore文件创建成功")
        except Exception as e:
            self.print_error(f".gitignore文件创建失败: {str(e)}")
        
        # 4. 首次提交
        self.print_info("正在进行首次提交...")
        self.run_command("git add .", show_output=False)
        success, _ = self.run_command('git commit -m "first commit"', show_output=False)
        if success:
            self.print_success("首次提交完成")
        else:
            self.print_warning("首次提交失败（可能没有文件可提交）")
        
        # 5. 配置远程仓库
        self.configure_remotes()
        
        return True
    
    def configure_remotes(self):
        """配置远程仓库"""
        self.print_info("\n配置远程仓库...")
        
        print("\n请选择要配置的远程仓库：")
        print("1. GitHub")
        print("2. Gitea")
        print("3. 两者都配置")
        print("4. 跳过")
        
        choice = input("\n请选择 [1-4]: ").strip()
        
        if choice == '1':
            self.add_github_remote()
        elif choice == '2':
            self.add_gitea_remote()
        elif choice == '3':
            self.add_github_remote()
            self.add_gitea_remote()
        else:
            self.print_info("跳过远程仓库配置")
    
    def add_github_remote(self):
        """添加GitHub远程仓库"""
        repo_name = input(f"\n请输入GitHub仓库名: ").strip()
        if not repo_name:
            self.print_warning("仓库名不能为空，跳过GitHub配置")
            return
        
        remote_url = f"git@github.com:{self.github_user}/{repo_name}.git"
        
        # 检查remote是否已存在
        success, output = self.run_command("git remote", show_output=False)
        if "github" in output:
            self.run_command("git remote remove github", show_output=False)
        
        success, _ = self.run_command(f'git remote add github {remote_url}', show_output=False)
        if success:
            self.print_success(f"GitHub远程仓库已添加: {remote_url}")
        else:
            self.print_error("GitHub远程仓库添加失败")
    
    def add_gitea_remote(self):
        """添加Gitea远程仓库"""
        user = input(f"\n请输入Gitea用户名: ").strip()
        if not user:
            self.print_warning("用户名不能为空，跳过Gitea配置")
            return
        
        repo_name = input(f"请输入Gitea仓库名: ").strip()
        if not repo_name:
            self.print_warning("仓库名不能为空，跳过Gitea配置")
            return
        
        remote_url = f"ssh://git@{self.gitea_host}:{self.gitea_port}/{user}/{repo_name}.git"
        
        # 检查remote是否已存在
        success, output = self.run_command("git remote", show_output=False)
        if "gitea" in output:
            self.run_command("git remote remove gitea", show_output=False)
        
        success, _ = self.run_command(f'git remote add gitea {remote_url}', show_output=False)
        if success:
            self.print_success(f"Gitea远程仓库已添加: {remote_url}")
        else:
            self.print_error("Gitea远程仓库添加失败")
    
    def commit_and_push(self):
        """提交并推送更改"""
        self.print_header("提交并推送更改")
        
        if not self.is_git_repo():
            self.print_error("当前目录不是Git仓库，请先初始化")
            return False
        
        # 1. 检查是否有更改
        self.print_info("检查文件更改...")
        success, output = self.run_command("git status --short", show_output=False)
        
        if not output.strip():
            self.print_warning("没有文件更改，无需提交")
            return True
        
        print("\n当前更改的文件：")
        print(output)
        
        # 2. 输入提交信息
        commit_msg = input("\n请输入提交信息 (直接回车使用默认信息): ").strip()
        if not commit_msg:
            from datetime import datetime
            commit_msg = f"update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # 3. 添加所有更改
        self.print_info("正在添加文件...")
        success, _ = self.run_command("git add .", show_output=False)
        if not success:
            self.print_error("添加文件失败")
            return False
        self.print_success("文件添加成功")
        
        # 4. 提交更改
        self.print_info("正在提交更改...")
        success, _ = self.run_command(f'git commit -m "{commit_msg}"', show_output=True)
        if not success:
            self.print_error("提交失败")
            return False
        self.print_success("提交成功")
        
        # 5. 推送到远程仓库
        self.push_to_remote()
        
        return True
    
    def push_to_remote(self):
        """推送到远程仓库"""
        # 获取当前分支
        success, branch = self.run_command("git branch --show-current", show_output=False)
        if not success or not branch.strip():
            branch = "main"
        else:
            branch = branch.strip()
        
        # 获取所有远程仓库
        success, output = self.run_command("git remote", show_output=False)
        if not success or not output.strip():
            self.print_warning("没有配置远程仓库")
            return
        
        remotes = [r.strip() for r in output.strip().split('\n') if r.strip()]
        
        if not remotes:
            self.print_warning("没有配置远程仓库")
            return
        
        print("\n可用的远程仓库：")
        for idx, remote in enumerate(remotes, 1):
            print(f"{idx}. {remote}")
        print(f"{len(remotes) + 1}. 全部推送")
        
        choice = input(f"\n请选择要推送的远程仓库 [1-{len(remotes) + 1}]: ").strip()
        
        try:
            choice_idx = int(choice)
            if choice_idx == len(remotes) + 1:
                # 推送到所有远程仓库
                for remote in remotes:
                    self.push_to_specific_remote(remote, branch)
            elif 1 <= choice_idx <= len(remotes):
                # 推送到指定远程仓库
                remote = remotes[choice_idx - 1]
                self.push_to_specific_remote(remote, branch)
            else:
                self.print_error("无效的选择")
        except ValueError:
            self.print_error("无效的输入")
    
    def push_to_specific_remote(self, remote: str, branch: str):
        """推送到指定远程仓库"""
        self.print_info(f"正在推送到 {remote}...")
        
        # 检查是否需要设置上游分支
        success, _ = self.run_command(f"git push {remote} {branch}", show_output=True)
        
        if not success:
            # 尝试设置上游分支
            self.print_info(f"尝试设置上游分支...")
            success, _ = self.run_command(f"git push -u {remote} {branch}", show_output=True)
        
        if success:
            self.print_success(f"成功推送到 {remote}")
        else:
            self.print_error(f"推送到 {remote} 失败")
    
    def pull_from_remote(self):
        """从远程仓库拉取"""
        self.print_header("从远程仓库拉取")
        
        if not self.is_git_repo():
            self.print_error("当前目录不是Git仓库")
            return False
        
        # 获取所有远程仓库
        success, output = self.run_command("git remote", show_output=False)
        if not success or not output.strip():
            self.print_warning("没有配置远程仓库")
            return False
        
        remotes = [r.strip() for r in output.strip().split('\n') if r.strip()]
        
        if not remotes:
            self.print_warning("没有配置远程仓库")
            return False
        
        print("\n可用的远程仓库：")
        for idx, remote in enumerate(remotes, 1):
            print(f"{idx}. {remote}")
        
        choice = input(f"\n请选择要拉取的远程仓库 [1-{len(remotes)}]: ").strip()
        
        try:
            choice_idx = int(choice)
            if 1 <= choice_idx <= len(remotes):
                remote = remotes[choice_idx - 1]
                
                # 获取当前分支
                success, branch = self.run_command("git branch --show-current", show_output=False)
                if not success or not branch.strip():
                    branch = "main"
                else:
                    branch = branch.strip()
                
                self.print_info(f"正在从 {remote} 拉取 {branch} 分支...")
                success, _ = self.run_command(f"git pull {remote} {branch}", show_output=True)
                
                if success:
                    self.print_success(f"成功从 {remote} 拉取更新")
                else:
                    self.print_error(f"从 {remote} 拉取失败")
            else:
                self.print_error("无效的选择")
        except ValueError:
            self.print_error("无效的输入")
    
    def show_status(self):
        """显示仓库状态"""
        self.print_header("仓库状态")
        
        if not self.is_git_repo():
            self.print_error("当前目录不是Git仓库")
            return
        
        print(f"{Colors.CYAN}当前目录:{Colors.ENDC} {self.current_dir}\n")
        
        # Git状态
        self.print_info("Git状态：")
        self.run_command("git status", show_output=True)
        
        # 远程仓库
        print(f"\n{Colors.CYAN}远程仓库：{Colors.ENDC}")
        self.run_command("git remote -v", show_output=True)
        
        # 最近提交
        print(f"\n{Colors.CYAN}最近3次提交：{Colors.ENDC}")
        self.run_command("git log --oneline -3", show_output=True)
    
    def manage_remotes(self):
        """管理远程仓库"""
        self.print_header("管理远程仓库")
        
        if not self.is_git_repo():
            self.print_error("当前目录不是Git仓库")
            return
        
        while True:
            print("\n远程仓库管理：")
            print("1. 查看远程仓库")
            print("2. 添加GitHub远程仓库")
            print("3. 添加Gitea远程仓库")
            print("4. 删除远程仓库")
            print("5. 返回主菜单")
            
            choice = input("\n请选择 [1-5]: ").strip()
            
            if choice == '1':
                print(f"\n{Colors.CYAN}当前远程仓库：{Colors.ENDC}")
                self.run_command("git remote -v", show_output=True)
            elif choice == '2':
                self.add_github_remote()
            elif choice == '3':
                self.add_gitea_remote()
            elif choice == '4':
                self.remove_remote()
            elif choice == '5':
                break
            else:
                self.print_error("无效的选择")
    
    def remove_remote(self):
        """删除远程仓库"""
        success, output = self.run_command("git remote", show_output=False)
        if not success or not output.strip():
            self.print_warning("没有配置远程仓库")
            return
        
        remotes = [r.strip() for r in output.strip().split('\n') if r.strip()]
        
        if not remotes:
            self.print_warning("没有配置远程仓库")
            return
        
        print("\n当前远程仓库：")
        for idx, remote in enumerate(remotes, 1):
            print(f"{idx}. {remote}")
        
        choice = input(f"\n请选择要删除的远程仓库 [1-{len(remotes)}]: ").strip()
        
        try:
            choice_idx = int(choice)
            if 1 <= choice_idx <= len(remotes):
                remote = remotes[choice_idx - 1]
                confirm = input(f"确认删除远程仓库 '{remote}'? [y/N]: ").strip().lower()
                if confirm == 'y':
                    success, _ = self.run_command(f"git remote remove {remote}", show_output=False)
                    if success:
                        self.print_success(f"远程仓库 '{remote}' 已删除")
                    else:
                        self.print_error("删除失败")
            else:
                self.print_error("无效的选择")
        except ValueError:
            self.print_error("无效的输入")
    
    def run(self):
        """运行主程序"""
        self.print_header("萌芽一键Git管理工具")
        print(f"{Colors.CYAN}当前目录:{Colors.ENDC} {self.current_dir}")
        print(f"{Colors.CYAN}Git仓库:{Colors.ENDC} {'是' if self.is_git_repo() else '否'}")
        
        while True:
            print(f"\n{Colors.BOLD}请选择操作：{Colors.ENDC}")
            print("1. 初始化Git仓库")
            print("2. 提交并推送更改")
            print("3. 从远程仓库拉取")
            print("4. 查看仓库状态")
            print("5. 管理远程仓库")
            print("6. 退出")
            
            choice = input(f"\n{Colors.BOLD}请输入选项 [1-6]: {Colors.ENDC}").strip()
            
            if choice == '1':
                self.init_git_repo()
            elif choice == '2':
                self.commit_and_push()
            elif choice == '3':
                self.pull_from_remote()
            elif choice == '4':
                self.show_status()
            elif choice == '5':
                self.manage_remotes()
            elif choice == '6':
                self.print_success("感谢使用萌芽Git管理工具！")
                break
            else:
                self.print_error("无效的选择，请重新输入")


def main():
    """主函数"""
    try:
        manager = GitManager()
        manager.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}程序被用户中断{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}发生错误: {str(e)}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
