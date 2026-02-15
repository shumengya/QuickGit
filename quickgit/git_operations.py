"""
Git操作模块 - 提供Git基本操作功能
"""

import os
from datetime import datetime
from .utils import CommandExecutor, OutputFormatter
from .config import Config


class GitOperations:
    """Git操作类"""
    
    def __init__(self, work_dir: str = ""):
        """
        初始化Git操作类
        
        Args:
            work_dir: 工作目录（默认为当前目录）
        """
        self.executor = CommandExecutor()
        if work_dir:
            self.current_dir = work_dir
        else:
            self.current_dir = os.getcwd()
    
    def change_directory(self, new_dir: str):
        """
        切换工作目录
        
        Args:
            new_dir: 新的工作目录
        """
        if os.path.isdir(new_dir):
            self.current_dir = os.path.abspath(new_dir)
            os.chdir(self.current_dir)
        else:
            raise ValueError(f"目录不存在: {new_dir}")
    
    def is_git_repo(self) -> bool:
        """检查当前目录是否是Git仓库"""
        git_dir = os.path.join(self.current_dir, '.git')
        return os.path.isdir(git_dir)
    
    def init_repo(self) -> bool:
        """
        初始化Git仓库
        
        Returns:
            是否成功
        """
        from .utils import Colors
        
        if self.is_git_repo():
            OutputFormatter.warning("当前目录已经是Git仓库")
            return True
        
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        # 初始化Git仓库
        OutputFormatter.step(1, "初始化Git仓库...")
        success, _ = self.executor.run("git init", show_output=False)
        if not success:
            OutputFormatter.error("Git初始化失败")
            return False
        OutputFormatter.success("Git仓库初始化成功")
        
        # 创建main分支
        OutputFormatter.step(2, "创建main分支...")
        success, _ = self.executor.run(f"git checkout -b {Config.DEFAULT_BRANCH}", show_output=False)
        if success:
            OutputFormatter.success("main分支创建成功")
        else:
            OutputFormatter.warning("main分支创建失败，将使用默认分支")
        
        # 创建.gitignore文件
        OutputFormatter.step(3, "创建.gitignore文件...")
        self._create_gitignore()
        
        # 首次提交
        OutputFormatter.step(4, "进行首次提交...")
        self.executor.run("git add .", show_output=False)
        success, _ = self.executor.run('git commit -m "first commit"', show_output=False)
        if success:
            OutputFormatter.success("首次提交完成")
        else:
            OutputFormatter.warning("首次提交失败（可能没有文件可提交）")
        
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        return True
    
    def _create_gitignore(self):
        """创建.gitignore文件"""
        try:
            with open('.gitignore', 'w', encoding='utf-8') as f:
                f.write(Config.GITIGNORE_TEMPLATE)
            OutputFormatter.success(".gitignore文件创建成功")
        except Exception as e:
            OutputFormatter.error(f".gitignore文件创建失败: {str(e)}")
    
    def get_status(self) -> tuple[bool, str]:
        """
        获取Git状态
        
        Returns:
            (是否成功, 状态输出)
        """
        return self.executor.run("git status --short", show_output=False)
    
    def has_changes(self) -> bool:
        """
        检查是否有更改
        
        Returns:
            是否有更改
        """
        success, output = self.get_status()
        return success and bool(output.strip())
    
    def add_all(self) -> bool:
        """
        添加所有更改
        
        Returns:
            是否成功
        """
        OutputFormatter.info("正在添加文件...")
        success, _ = self.executor.run("git add .", show_output=False)
        if success:
            OutputFormatter.success("文件添加成功")
        else:
            OutputFormatter.error("添加文件失败")
        return success
    
    def commit(self, message: str) -> bool:
        """
        提交更改
        
        Args:
            message: 提交信息
            
        Returns:
            是否成功
        """
        if not message:
            message = f"update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        OutputFormatter.status('running', f"提交更改: {message}")
        success, _ = self.executor.run(f'git commit -m "{message}"', show_output=True)
        if success:
            OutputFormatter.success("提交成功")
        else:
            OutputFormatter.error("提交失败")
        return success
    
    def get_current_branch(self) -> str:
        """
        获取当前分支
        
        Returns:
            分支名
        """
        success, branch = self.executor.run("git branch --show-current", show_output=False)
        if success and branch.strip():
            return branch.strip()
        return Config.DEFAULT_BRANCH
    
    def push(self, remote: str, branch: str = "") -> bool:
        """
        推送到远程仓库
        
        Args:
            remote: 远程仓库名
            branch: 分支名（默认为当前分支）
            
        Returns:
            是否成功
        """
        if not branch:
            branch = self.get_current_branch()
        
        OutputFormatter.status('running', f"推送到 {remote}/{branch}...")
        
        # 先尝试直接推送
        success, _ = self.executor.run(f"git push {remote} {branch}", show_output=True)
        
        if not success:
            # 如果失败，尝试设置上游分支
            OutputFormatter.info("尝试设置上游分支...")
            success, _ = self.executor.run(f"git push -u {remote} {branch}", show_output=True)
        
        if success:
            OutputFormatter.success(f"成功推送到 {remote}")
        else:
            OutputFormatter.error(f"推送到 {remote} 失败")
        
        return success
    
    def pull(self, remote: str, branch: str = "") -> bool:
        """
        从远程仓库拉取
        
        Args:
            remote: 远程仓库名
            branch: 分支名（默认为当前分支）
            
        Returns:
            是否成功
        """
        if not branch:
            branch = self.get_current_branch()
        
        OutputFormatter.status('running', f"从 {remote}/{branch} 拉取更新...")
        success, _ = self.executor.run(f"git pull {remote} {branch}", show_output=True)
        
        if success:
            OutputFormatter.success(f"成功从 {remote} 拉取更新")
        else:
            OutputFormatter.error(f"从 {remote} 拉取失败")
        
        return success
    
    def show_status(self):
        """显示仓库状态"""
        from .utils import Colors
        
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        OutputFormatter.key_value(">> 当前目录", self.current_dir, Colors.BRIGHT_YELLOW)
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
        
        # Git状态
        print(f"{Colors.BRIGHT_BLUE}>> Git状态：{Colors.ENDC}")
        self.executor.run("git status", show_output=True)
        
        # 最近提交
        print(f"\n{Colors.BRIGHT_MAGENTA}>> 最近3次提交：{Colors.ENDC}")
        self.executor.run("git log --oneline -3", show_output=True)
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
