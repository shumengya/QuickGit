# Agent Guidelines for QuickGit

This document provides coding agents with essential information about the QuickGit codebase, including build commands, code style, and architectural conventions.

---

## Project Overview

**QuickGit** is a modular CLI Git management tool written in Python 3.6+. It simplifies Git operations through an interactive menu system with colorful console output.

**Key Technologies:**
- Pure Python 3.6+ (no external dependencies)
- Standard library only: `subprocess`, `os`, `datetime`, `sys`
- Cross-platform support: Windows, Linux, macOS
- ANSI escape codes for colorful console output
- **SSH-only Git operations**: Supports GitHub and Gitea via SSH (no HTTPS support)

---

## Build, Run, and Test Commands

### Running the Application

```bash
# Recommended: Run the modular version
python quickgit.py        # Windows
python3 quickgit.py       # Linux/macOS

# Platform-specific launchers:
run.bat                   # Windows (sets UTF-8 encoding)
./run.sh                  # Linux/macOS (first run: chmod +x run.sh)

# Legacy: Run the single-file version
python mengya_git_manager.py
```

### Testing

**No formal test suite exists yet.** Manual testing workflow:

1. **Prerequisite: Configure SSH keys**
   ```bash
   # Generate SSH key if needed
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Test SSH connection
   ssh -T git@github.com
   ssh -T git@git.shumengya.top -p 8022
   ```

2. **Test in a clean directory:**
   ```bash
   cd /path/to/test/directory
   python E:\SmyProjects\Python\脚本\萌芽一键Git管理\quickgit.py
   ```

3. **Test each menu option:**
   - Option 1: Initialize Git repo
   - Option 2: Commit changes to local (requires changes)
   - Option 3: Push to remote (requires SSH-configured remote)
   - Option 4: Pull from remote (requires SSH-configured remote)
   - Option 5: View status
   - Option 6: Manage remotes (add GitHub/Gitea via SSH)
   - Option 7: Exit

4. **Verify console output:**
   - Check colors render correctly
   - Ensure ASCII dividers align (60 chars wide)
   - No encoding errors with Chinese characters

### Linting and Code Quality

```bash
# No formal linting configured yet
# Recommended tools for future use:
# pip install pylint black mypy

# Type checking (Python 3.10+ syntax used):
# mypy quickgit/

# Formatting:
# black quickgit/ --line-length 100

# Linting:
# pylint quickgit/
```

---

## Code Style Guidelines

### File Organization

**Module Structure:**
```
quickgit/
├── __init__.py          # Package init (empty)
├── config.py            # Configuration constants
├── utils.py             # Utilities (Colors, CommandExecutor, OutputFormatter, InputValidator, PlatformUtils)
├── git_operations.py    # Git command wrapper (supports custom work directory)
├── remote_manager.py    # Remote repository management
└── ui.py                # User interface and menu system
```

**Principle:** Each module has a single, well-defined responsibility.

### Key Features

1. **Flexible Directory Management**: Users can select any directory to manage at startup
2. **Cross-platform Path Handling**: Automatic path normalization for Windows/Linux/macOS
3. **Directory Validation**: Real-time validation of user-provided paths

### Import Conventions

**Order:**
1. Standard library imports
2. Relative imports from `quickgit` package

**Style:**
```python
# Standard library
import os
import sys
from datetime import datetime

# Internal modules (relative imports preferred)
from .utils import CommandExecutor, OutputFormatter, Colors
from .config import Config
```

**Lazy imports for circular dependency avoidance:**
```python
def some_function():
    from .utils import Colors  # Import inside function if needed
    print(f"{Colors.CYAN}Message{Colors.ENDC}")
```

### Type Hints

**Required for all function signatures:**

```python
# Good
def run(command: str, show_output: bool = True) -> tuple[bool, str]:
    """Execute command and return (success, output)"""
    pass

def get_remotes(self) -> list[str]:
    """Get all remote repositories"""
    pass

def confirm(prompt: str, default: bool = False) -> bool:
    """Get user confirmation"""
    pass
```

**Note:** Uses Python 3.10+ syntax (`list[str]`, `tuple[bool, str]`). For Python 3.6-3.9 compatibility, use:
```python
from typing import List, Tuple
def get_remotes(self) -> List[str]: ...
```

### Naming Conventions

- **Classes:** `PascalCase` (e.g., `GitOperations`, `RemoteManager`)
- **Functions/Methods:** `snake_case` (e.g., `add_github_remote`, `show_main_menu`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `DEFAULT_BRANCH`, `GITEA_HOST`)
- **Private methods:** Prefix with `_` (e.g., `_create_gitignore`, `_add_remote`)
- **Module-level:** Avoid global variables; use `Config` class for constants

### Formatting and Whitespace

- **Line length:** Aim for 100 characters max (not strictly enforced)
- **Indentation:** 4 spaces (no tabs)
- **Blank lines:** 2 between top-level definitions, 1 between methods
- **Strings:** Use double quotes `"` for user-facing text, either for code strings

### Error Handling

**Always provide user-friendly feedback:**

```python
# Good
try:
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(Config.GITIGNORE_TEMPLATE)
    OutputFormatter.success(".gitignore文件创建成功")
except Exception as e:
    OutputFormatter.error(f".gitignore文件创建失败: {str(e)}")
```

**Command execution pattern:**

