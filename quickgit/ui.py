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
        OutputFormatter.header("萌芽一键Git管理工具 - QuickGit")
        print(f"{Colors.CYAN}当前目录:{Colors.ENDC} {self.git_ops.current_dir}")
        print(f"{Colors.CYAN}Git仓库:{Colors.ENDC} {'是' if self.git_ops.is_git_repo() else '否'}")
    
    def show_main_menu(self):
        """显示主菜单"""
        print(f"\n{Colors.BOLD}请选择操作：{Colors.ENDC}")
        print("1. 初始化Git仓库")
        print("2. 提交并推送更改")
        print("3. 从远程仓库拉取")
        print("4. 查看仓库状态")
        print("5. 管理远程仓库")
        print("6. 退出")
    
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
        
        # 检查是否有更改
        OutputFormatter.info("检查文件更改...")
        
        if not self.git_ops.has_changes():
            OutputFormatter.warning("没有文件更改，无需提交")
            return
        
        # 显示更改
        print("\n当前更改的文件：")
        _, status = self.git_ops.get_status()
        print(status)
        
        # 输入提交信息
        commit_msg = InputValidator.get_input(
            "\n请输入提交信息 (直接回车使用默认信息): ",
            allow_empty=True
        )
        
        # 添加并提交
        if not self.git_ops.add_all():
            return
        
        if not self.git_ops.commit(commit_msg if commit_msg else None):
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
            print("\n远程仓库管理：")
            print("1. 查看远程仓库")
            print("2. 添加GitHub远程仓库")
            print("3. 添加Gitea远程仓库")
            print("4. 删除远程仓库")
            print("5. 返回主菜单")
            
            choice = InputValidator.get_choice("\n请选择 [1-5]: ", range(1, 6))
            
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
                f"\n{Colors.BOLD}请输入选项 [1-6]: {Colors.ENDC}",
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
                OutputFormatter.success("感谢使用萌芽Git管理工具！")
                break
