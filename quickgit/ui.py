"""
UI交互模块 - 处理用户界面和交互逻辑
"""

import os
from .git_operations import GitOperations
from .remote_manager import RemoteManager
from .utils import OutputFormatter, InputValidator, Colors, PlatformUtils


class GitManagerUI:
    """Git管理器UI"""
    
    def __init__(self, work_dir: str = ""):
        """
        初始化UI
        
        Args:
            work_dir: 工作目录（默认为当前目录）
        """
        self.git_ops = GitOperations(work_dir)
        self.remote_mgr = RemoteManager()
    
    def select_work_directory(self):
        """让用户选择工作目录"""
        from .utils import Colors
        
        print(f"\n{Colors.BRIGHT_CYAN}{'=' * 60}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}   QuickGit - 萌芽一键Git管理工具 v1.0{Colors.ENDC}")
        print(f"{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.ENDC}")
        
        # 获取当前目录
        current_dir = os.getcwd()
        
        # 显示平台信息和路径示例
        platform = PlatformUtils.get_platform_name()
        print(f"{Colors.BRIGHT_YELLOW}当前平台:{Colors.ENDC} {Colors.WHITE}{platform}{Colors.ENDC}")
        print(f"{Colors.BRIGHT_YELLOW}脚本目录:{Colors.ENDC} {Colors.WHITE}{current_dir}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        # 显示路径输入提示
        OutputFormatter.info("请输入要管理的Git仓库目录")
        
        # 根据平台显示不同的示例
        if PlatformUtils.is_windows():
            OutputFormatter.tip("Windows路径示例: C:\\Users\\YourName\\project")
            OutputFormatter.tip("或使用相对路径: .\\myproject")
        else:
            OutputFormatter.tip("Linux/macOS路径示例: /home/yourname/project")
            OutputFormatter.tip("或使用相对路径: ./myproject 或 ~/project")
        
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        # 获取用户输入的目录
        work_dir = InputValidator.get_directory(
            f"{Colors.BRIGHT_CYAN}>> 请输入目录路径{Colors.ENDC}",
            default=current_dir
        )
        
        # 切换到工作目录
        try:
            self.git_ops.change_directory(work_dir)
            OutputFormatter.success(f"已切换到工作目录: {work_dir}")
        except Exception as e:
            OutputFormatter.error(f"切换目录失败: {str(e)}")
            return False
        
        return True
    
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
        OutputFormatter.menu_item(2, "提交更改到本地")
        OutputFormatter.menu_item(3, "推送到远程仓库")
        OutputFormatter.menu_item(4, "从远程仓库拉取")
        OutputFormatter.menu_item(5, "查看仓库状态")
        OutputFormatter.menu_item(6, "管理远程仓库")
        OutputFormatter.menu_item(7, "退出程序")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        # 显示永久提示
        OutputFormatter.tip("提交代码前建议先拉取最新代码，减少代码冲突")
        OutputFormatter.tip("使用SSH进行Git提交更方便快捷和安全")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
    
    def handle_init_repo(self):
        """处理初始化仓库"""
        OutputFormatter.header("初始化Git仓库")
        
        if self.git_ops.init_repo():
            # 配置远程仓库
            self.remote_mgr.configure_remotes_interactive()
    
    def handle_commit(self):
        """处理提交到本地"""
        OutputFormatter.header("提交更改到本地")
        
        if not self.git_ops.is_git_repo():
            OutputFormatter.error("当前目录不是Git仓库，请先初始化")
            return
        
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
        
        OutputFormatter.tip("提交成功！如需推送到远程仓库，请选择菜单选项3")
    
    def handle_push(self):
        """处理推送到远程"""
        OutputFormatter.header("推送到远程仓库")
        
        if not self.git_ops.is_git_repo():
            OutputFormatter.error("当前目录不是Git仓库，请先初始化")
            return
        
        # 检查是否有提交可推送
        OutputFormatter.status('running', "检查待推送的提交...")
        
        # 推送到远程仓库
        selected_remotes = self.remote_mgr.select_remote_for_push()
        
        if not selected_remotes:
            OutputFormatter.warning("未选择远程仓库")
            return
        
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
        # 首先选择工作目录
        if not self.select_work_directory():
            return
        
        # 显示欢迎信息
        self.show_welcome()
        
        while True:
            self.show_main_menu()
            
            choice = InputValidator.get_choice(
                f"{Colors.BRIGHT_MAGENTA}>> 请输入选项 [1-7]: {Colors.ENDC}",
                range(1, 8)
            )
            
            if choice == 1:
                self.handle_init_repo()
            elif choice == 2:
                self.handle_commit()
            elif choice == 3:
                self.handle_push()
            elif choice == 4:
                self.handle_pull()
            elif choice == 5:
                self.handle_show_status()
            elif choice == 6:
                self.handle_manage_remotes()
            elif choice == 7:
                print(f"\n{Colors.BRIGHT_GREEN}{'=' * 60}")
                print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}   感谢使用QuickGit！祝您工作愉快！{Colors.ENDC}")
                print(f"{Colors.BRIGHT_GREEN}{'=' * 60}{Colors.ENDC}\n")
                break
