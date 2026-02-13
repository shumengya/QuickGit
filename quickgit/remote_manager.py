"""
远程仓库管理模块 - 处理GitHub和Gitea远程仓库的管理
"""

from .utils import CommandExecutor, OutputFormatter, InputValidator
from .config import Config


class RemoteManager:
    """远程仓库管理器"""
    
    def __init__(self):
        self.executor = CommandExecutor()
    
    def get_remotes(self) -> list[str]:
        """
        获取所有远程仓库
        
        Returns:
            远程仓库列表
        """
        success, output = self.executor.run("git remote", show_output=False)
        if success and output.strip():
            return [r.strip() for r in output.strip().split('\n') if r.strip()]
        return []
    
    def show_remotes(self):
        """显示所有远程仓库"""
        from .utils import Colors
        print(f"\n{Colors.CYAN}远程仓库：{Colors.ENDC}")
        self.executor.run("git remote -v", show_output=True)
    
    def add_github_remote(self, repo_name: str = None) -> bool:
        """
        添加GitHub远程仓库
        
        Args:
            repo_name: 仓库名（如果为None则提示用户输入）
            
        Returns:
            是否成功
        """
        if not repo_name:
            repo_name = InputValidator.get_input("\n请输入GitHub仓库名: ")
        
        remote_url = f"git@github.com:{Config.GITHUB_USER}/{repo_name}.git"
        
        return self._add_remote("github", remote_url)
    
    def add_gitea_remote(self, user: str = None, repo_name: str = None) -> bool:
        """
        添加Gitea远程仓库
        
        Args:
            user: Gitea用户名（如果为None则提示用户输入）
            repo_name: 仓库名（如果为None则提示用户输入）
            
        Returns:
            是否成功
        """
        if not user:
            user = InputValidator.get_input("\n请输入Gitea用户名: ")
        
        if not repo_name:
            repo_name = InputValidator.get_input("请输入Gitea仓库名: ")
        
        remote_url = f"ssh://git@{Config.GITEA_HOST}:{Config.GITEA_PORT}/{user}/{repo_name}.git"
        
        return self._add_remote("gitea", remote_url)
    
    def _add_remote(self, name: str, url: str) -> bool:
        """
        添加远程仓库
        
        Args:
            name: 远程仓库名称
            url: 远程仓库URL
            
        Returns:
            是否成功
        """
        # 检查remote是否已存在
        remotes = self.get_remotes()
        if name in remotes:
            if InputValidator.confirm(f"远程仓库 '{name}' 已存在，是否覆盖？", default=False):
                self.executor.run(f"git remote remove {name}", show_output=False)
            else:
                return False
        
        success, _ = self.executor.run(f'git remote add {name} {url}', show_output=False)
        if success:
            OutputFormatter.success(f"{name.capitalize()}远程仓库已添加: {url}")
        else:
            OutputFormatter.error(f"{name.capitalize()}远程仓库添加失败")
        
        return success
    
    def remove_remote(self, name: str = None) -> bool:
        """
        删除远程仓库
        
        Args:
            name: 远程仓库名（如果为None则提示用户选择）
            
        Returns:
            是否成功
        """
        remotes = self.get_remotes()
        
        if not remotes:
            OutputFormatter.warning("没有配置远程仓库")
            return False
        
        if not name:
            # 让用户选择要删除的远程仓库
            print("\n当前远程仓库：")
            for idx, remote in enumerate(remotes, 1):
                print(f"{idx}. {remote}")
            
            choice = InputValidator.get_choice(
                f"\n请选择要删除的远程仓库 [1-{len(remotes)}]: ",
                range(1, len(remotes) + 1)
            )
            
            name = remotes[choice - 1]
        
        if not InputValidator.confirm(f"确认删除远程仓库 '{name}'?", default=False):
            return False
        
        success, _ = self.executor.run(f"git remote remove {name}", show_output=False)
        if success:
            OutputFormatter.success(f"远程仓库 '{name}' 已删除")
        else:
            OutputFormatter.error("删除失败")
        
        return success
    
    def configure_remotes_interactive(self):
        """交互式配置远程仓库"""
        OutputFormatter.info("\n配置远程仓库...")
        
        print("\n请选择要配置的远程仓库：")
        print("1. GitHub")
        print("2. Gitea")
        print("3. 两者都配置")
        print("4. 跳过")
        
        choice = InputValidator.get_choice("\n请选择 [1-4]: ", range(1, 5))
        
        if choice == 1:
            self.add_github_remote()
        elif choice == 2:
            self.add_gitea_remote()
        elif choice == 3:
            self.add_github_remote()
            self.add_gitea_remote()
        else:
            OutputFormatter.info("跳过远程仓库配置")
    
    def select_remote_for_push(self) -> list[str]:
        """
        选择要推送的远程仓库
        
        Returns:
            选中的远程仓库列表
        """
        remotes = self.get_remotes()
        
        if not remotes:
            OutputFormatter.warning("没有配置远程仓库")
            return []
        
        print("\n可用的远程仓库：")
        for idx, remote in enumerate(remotes, 1):
            print(f"{idx}. {remote}")
        print(f"{len(remotes) + 1}. 全部推送")
        
        choice = InputValidator.get_choice(
            f"\n请选择要推送的远程仓库 [1-{len(remotes) + 1}]: ",
            range(1, len(remotes) + 2)
        )
        
        if choice == len(remotes) + 1:
            return remotes
        else:
            return [remotes[choice - 1]]
    
    def select_remote_for_pull(self) -> str:
        """
        选择要拉取的远程仓库
        
        Returns:
            选中的远程仓库名
        """
        remotes = self.get_remotes()
        
        if not remotes:
            OutputFormatter.warning("没有配置远程仓库")
            return None
        
        print("\n可用的远程仓库：")
        for idx, remote in enumerate(remotes, 1):
            print(f"{idx}. {remote}")
        
        choice = InputValidator.get_choice(
            f"\n请选择要拉取的远程仓库 [1-{len(remotes)}]: ",
            range(1, len(remotes) + 1)
        )
        
        return remotes[choice - 1]
