# -*- coding: utf-8 -*-

import os
import sys
import locale
import threading 
import time
from concurrent.futures import ThreadPoolExecutor 
from rich.console import Console
from rich.table import Table
from charset_normalizer import from_bytes
import pathlib
import argparse

# =========================
# I18N 国际化配置
# =========================
i18n = {
    "zh-cn": {
        "title": "📊 代码行数统计 (按类别)",
        "path": "路径",
        "file_cnt": "统计文件",
        "skip_cnt": "跳过文件",
        "skip_dir": "跳过目录",
        "err_path": "❌ 路径不存在",
        "t_type": "语言类别",
        "t_files": "文件数",
        "t_code": "代码行",
        "t_comment": "注释行",
        "t_empty": "空行",
        "t_code_char": "代码字符",
        "t_comment_char": "注释字符",
        "t_total": "总计"
    },
    "en-us": {
        "title": "📊 LOC Statistics (By Category)",
        "path": "Path",
        "file_cnt": "Files Processed",
        "skip_cnt": "Files Skipped",
        "skip_dir": "Skipped Directories",
        "err_path": "❌ Path not found",
        "t_type": "Language",
        "t_files": "Files",
        "t_code": "Code Lines",
        "t_comment": "Comment Lines",
        "t_empty": "Empty Lines",
        "t_code_char": "Code Chars",
        "t_comment_char": "Comment Chars",
        "t_total": "TOTAL"
    }
}

def detect_language():
    """
    跨平台语言检测
    """
    try:
        # 方法1: 使用 locale.getlocale
        sys_lang_code, _ = locale.getlocale(locale.LC_CTYPE)
        
        if sys_lang_code:
            # 处理各种可能的格式
            lang_str = sys_lang_code.lower()
            
            # 处理 Windows 格式: "Chinese (Simplified)_China"
            if 'chinese' in lang_str or 'zh' in lang_str:
                return "zh-cn"
            elif 'english' in lang_str or 'en' in lang_str:
                return "en-us"
                
        # 方法2: 检查环境变量
        env_vars = ['LANG', 'LC_ALL', 'LANGUAGE']
        for var in env_vars:
            value = os.environ.get(var, '').lower()
            if 'zh' in value or 'chinese' in value:
                return "zh-cn"
            elif 'en' in value or 'english' in value:
                return "en-us"
                
    except Exception as e:
        print(f"[-] Language detection error: {e}")
    
    # 默认返回英语
    return "en-us"

current_lang = detect_language()

def _t(key):
    return i18n.get(current_lang, i18n["en-us"]).get(key, key)


# =========================
# 配置：扩展名、注释规则、字符串规则
# =========================
config = {
    # 忽略的目录
    "ignore_dirs": [
        ".vs",
        ".vscode",
        ".idea",
        "node_modules",
        ".git",
        ".github"
    ],

    # 忽略的文件
    "ignore_files": [
    ],

    # 允许的扩展名
    "enabled_exts": {
    },

    # 允许的文件名+扩展名
    "enabled_filenames": {
    },

    # 注释配置
    "comment_types": {
    },

    # 字符串配置
    "string_types": {
    },

    "max_file_size": 16 * 1024 * 1024, # 16MB
    
    # 全局结果容器
    "result": {}, 
    "quick_result": {
        "file_count": 0,
        "skip_dir_count": 0,
        "skip_file_count": 0,
    },

    # 实时文件模式标志
    "enabled_file_mode": False,

    # 进度条显示标志（默认启用）
    "show_progress": True,
}

# 添加配置函数
def add_config(type : str, file_name : dict, comment_types : dict, string_types : dict):
    if "exts" in file_name:
        for ext in file_name["exts"]:
            config["enabled_exts"][ext] = type
    if "filenames" in file_name:
        for filename in file_name["filenames"]:
            config["enabled_filenames"][filename] = type
            
    config["comment_types"][type] = comment_types

    config["string_types"][type] = string_types

