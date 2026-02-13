"""
工具类模块 - 提供命令执行、输出格式化等工具函数
"""

import subprocess


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


class CommandExecutor:
    """命令执行器"""
    
    @staticmethod
    def run(command: str, show_output: bool = True) -> tuple[bool, str]:
        """
        执行命令
        
        Args:
            command: 要执行的命令
            show_output: 是否显示输出
            
        Returns:
            (是否成功, 输出内容)
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
            OutputFormatter.error(f"命令执行失败: {str(e)}")
            return False, str(e)


class OutputFormatter:
    """输出格式化器"""
    
    @staticmethod
    def header(text: str):
        """打印标题"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*50}")
        print(f"  {text}")
        print(f"{'='*50}{Colors.ENDC}\n")
    
    @staticmethod
    def success(text: str):
        """打印成功信息"""
        print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")
    
    @staticmethod
    def error(text: str):
        """打印错误信息"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")
    
    @staticmethod
    def info(text: str):
        """打印提示信息"""
        print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")
    
    @staticmethod
    def warning(text: str):
        """打印警告信息"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


class InputValidator:
    """输入验证器"""
    
    @staticmethod
    def get_choice(prompt: str, valid_range: range) -> int:
        """
        获取用户选择（数字）
        
        Args:
            prompt: 提示信息
            valid_range: 有效范围
            
        Returns:
            用户选择的数字
        """
        while True:
            try:
                choice = input(prompt).strip()
                choice_num = int(choice)
                if choice_num in valid_range:
                    return choice_num
                else:
                    OutputFormatter.error(f"请输入 {valid_range.start}-{valid_range.stop-1} 之间的数字")
            except ValueError:
                OutputFormatter.error("请输入有效的数字")
    
    @staticmethod
    def get_input(prompt: str, allow_empty: bool = False) -> str:
        """
        获取用户输入
        
        Args:
            prompt: 提示信息
            allow_empty: 是否允许空输入
            
        Returns:
            用户输入的字符串
        """
        while True:
            user_input = input(prompt).strip()
            if user_input or allow_empty:
                return user_input
            else:
                OutputFormatter.error("输入不能为空")
    
    @staticmethod
    def confirm(prompt: str, default: bool = False) -> bool:
        """
        获取用户确认
        
        Args:
            prompt: 提示信息
            default: 默认值
            
        Returns:
            用户确认结果
        """
        suffix = " [Y/n]: " if default else " [y/N]: "
        user_input = input(prompt + suffix).strip().lower()
        
        if not user_input:
            return default
        
        return user_input in ['y', 'yes']
