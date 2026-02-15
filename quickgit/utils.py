"""
工具类模块 - 提供命令执行、输出格式化等工具函数
"""

import os
import subprocess
import sys


class Colors:
    """控制台颜色"""
    # 基础颜色
    HEADER = '\033[95m'      # 紫色
    BLUE = '\033[94m'        # 蓝色
    CYAN = '\033[96m'        # 青色
    GREEN = '\033[92m'       # 绿色
    YELLOW = '\033[93m'      # 黄色
    RED = '\033[91m'         # 红色
    MAGENTA = '\033[35m'     # 品红
    WHITE = '\033[97m'       # 白色
    
    # 亮色系
    BRIGHT_CYAN = '\033[96m\033[1m'    # 亮青色
    BRIGHT_GREEN = '\033[92m\033[1m'   # 亮绿色
    BRIGHT_YELLOW = '\033[93m\033[1m'  # 亮黄色
    BRIGHT_RED = '\033[91m\033[1m'     # 亮红色
    BRIGHT_BLUE = '\033[94m\033[1m'    # 亮蓝色
    BRIGHT_MAGENTA = '\033[95m\033[1m' # 亮品红
    
    # 背景色
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_RED = '\033[41m'
    BG_CYAN = '\033[46m'
    BG_MAGENTA = '\033[45m'
    
    # 样式
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[7m'
    ENDC = '\033[0m'
    
    # 兼容旧代码
    WARNING = '\033[93m'
    FAIL = '\033[91m'


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
        """打印标题 - 顶部大标题"""
        line = "=" * 60
        print(f"\n{Colors.BRIGHT_CYAN}{line}")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}>> {text}")
        print(f"{Colors.BRIGHT_CYAN}{line}{Colors.ENDC}")
    
    @staticmethod
    def section(text: str):
        """打印分节标题"""
        print(f"\n{Colors.BRIGHT_YELLOW}{'=' * 60}")
        print(f"{Colors.BRIGHT_BLUE}{Colors.BOLD}>> {text}")
        print(f"{Colors.BRIGHT_YELLOW}{'=' * 60}{Colors.ENDC}")
    
    @staticmethod
    def divider():
        """打印分割线"""
        print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
    
    @staticmethod
    def thin_divider():
        """打印细分割线"""
        print(f"{Colors.CYAN}{'·' * 60}{Colors.ENDC}")
    
    @staticmethod
    def success(text: str):
        """打印成功信息"""
        print(f"{Colors.BRIGHT_GREEN}[√]{Colors.ENDC} {Colors.GREEN}{text}{Colors.ENDC}")
    
    @staticmethod
    def error(text: str):
        """打印错误信息"""
        print(f"{Colors.BRIGHT_RED}[×]{Colors.ENDC} {Colors.RED}{text}{Colors.ENDC}")
    
    @staticmethod
    def info(text: str):
        """打印提示信息"""
        print(f"{Colors.BRIGHT_CYAN}[i]{Colors.ENDC} {Colors.CYAN}{text}{Colors.ENDC}")
    
    @staticmethod
    def warning(text: str):
        """打印警告信息"""
        print(f"{Colors.BRIGHT_YELLOW}[!]{Colors.ENDC} {Colors.YELLOW}{text}{Colors.ENDC}")
    
    @staticmethod
    def tip(text: str):
        """打印提示信息"""
        print(f"{Colors.BRIGHT_CYAN}[*]{Colors.ENDC} {Colors.CYAN}{text}{Colors.ENDC}")
    
    @staticmethod
    def step(num: int, text: str):
        """打印步骤信息"""
        print(f"{Colors.BRIGHT_BLUE}[{num}]{Colors.ENDC} {Colors.WHITE}{text}{Colors.ENDC}")
    
    @staticmethod
    def menu_item(num: int, text: str, icon: str = ">>"):
        """打印菜单项"""
        print(f"{Colors.BRIGHT_CYAN}[{num}]{Colors.ENDC} {Colors.WHITE}{text}{Colors.ENDC}")
    
    @staticmethod
    def key_value(key: str, value: str, key_color=None, value_color=None):
        """打印键值对"""
        if key_color is None:
            key_color = Colors.BRIGHT_CYAN
        if value_color is None:
            value_color = Colors.WHITE
        print(f"{key_color}{key}:{Colors.ENDC} {value_color}{value}{Colors.ENDC}")
    
    @staticmethod
    def status(status_type: str, text: str):
        """打印状态信息"""
        icons = {
            'pending': f"{Colors.YELLOW}[·]{Colors.ENDC}",
            'running': f"{Colors.BRIGHT_CYAN}[>]{Colors.ENDC}",
            'success': f"{Colors.BRIGHT_GREEN}[√]{Colors.ENDC}",
            'error': f"{Colors.BRIGHT_RED}[×]{Colors.ENDC}",
        }
        icon = icons.get(status_type, "[·]")
        print(f"{icon} {text}")


class PlatformUtils:
    """跨平台工具类"""
    
    @staticmethod
    def clear_screen():
        """清屏 - 跨平台兼容"""
        # Windows
        if os.name == 'nt':
            os.system('cls')
        # Linux/macOS
        else:
            os.system('clear')
    
    @staticmethod
    def is_windows() -> bool:
        """检查是否为 Windows 系统"""
        return os.name == 'nt'
    
    @staticmethod
    def is_linux() -> bool:
        """检查是否为 Linux 系统"""
        return sys.platform.startswith('linux')
    
    @staticmethod
    def is_mac() -> bool:
        """检查是否为 macOS 系统"""
        return sys.platform == 'darwin'
    
    @staticmethod
    def get_platform_name() -> str:
        """获取平台名称"""
        if PlatformUtils.is_windows():
            return "Windows"
        elif PlatformUtils.is_linux():
            return "Linux"
        elif PlatformUtils.is_mac():
            return "macOS"
        else:
            return "Unknown"


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