# 注册配置
# C 语言
add_config("C Header", {"exts": [".h"]}, {"single": ["//"], "multi": [["/*", "*/"]]}, {"single": ["\"", "\'"]})
# C 头文件
add_config("C", {"exts": [".c"]}, {"single": ["//"], "multi": [["/*", "*/"]]}, {"single": ["\"", "\'"]})
# C++ 源文件
add_config("C++ Header", {"exts": [".hpp", ".hh", ".h++", ".hxx"]}, {"single": ["//"], "multi": [["/*", "*/"]]}, {"single": ["\"", "\'"]})
# C++ 头文件
add_config("C++", {"exts": [".cpp", ".cc", ".c++", ".cxx"]}, {"single": ["//"], "multi": [["/*", "*/"]]}, {"single": ["\"", "\'"]})
# CMake 脚本
add_config("CMake", {"exts": [".cmake"], "filenames": ["CMakeLists.txt"]}, {"single": ["#"]}, {"quotes": ["\""]})
# Python 脚本
add_config("Python", {"exts": [".py"]}, {"single": ["#"]}, {"single": ["\""], "multi": [["\"\"\"", "\"\"\""], ["'''", "'''"]]})
# JavaScript 文件
add_config("JavaScript", {"exts": [".js", ".mjs", ".cjs"]}, {"single": ["//"], "multi": [["/*", "*/"]]}, {"single": ["\"", "'"], "multi": [["`", "`"]]})
# TypeScript 文件
add_config("TypeScript", {"exts": [".ts", ".mts", ".cts"]}, {"single": ["//"], "multi": [["/*", "*/"]]}, {"single": ["\"", "'"], "multi": [["`", "`"]]})
# Vue 文件
add_config("Vue", {"exts": [".vue"]}, {"single": ["//"], "multi": [["/*", "*/"], ["<!--", "-->"]]}, {"single": ["\"", "'"], "multi": [["`", "`"]]})
# Java 文件
add_config("Java", {"exts": [".java"]}, {"single": ["//"], "multi": [["/*", "*/"]]}, {"single": ["\""]})
# HTML 文件
add_config("HTML", {"exts": [".html", ".htm"]}, {}, {"multi": [["<!--", "-->"]]})
# CSS 文件
add_config("CSS", {"exts": [".css"]}, {"multi": [["/*", "*/"]]}, {})
# JSON 文件
add_config("JSON", {"exts": [".json", ".jsonl"]}, {}, {"single": ["\""]})
# YAML 文件
add_config("YAML", {"exts": [".yml", ".yaml"]}, {"single": ["#"]}, {})
# XML 文件
add_config("XML", {"exts": [".xml"]}, {}, {"multi": [["<!--", "-->"]]})
# TOML 文件
add_config("TOML", {"exts": [".toml"]}, {"single": ["#"]}, {})
# Rust 文件
add_config("Rust", {"exts": [".rs"]}, {"single": ["//"], "multi": [["/*", "*/"]]}, {"single": ["\""]})
# Go 文件
add_config("Go", {"exts": [".go"]}, {"single": ["//"], "multi": [["/*", "*/"]]}, {"single": ["\""]})
# PHP 文件
add_config("PHP", {"exts": [".php", ".phtml", ".php4", ".php5"]}, {"single": ["//", "#"], "multi": [["/*", "*/"]]}, {"single": ["\"", "'"]})
# Shell 脚本
add_config("Shell", {"exts": [".sh", ".bash", ".zsh"]}, {"single": ["#"]}, {})
# bat 脚本
add_config("bat", {"exts": [".bat"]}, {"single": ["REM"]}, {"single": ["\""]})
# powershell 脚本
add_config("powershell", {"exts": [".ps1"]}, {"single": ["#"]}, {"single": ["\""]})
# Lua 脚本
add_config("Lua", {"exts": [".lua"]}, {"single": ["--"], "multi": [["--[[", "]]"]]}, {"single": ["\""]})
# markdown 文件
add_config("markdown", {"exts": [".md", ".markdown"]}, {}, {})
# Perl 脚本
add_config("Perl", {"exts": [".pl"]}, {"single": ["#"]}, {"single": ["\"", "'"]})
# Assembly 文件
add_config("Assembly", {"exts": [".asm", ".s"]}, {"single": ["#", ";"]}, {"single": ["\"", "'"]})


