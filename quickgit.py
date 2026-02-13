#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuickGit - 萌芽一键Git管理工具
主程序入口
"""

import sys
from quickgit.ui import GitManagerUI


def main():
    """主函数"""
    try:
        ui = GitManagerUI()
        ui.run()
    except KeyboardInterrupt:
        from quickgit.utils import Colors
        print(f"\n\n{Colors.WARNING}程序被用户中断{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        from quickgit.utils import Colors
        print(f"\n{Colors.FAIL}发生错误: {str(e)}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
