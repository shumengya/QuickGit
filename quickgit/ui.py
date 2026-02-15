"""
UI交互模块 - 处理用户界面和交互逻辑
"""

from .git_operations import GitOperations
from .remote_manager import RemoteManager
from .utils import OutputFormatter, InputValidator, Colors


class GitManagerUI:
    """Git管理器UI"""
    
    def __init__(self):
        self.git_ops = GitOperations()
        self.remote_mgr = RemoteManager()
    
    def show_welcome(self):
        """显示欢迎信息"""
        from .utils import Colors
        
        # 简洁的标题
        print(f"\n{Colors.BRIGHT_CYAN}{'=' * 60}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}   QuickGit - 萌芽一键Git管理工具 v1.0{Colors.ENDC}")
        print(f"{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.ENDC}")
        
        # 显示当前状态
        is_repo = self.git_ops.is_git_repo()
        repo_status = f"{Colors.BRIGHT_GREEN}[已初始化]{Colors.ENDC}" if is_repo else f"{Colors.BRIGHT_RED}[未初始化]{Colors.ENDC}"
        
        print(f"{Colors.BRIGHT_YELLOW}当前目录:{Colors.ENDC} {Colors.WHITE}{self.git_ops.current_dir}{Colors.ENDC}")
        print(f"{Colors.BRIGHT_YELLOW}Git状态:{Colors.ENDC} {repo_status}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
    
    def show_main_menu(self):
        """显示主菜单"""
        print(f"\n{Colors.BRIGHT_MAGENTA}{Colors.BOLD}>> 主菜单{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        OutputFormatter.menu_item(1, "初始化Git仓库")
        OutputFormatter.menu_item(2, "提交并推送更改")
        OutputFormatter.menu_item(3, "从远程仓库拉取")
        OutputFormatter.menu_item(4, "查看仓库状态")
        OutputFormatter.menu_item(5, "管理远程仓库")
        OutputFormatter.menu_item(6, "退出程序")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
    
    def handle_init_repo(self):
        """处理初始化仓库"""
        OutputFormatter.header("初始化Git仓库")
        
        if self.git_ops.init_repo():
            # 配置远程仓库
            self.remote_mgr.configure_remotes_interactive()
    
    def handle_commit_and_push(self):
        """处理提交并推送"""
        OutputFormatter.header("提交并推送更改")
        
        if not self.git_ops.is_git_repo():
            OutputFormatter.error("当前目录不是Git仓库，请先初始化")
            return
        
        # 提示：先拉取再提交
        OutputFormatter.tip("建议先拉取最新代码再提交，减少代码冲突")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        # 检查是否有更改
        OutputFormatter.status('running', "检查文件更改中...")
        
        if not self.git_ops.has_changes():
            OutputFormatter.warning("没有文件更改，无需提交")
            return
        
        # 显示更改
        print(f"\n{Colors.BRIGHT_YELLOW}>> 当前更改的文件：{Colors.ENDC}")
        _, status = self.git_ops.get_status()
        print(f"{Colors.CYAN}{status}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        # 输入提交信息
        commit_msg = InputValidator.get_input(
            f"{Colors.BRIGHT_CYAN}>> 请输入提交信息 (回车使用默认): {Colors.ENDC}",
            allow_empty=True
        )
        
        # 添加并提交
        if not self.git_ops.add_all():
            return
        
        if not self.git_ops.commit(commit_msg or ""):
            return
        
        # 推送到远程仓库
        selected_remotes = self.remote_mgr.select_remote_for_push()
        
        for remote in selected_remotes:
            self.git_ops.push(remote)
    
    def handle_pull(self):
        """处理拉取"""
        OutputFormatter.header("从远程仓库拉取")
        
        if not self.git_ops.is_git_repo():
            OutputFormatter.error("当前目录不是Git仓库")
            return
        
        remote = self.remote_mgr.select_remote_for_pull()
        if remote:
            self.git_ops.pull(remote)
    
    def handle_show_status(self):
        """处理显示状态"""
        OutputFormatter.header("仓库状态")
        
        if not self.git_ops.is_git_repo():
            OutputFormatter.error("当前目录不是Git仓库")
            return
        
        self.git_ops.show_status()
        
        # 显示远程仓库
        self.remote_mgr.show_remotes()
    
    def handle_manage_remotes(self):
        """处理远程仓库管理"""
        OutputFormatter.header("管理远程仓库")
        
        if not self.git_ops.is_git_repo():
            OutputFormatter.error("当前目录不是Git仓库")
            return
        
        while True:
            print(f"\n{Colors.BRIGHT_BLUE}{Colors.BOLD}>> 远程仓库管理{Colors.ENDC}")
            print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
            
            OutputFormatter.menu_item(1, "查看远程仓库")
            OutputFormatter.menu_item(2, "添加GitHub远程仓库")
            OutputFormatter.menu_item(3, "添加Gitea远程仓库")
            OutputFormatter.menu_item(4, "删除远程仓库")
            OutputFormatter.menu_item(5, "返回主菜单")
            print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
            
            choice = InputValidator.get_choice(
                f"{Colors.BRIGHT_CYAN}>> 请选择 [1-5]: {Colors.ENDC}",
                range(1, 6)
            )
            
            if choice == 1:
                self.remote_mgr.show_remotes()
            elif choice == 2:
                self.remote_mgr.add_github_remote()
            elif choice == 3:
                self.remote_mgr.add_gitea_remote()
            elif choice == 4:
                self.remote_mgr.remove_remote()
            elif choice == 5:
                break
    
    def run(self):
        """运行主程序"""
        self.show_welcome()
        
        while True:
            self.show_main_menu()
            
            choice = InputValidator.get_choice(
                f"{Colors.BRIGHT_MAGENTA}>> 请输入选项 [1-6]: {Colors.ENDC}",
                range(1, 7)
            )
            
            if choice == 1:
                self.handle_init_repo()
            elif choice == 2:
                self.handle_commit_and_push()
            elif choice == 3:
                self.handle_pull()
            elif choice == 4:
                self.handle_show_status()
            elif choice == 5:
                self.handle_manage_remotes()
            elif choice == 6:
                print(f"\n{Colors.BRIGHT_GREEN}{'=' * 60}")
                print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}   感谢使用QuickGit！祝您工作愉快！{Colors.ENDC}")
                print(f"{Colors.BRIGHT_GREEN}{'=' * 60}{Colors.ENDC}\n")
                break