# 引入全局锁来保护 config 字典的修改
CONFIG_LOCK = threading.Lock()

# =========================
# 高性能编码检测（已修复）
# =========================
def detect_encoding_fast(path):
    with open(path, "rb") as f:
        raw = f.read(32768)

    # BOM 快速判断
    if raw.startswith(b'\xef\xbb\xbf'):
        return "utf-8-sig"
    if raw.startswith(b'\xff\xfe'):
        return "utf-16-le"
    if raw.startswith(b'\xfe\xff'):
        return "utf-16-be"

    # UTF-8 快速路径（极快）
    try:
        raw.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass

    # charset-normalizer（高精度）
    best = from_bytes(raw).best()
    if best and best.encoding:
        return best.encoding

    # 兜底
    return "latin-1"

# =========================
# 核心解析器：状态机
# =========================
def count_line_segments(line, comment_conf, string_conf, state):
    """
    状态机：计算一行中的代码段、注释段以及非空白字符数量。
    """
    i = 0
    n = len(line)

    code_seg = code_chars = 0
    comment_seg = comment_chars = 0

    single_comments = comment_conf.get("single", [])
    multi_comments = comment_conf.get("multi", [])
    string_single = string_conf.get("single", [])
    multi_strings = string_conf.get("multi", [])

    has_code = False
    has_comment = False

    def start_code():
        nonlocal has_code, code_seg
        if not has_code:
            code_seg += 1
            has_code = True

    def start_comment():
        nonlocal has_comment, comment_seg
        if not has_comment:
            comment_seg += 1
            has_comment = True

    while i < n:
        char = line[i]

        # 1. 状态：在多行注释中
        if state["in_multi_comment"]:
            start_comment()
            
            if not char.isspace():
                comment_chars += 1
            
            closed = False
            for s, e in multi_comments:
                if line.startswith(e, i):
                    for c_char in e:
                        if not c_char.isspace():
                            comment_chars += 1
                    
                    i += len(e)
                    state["in_multi_comment"] = False
                    has_comment = False
                    closed = True
                    break
            
            if not closed:
                i += 1
            continue

        # 2. 状态：在字符串中 (只统计非空白字符)
        if state["in_string"]:
            start_code()
            
            if not char.isspace():
                code_chars += 1 

            if char == "\\" and i + 1 < n:
                if not line[i+1].isspace():
                    code_chars += 1
                i += 2
                continue
            
            ender = state["string_ender"]
            if line.startswith(ender, i):
                for s_char in ender:
                    if not s_char.isspace():
                        code_chars += 1
                
                i += len(ender)
                state["in_string"] = False
                state["string_ender"] = None
                continue
            
            i += 1
            continue

        # 3. 正常模式：检查各种开始标记

        # A. 检查多行注释开始
        is_multi_comment_start = False
        for s, e in multi_comments:
            if line.startswith(s, i):
                start_comment()
                for c_char in s:
                    if not c_char.isspace():
                        comment_chars += 1
                
                i += len(s)
                state["in_multi_comment"] = True
                has_code = False
                is_multi_comment_start = True
                break
        if is_multi_comment_start:
            continue

        # B. 检查多行/特殊字符串开始
        is_multi_string_start = False
        for s, e in multi_strings:
            if line.startswith(s, i):
                start_code()
                for s_char in s:
                    if not s_char.isspace():
                        code_chars += 1
                
                i += len(s)
                state["in_string"] = True
                state["string_ender"] = e
                is_multi_string_start = True
                break
        if is_multi_string_start:
            continue

        # C. 检查普通字符串开始
        if char in string_single:
            start_code()
            code_chars += 1
            state["in_string"] = True
            state["string_ender"] = char
            i += 1
            continue

        # D. 检查单行注释开始
        for s in single_comments:
            if line.startswith(s, i):
                start_comment()
                
                for c_char in s:
                    if not c_char.isspace():
                        comment_chars += 1

                rest_of_line = line[i + len(s):].rstrip()
                for c_char in rest_of_line:
                    if not c_char.isspace():
                        comment_chars += 1
                
                return code_seg, code_chars, comment_seg, comment_chars
        
        # E. 普通代码字符
        if not char.isspace():
            start_code()
            code_chars += 1
        
        i += 1

    return code_seg, code_chars, comment_seg, comment_chars


