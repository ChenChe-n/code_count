[English](README.md) | [中文](README_zh.md)

# 代码行数统计工具

这是一个强大的代码行数统计工具，支持多种编程语言，具有高性能、准确识别注释和跨平台等特点。

## 功能特点

- 🚀 **高性能**: 利用多线程技术并行处理文件，大幅提升统计速度
- 🌍 **多语言支持**: 支持 30+ 种编程语言，包括 Python, Java, JavaScript, C++, HTML, CSS 等
- 💬 **智能注释识别**: 准确区分代码行、注释行和空行
- 🔤 **字符统计**: 统计代码字符数和注释字符数
- 📊 **可视化输出**: 使用 Rich 库提供美观的表格输出
- 🌐 **国际化**: 支持中英文界面自动切换
- 🧠 **智能编码检测**: 自动检测文件编码，支持 UTF-8, GBK 等多种编码
- 🗂️ **文件模式**: 可选的文件模式，逐文件实时输出统计信息
- ⏱️ **进度显示**: 显示实时处理进度
- 🚫 **忽略规则**: 自动忽略常见的开发工具目录如 `.git`, `node_modules` 等

## 支持的语言

- Python (.py)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
- HTML (.html, .htm)
- CSS (.css)
- JSON (.json)
- XML (.xml)
- YAML (.yml, .yaml)
- Go (.go)
- Rust (.rs)
- PHP (.php)
- Shell (.sh)
- PowerShell (.ps1)
- Lua (.lua)
- Markdown (.md)
- CMake (.cmake, CMakeLists.txt)
- And more...

## 安装要求

- Python 3.6+
- 依赖包:
  - `rich` >= 10.0.0
  - `chardet` >= 4.0.0

## 安装步骤

1. 克隆或下载此仓库
2. 安装依赖包:
   ```bash
   pip install -r requirements.txt
   ```
   
   或者分别安装:
   ```bash
   pip install rich>=10.0.0
   pip install chardet>=4.0.0
   ```

## 使用方法

### 基本用法

```bash
python main.py
```

这将统计当前目录下的所有代码文件。

### 指定路径

```bash
python main.py /path/to/code
python main.py /path/to/project1 /path/to/project2
```

### 文件模式

使用 `-f` 或 `--file-mode` 参数启用文件模式，在处理完每个文件后立即输出详细信息：

```bash
python main.py -f
python main.py --file-mode /path/to/code
```

### 路径包含空格

如果路径包含空格，请使用引号包围：

```bash
python main.py "/path/to/my project"
```

## 输出说明

工具会输出一个表格，包含以下列：

- **语言类别**: 文件的编程语言类型
- **文件数**: 该语言类型的文件数量
- **代码行**: 实际代码行数（不含注释和空行）
- **注释行**: 注释行数
- **空行**: 空行数
- **代码字符**: 代码行中的非空白字符数
- **注释字符**: 注释行中的非空白字符数

## 许可证

MIT License