```python
success, output = self.executor.run("git status", show_output=False)
if success:
    OutputFormatter.success("操作成功")
else:
    OutputFormatter.error("操作失败")
    return False
```

**Never swallow exceptions silently.** Always log errors via `OutputFormatter.error()`.

---

## Console Output Guidelines

### Critical Rules

1. **NO EMOJI CHARACTERS** - They cause Windows console encoding errors
2. **NO UNICODE BOX-DRAWING** (`┌─┐│└┘╔═╗║╚╝`) - They misalign across terminals
3. **Use ASCII only:** `=`, `-`, `·` for dividers
4. **Status indicators:** `[√]`, `[×]`, `[i]`, `[!]`, `[>]` instead of Unicode symbols
5. **Fixed width:** All dividers are exactly 60 characters wide

### Color Usage

**Color scheme:**
```python
Colors.BRIGHT_GREEN    # Success messages
Colors.BRIGHT_RED      # Errors
Colors.BRIGHT_CYAN     # Info/prompts
Colors.BRIGHT_YELLOW   # Warnings/section headers
Colors.BRIGHT_MAGENTA  # Main headers
Colors.WHITE           # General text
```

**Always reset colors:**
```python
print(f"{Colors.BRIGHT_GREEN}Success{Colors.ENDC}")  # ENDC resets to default
```

### Output Formatting Functions

```python
OutputFormatter.header("Title")          # Top-level header (cyan/magenta)
OutputFormatter.section("Section")       # Section header (yellow/blue)
OutputFormatter.divider()                # 60-char line: ----------
OutputFormatter.success("Done!")         # [√] Green success
OutputFormatter.error("Failed!")         # [×] Red error
OutputFormatter.info("Note...")          # [i] Cyan info
OutputFormatter.warning("Warning!")      # [!] Yellow warning
OutputFormatter.tip("Tip...")            # [*] Cyan tip/suggestion
OutputFormatter.step(1, "Step one")      # [1] Step indicator
OutputFormatter.menu_item(1, "Option")   # [1] Menu item
```

---

## Git Operations Patterns

### SSH Configuration

**⚠️ IMPORTANT: This tool ONLY supports SSH connections. HTTPS is not supported.**

- **GitHub:** `git@github.com:shumengya/{repo}.git`
- **Gitea:** `ssh://git@git.shumengya.top:8022/{user}/{repo}.git`

All remote operations (push, pull, fetch) use SSH. Do not use HTTPS URLs like `https://github.com/user/repo.git`.

**Prerequisites:**
1. User must have SSH keys generated (`ssh-keygen`)
2. Public key must be added to GitHub/Gitea account
3. SSH connection must be tested and working

### Command Execution

**Pattern for all Git commands:**

```python
# 1. Show status indicator
OutputFormatter.status('running', "Pushing to remote...")

# 2. Execute command (capture output)
success, output = self.executor.run("git push origin main", show_output=True)

# 3. Provide feedback
if success:
    OutputFormatter.success("Push successful")
else:
    OutputFormatter.error("Push failed")

return success
```

---

## Adding New Features

### Checklist for New Functionality

1. **Determine the module:** Where does this feature belong?
   - Git operations → `git_operations.py`
   - Remote management → `remote_manager.py`
   - UI/menus → `ui.py`
   - Config/constants → `config.py`
   - Utilities → `utils.py`

2. **Add type hints** to all functions

3. **Use OutputFormatter** for all user-facing messages

4. **Test manually** in a clean directory

5. **Update README.md** if adding user-facing features

---

## Common Gotchas

1. **Windows path handling:** Use `os.path` or `pathlib` for cross-platform paths
2. **Encoding:** All file I/O must specify `encoding='utf-8'`
3. **Subprocess:** Always use `encoding='utf-8', errors='ignore'` in `subprocess.run()`
4. **Git output:** Some commands have localized output; parse carefully
5. **Empty commits:** Check `git status --short` before committing
6. **Divider width:** Always use exactly 60 characters for consistency
7. **Platform differences:**
   - Use `python3` on Linux/macOS, `python` on Windows
   - Shell scripts: `.sh` for Unix, `.bat` for Windows
   - Clear screen: Use `PlatformUtils.clear_screen()` for cross-platform support

---

## Platform-Specific Notes

### Windows
- Use `run.bat` launcher to set UTF-8 encoding (`chcp 65001`)
- ANSI colors supported on Windows 10+ by default
- Python command: `python` (not `python3`)

### Linux/macOS
- Use `run.sh` launcher (requires `chmod +x run.sh` first time)
- Ensure terminal supports UTF-8 encoding
- Python command: `python3` (not `python`)
- Shell uses bash (shebang: `#!/bin/bash`)

### Cross-Platform Code
- Use `PlatformUtils.is_windows()`, `is_linux()`, `is_mac()` for platform detection
- Use `PlatformUtils.clear_screen()` instead of `os.system('cls')` or `os.system('clear')`
- Always use `os.path.join()` or `pathlib.Path` for file paths

---

## Future Development Notes

**Planned features (not yet implemented):**
- Branch management
- Tag management
- Conflict resolution assistance
- Custom configuration file support
- Batch operations for multiple repositories
- Formal test suite (pytest recommended)
- CI/CD pipeline

**When implementing these:**
- Follow the existing modular architecture
- Add to appropriate module (or create new module if needed)
- Maintain the colorful, user-friendly console output style
- Keep Windows compatibility in mind