# =========================
# 文件处理 (为多线程修改)
# =========================
def handle_file(file_path):
    """处理单个文件，并将结果安全地存储到全局配置中。"""
    # 扩展名
    ext = os.path.splitext(file_path)[1].lower()
    # 文件名+扩展名
    file_name = os.path.basename(file_path)

    # 文件大小限制
    if os.path.getsize(file_path) > config["max_file_size"]:
        with CONFIG_LOCK:
            config["quick_result"]["skip_file_count"] += 1
        return

    # 判断文件类型
    file_type = None
    if file_name in config["enabled_filenames"]:
        file_type = config["enabled_filenames"][file_name]
    elif ext in config["enabled_exts"]:
        file_type = config["enabled_exts"][ext]

    if not file_type:
        # 文件类型不支持，跳过
        with CONFIG_LOCK:
            config["quick_result"]["skip_file_count"] += 1
        return

    comment_conf = config["comment_types"].get(file_type, {})
    string_conf = config["string_types"].get(file_type, {})

    lines = None

    # 自动检测编码
    try:
        encoding = detect_encoding_fast(file_path)
        with open(file_path, "r", encoding=encoding, errors="replace") as f:
            lines = f.readlines()
    except Exception:
        with CONFIG_LOCK:
            config["quick_result"]["skip_file_count"] += 1
        return
                
    if lines is None:
        with CONFIG_LOCK:
            config["quick_result"]["skip_file_count"] += 1
        return

    # 局部结果 (线程私有)
    res = {
        "file": file_path,
        "code": 0, "code_char": 0,
        "comment": 0, "comment_char": 0,
        "empty": 0,
    }

    state = {
        "in_multi_comment": False,
        "in_string": False,
        "string_ender": None
    }

    for line in lines:
        stripped = line.strip()
        if stripped == "":
            res["empty"] += 1
            continue

        cs, cc, ms, mc = count_line_segments(line, comment_conf, string_conf, state)
        
        res["code"] += cs
        res["code_char"] += cc
        res["comment"] += ms
        res["comment_char"] += mc

    # --- 线程安全区域：将局部结果合并到全局 config ---
    with CONFIG_LOCK:
        config["quick_result"]["file_count"] += 1
        config["result"].setdefault(file_type, []).append(res)
          # 如果启用了文件模式，立即输出文件详细信息
    if config["enabled_file_mode"]:
        print(f"{_t("path")}: {res['file']} \t{_t("t_type")}: {file_type} \t{"t_code"}: {res['code']} \t"
              f"{_t("t_comment")}: {res['comment']} \t{_t("t_empty")}: {res['empty']} \t"
              f"{_t("t_code_char")}: {res['code_char']} \t{_t("t_comment_char")}: {res['comment_char']}")
    # --------------------------------------------------


# =========================
# 文件收集器 (只负责收集路径)
# =========================
def walk_dir(dir_path, file_list):
    """递归遍历目录并收集所有需要处理的文件路径"""
    try:
        dir_path_obj = pathlib.Path(dir_path)
        
        for item in dir_path_obj.iterdir():
            try:
                if item.is_file():
                    if item.name in config["ignore_files"]:
                        with CONFIG_LOCK:
                            config["quick_result"]["skip_file_count"] += 1
                        continue
                    file_list.append(str(item))
                elif item.is_dir():
                    if item.name in config["ignore_dirs"]:
                        with CONFIG_LOCK:
                            config["quick_result"]["skip_dir_count"] += 1
                        continue
                    walk_dir(str(item), file_list)
            except (OSError, PermissionError):
                # 忽略无法访问的文件或目录
                continue
                
    except (OSError, PermissionError):
        # 回退到传统的 os.listdir 方法
        try:
            items = os.listdir(dir_path)
        except:
            return

        for item in items:
            try:
                path = os.path.join(dir_path, item)
                if os.path.isfile(path):
                    file_list.append(path)
                elif os.path.isdir(path):
                    if item in config["ignore_dirs"]:
                        with CONFIG_LOCK:
                            config["quick_result"]["skip_dir_count"] += 1
                        continue
                    walk_dir(path, file_list)
            except (OSError, PermissionError):
                continue

