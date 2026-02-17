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
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        print(f"{Colors.BRIGHT_CYAN}>> 远程仓库列表：{Colors.ENDC}")
        self.executor.run("git remote -v", show_output=True)
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
    
    def add_github_remote(self, repo_name: str = "") -> bool:
        """
        添加GitHub远程仓库
        
        Args:
            repo_name: 仓库名（如果为空则提示用户输入）
            
        Returns:
            是否成功
        """
        if not repo_name:
            from .utils import Colors
            repo_name = InputValidator.get_input(f"{Colors.BRIGHT_CYAN}>> 请输入GitHub仓库名: {Colors.ENDC}")
        
        github_user = Config.get_github_user()
        remote_url = f"git@github.com:{github_user}/{repo_name}.git"
        
        return self._add_remote("github", remote_url)
    
    def add_gitea_remote(self, user: str = "", repo_name: str = "") -> bool:
        """
        添加Gitea远程仓库
        
        Args:
            user: Gitea用户名（如果为空则提示用户输入）
            repo_name: 仓库名（如果为空则提示用户输入）
            
        Returns:
            是否成功
        """
        from .utils import Colors
        if not user:
            user = InputValidator.get_input(f"{Colors.BRIGHT_CYAN}>> 请输入Gitea用户名: {Colors.ENDC}")
        
        if not repo_name:
            repo_name = InputValidator.get_input(f"{Colors.BRIGHT_CYAN}>> 请输入Gitea仓库名: {Colors.ENDC}")
        
        gitea_host = Config.get_gitea_host()
        gitea_port = Config.get_gitea_port()
        remote_url = f"ssh://git@{gitea_host}:{gitea_port}/{user}/{repo_name}.git"
        
        return self._add_remote("gitea", remote_url)
    
    def add_custom_remote(self) -> bool:
        """
        添加自建Git远程仓库
        
        Returns:
            是否成功
        """
        from .utils import Colors
        
        print(f"\n{Colors.BRIGHT_MAGENTA}>> 添加自建Git仓库{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        OutputFormatter.tip("支持 GitLab、自建Gitea、Gogs 等 Git 服务器")
        OutputFormatter.tip("SSH URL 格式示例:")
        print(f"{Colors.WHITE}  - git@gitlab.com:user/repo.git")
        print(f"{Colors.WHITE}  - ssh://git@your-server.com:port/user/repo.git{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        # 输入远程仓库名称
        remote_name = InputValidator.get_input(
            f"{Colors.BRIGHT_CYAN}>> 请输入远程仓库名称 (如: gitlab, mygit): {Colors.ENDC}"
        )
        
        # 检查是否已存在
        remotes = self.get_remotes()
        if remote_name in remotes:
            OutputFormatter.warning(f"远程仓库 '{remote_name}' 已存在")
            if not InputValidator.confirm("是否覆盖？", default=False):
                return False
            self.executor.run(f"git remote remove {remote_name}", show_output=False)
        
        # 输入SSH URL
        remote_url = InputValidator.get_input(
            f"{Colors.BRIGHT_CYAN}>> 请输入完整的SSH URL: {Colors.ENDC}"
        )
        
        # 验证URL格式
        if not (remote_url.startswith("git@") or remote_url.startswith("ssh://")):
            OutputFormatter.error("无效的SSH URL格式，必须以 'git@' 或 'ssh://' 开头")
            return False
        
        return self._add_remote(remote_name, remote_url)
    
    def configure_gitea_settings(self):
        """配置Gitea服务器设置"""
        from .utils import Colors
        
        print(f"\n{Colors.BRIGHT_MAGENTA}>> 配置Gitea服务器{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        # 显示当前配置
        current_host = Config.get_gitea_host()
        current_port = Config.get_gitea_port()
        
        OutputFormatter.info(f"当前配置:")
        print(f"{Colors.WHITE}  主机: {current_host}{Colors.ENDC}")
        print(f"{Colors.WHITE}  端口: {current_port}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        # 询问是否修改
        if not InputValidator.confirm("是否修改Gitea服务器配置？", default=False):
            return
        
        # 输入新的主机地址
        new_host = InputValidator.get_input(
            f"{Colors.BRIGHT_CYAN}>> 请输入Gitea主机地址 (回车保持 {current_host}): {Colors.ENDC}",
            allow_empty=True
        )
        
        if new_host:
            Config.set("gitea_host", new_host)
            OutputFormatter.success(f"Gitea主机地址已更新为: {new_host}")
        
        # 输入新的端口
        new_port = InputValidator.get_input(
            f"{Colors.BRIGHT_CYAN}>> 请输入SSH端口 (回车保持 {current_port}): {Colors.ENDC}",
            allow_empty=True
        )
        
        if new_port:
            Config.set("gitea_port", new_port)
            OutputFormatter.success(f"Gitea SSH端口已更新为: {new_port}")
        
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        OutputFormatter.tip("配置已保存，下次添加Gitea仓库时将使用新配置")
    
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
    
    def remove_remote(self, name: str = "") -> bool:
        """
        删除远程仓库
        
        Args:
            name: 远程仓库名（如果为空则提示用户选择）
            
        Returns:
            是否成功
        """
        from .utils import Colors
        remotes = self.get_remotes()
        
        if not remotes:
            OutputFormatter.warning("没有配置远程仓库")
            return False
        
        if not name:
            # 让用户选择要删除的远程仓库
            print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
            print(f"{Colors.BRIGHT_YELLOW}>> 当前远程仓库：{Colors.ENDC}")
            for idx, remote in enumerate(remotes, 1):
                OutputFormatter.menu_item(idx, remote)
            print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
            
            choice = InputValidator.get_choice(
                f"{Colors.BRIGHT_CYAN}>> 请选择要删除的远程仓库 [1-{len(remotes)}]: {Colors.ENDC}",
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
        from .utils import Colors
        print(f"\n{Colors.BRIGHT_MAGENTA}>> 配置远程仓库{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        OutputFormatter.menu_item(1, "GitHub")
        OutputFormatter.menu_item(2, "Gitea")
        OutputFormatter.menu_item(3, "自建Git仓库")
        OutputFormatter.menu_item(4, "跳过")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        choice = InputValidator.get_choice(
            f"{Colors.BRIGHT_CYAN}>> 请选择 [1-4]: {Colors.ENDC}",
            range(1, 5)
        )
        
        if choice == 1:
            self.add_github_remote()
        elif choice == 2:
            self.add_gitea_remote()
        elif choice == 3:
            self.add_custom_remote()
        else:
            OutputFormatter.info("跳过远程仓库配置")
    
    def select_remote_for_push(self) -> list[str]:
        """
        选择要推送的远程仓库
        
        Returns:
            选中的远程仓库列表
        """
        from .utils import Colors
        remotes = self.get_remotes()
        
        if not remotes:
            OutputFormatter.warning("没有配置远程仓库")
            return []
        
        print(f"\n{Colors.BRIGHT_YELLOW}>> 可用的远程仓库：{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        for idx, remote in enumerate(remotes, 1):
            OutputFormatter.menu_item(idx, remote)
        OutputFormatter.menu_item(len(remotes) + 1, "全部推送")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        choice = InputValidator.get_choice(
            f"{Colors.BRIGHT_CYAN}>> 请选择 [1-{len(remotes) + 1}]: {Colors.ENDC}",
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
            选中的远程仓库名，如果没有配置则返回空字符串
        """
        from .utils import Colors
        remotes = self.get_remotes()
        
        if not remotes:
            OutputFormatter.warning("没有配置远程仓库")
            return ""
        
        print(f"\n{Colors.BRIGHT_YELLOW}>> 可用的远程仓库：{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        for idx, remote in enumerate(remotes, 1):
            OutputFormatter.menu_item(idx, remote)
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        choice = InputValidator.get_choice(
            f"{Colors.BRIGHT_CYAN}>> 请选择 [1-{len(remotes)}]: {Colors.ENDC}",
            range(1, len(remotes) + 1)
        )
        
        return remotes[choice - 1]
        
        choice = InputValidator.get_choice(
            f"\n请选择要拉取的远程仓库 [1-{len(remotes)}]: ",
            range(1, len(remotes) + 1)
        )
        
        return remotes[choice - 1]