def get_all_files_to_process(paths):
    """根据命令行参数获取所有待处理的文件路径"""
    file_list = []
    for path in paths:
        # 清理路径字符串，移除可能的引号
        path = path.strip('"\'')  # 移除首尾的引号
        
        # 使用 pathlib 处理路径
        try:
            import pathlib
            p = pathlib.Path(path)
            # resolve() 会处理相对路径并规范化路径
            resolved_path = p.resolve()
            
            if resolved_path.exists():
                if resolved_path.is_file():
                    file_list.append(str(resolved_path))
                elif resolved_path.is_dir():
                    walk_dir(str(resolved_path), file_list)
            else:
                # 尝试不解析的路径
                if p.exists():
                    if p.is_file():
                        file_list.append(str(p))
                    elif p.is_dir():
                        walk_dir(str(p), file_list)
                else:
                    print(f"{_t('err_path')}: {resolved_path}")
        except Exception:
            # 回退到传统方法
            try:
                normalized_path = os.path.abspath(os.path.normpath(path))
                if os.path.exists(normalized_path):
                    if os.path.isfile(normalized_path):
                        file_list.append(normalized_path)
                    else:
                        walk_dir(normalized_path, file_list)
                else:
                    print(f"{_t('err_path')}: {normalized_path}")
            except Exception as e:
                print(f"{_t('err_path')}: {path} - {str(e)}")
                
    return file_list


# =========================
# 实时进度显示线程函数
# =========================
def progress_displayer(total_files, stop_event):
    """实时在终端显示处理进度的独立线程函数"""
    # 使用 Rich Console，并输出到 stderr 以避免干扰 stdout 的最终表格
    local_console = Console(file=sys.stderr) 
    
    # 使用 Rich 的 screen 上下文管理器来实时更新同一行内容
    with local_console.screen() as screen:
        while not stop_event.is_set():
            # 安全读取 quick_result
            with CONFIG_LOCK:
                file_count = config["quick_result"]["file_count"]
                skip_count = config["quick_result"]["skip_file_count"]
            
            processed_count = file_count + skip_count
            
            # 计算进度百分比
            if total_files > 0:
                percent = processed_count / total_files
            else:
                percent = 1.0 # 如果没有文件则视为完成

            # 格式化进度条和状态信息
            progress_percent = f"[progress.percentage]{percent*100:3.1f}%[/progress.percentage]"
            progress_count = f"[progress.remaining]({processed_count} / {total_files})[/progress.remaining]"
            
            status_line = (
                f"Processing: [bold blue]{progress_percent} {progress_count}[/bold blue] "
                f"| {_t('file_cnt')}: [green]{file_count}[/green] "
                f"| {_t('skip_cnt')}: [dim]{skip_count}[/dim]"
            )
            
            # 刷新当前行
            screen.update(status_line)
            
            # 200ms 延迟
            time.sleep(0.2)
        
        # 退出前清除状态行 (使用空字符串更新)
        screen.update("")

# =========================
# 主程序
# =========================
def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='代码行数统计工具')
    parser.add_argument('paths', nargs='*', help='要统计的路径')
    parser.add_argument('-f', '--file-mode', action='store_true', help='启用文件模式，处理完每个文件后立即输出详细信息')
    
    args = parser.parse_args()
    
    # 设置文件模式标志和进度条显示标志
    with CONFIG_LOCK:
        config["enabled_file_mode"] = args.file_mode
        # 当启用文件模式时，禁用进度条显示以避免输出冲突
        config["show_progress"] = not args.file_mode
    
    if not args.paths:
        paths = [os.getcwd()]
    else:
        paths = args.paths
    
    # 1. 收集所有文件路径
    all_files = get_all_files_to_process(paths)
    total_files = len(all_files)
    
    console = Console()

    # 2. 启动进度显示线程（仅在需要时启动）
    progress_thread = None
    stop_display_event = None
    
    if config["show_progress"]:
        stop_display_event = threading.Event()
        progress_thread = threading.Thread(
            target=progress_displayer, 
            args=(total_files, stop_display_event), 
            daemon=True # 设置为守护线程，主程序退出时它也会退出
        )
        progress_thread.start()

    # 3. 使用线程池并行处理文件
    max_workers = os.cpu_count() * 2 if os.cpu_count() else 8
    
    # 使用 try...finally 确保在任何情况下都会停止进度显示线程
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(handle_file, all_files)
    finally:
        # 4. 停止进度显示线程并等待它完成（仅在启动了进度线程时）
        if progress_thread is not None and stop_display_event is not None:
            stop_display_event.set()
            progress_thread.join()
    
    # 5. 结果汇总和展示
    
    # 打印概览
    print(f"\n{_t('title')}")
    print(f"{_t('file_cnt')}: {config['quick_result']['file_count']}")
    print(f"{_t('skip_cnt')}: {config['quick_result']['skip_file_count']}")
    print(f"{_t('skip_dir')}: {config['quick_result']['skip_dir_count']}")

    # 创建表格
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column(_t("t_type"), justify="left", style="bold yellow")
    table.add_column(_t("t_files"), justify="right")
    table.add_column(_t("t_code"), justify="right", style="green")
    table.add_column(_t("t_comment"), justify="right", style="dim")
    table.add_column(_t("t_empty"), justify="right")
    table.add_column(_t("t_code_char"), justify="right")
    table.add_column(_t("t_comment_char"), justify="right")

    grand_total = {
        "files": 0, "code": 0, "comment": 0, "empty": 0, 
        "code_char": 0, "comment_char": 0
    }

    # 按类别汇总
    file_type_stats = []

    for ftype, file_list in config["result"].items():
        t_files = len(file_list)
        t_code = sum(f["code"] for f in file_list)
        t_comment = sum(f["comment"] for f in file_list)
        t_empty = sum(f["empty"] for f in file_list)
        t_code_char = sum(f["code_char"] for f in file_list)
        t_comment_char = sum(f["comment_char"] for f in file_list)

        grand_total["files"] += t_files
        grand_total["code"] += t_code
        grand_total["comment"] += t_comment
        grand_total["empty"] += t_empty
        grand_total["code_char"] += t_code_char
        grand_total["comment_char"] += t_comment_char

        # 保存每个文件类型统计数据，用于后续排序
        file_type_stats.append({
            "type": ftype,
            "files": t_files,
            "code": t_code,
            "comment": t_comment,
            "empty": t_empty,
            "code_char": t_code_char,
            "comment_char": t_comment_char
        })

    # 按照代码行数降序排序
    file_type_stats.sort(key=lambda x: x["code"], reverse=True)

    # 添加排序后的数据到表格
    for stat in file_type_stats:
        table.add_row(
            stat["type"],
            str(stat["files"]),
            f"{stat['code']:,}",
            f"{stat['comment']:,}",
            f"{stat['empty']:,}",
            f"{stat['code_char']:,}",
            f"{stat['comment_char']:,}",
        )

    # 添加总计行
    table.add_row(
        f"[bold]{_t('t_total')}[/bold]",
        f"[bold]{grand_total['files']:,}[/bold]",
        f"[bold][green]{grand_total['code']:,}[/green][/bold]",
        f"[bold][dim]{grand_total['comment']:,}[/dim][/bold]",
        f"[bold]{grand_total['empty']:,}[/bold]",
        f"[bold]{grand_total['code_char']:,}[/bold]",
        f"[bold]{grand_total['comment_char']:,}[/bold]",
    )

    # 打印表格
    console.print(table)
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)